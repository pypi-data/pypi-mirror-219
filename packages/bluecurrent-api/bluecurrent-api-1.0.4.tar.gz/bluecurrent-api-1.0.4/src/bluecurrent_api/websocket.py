"""Define an object that handles the connection to the Websocket"""
import asyncio
import json
from asyncio import Event
from typing import Any, Callable, Optional, cast

from websockets.client import WebSocketClientProtocol, connect
from websockets.exceptions import (
    ConnectionClosed,
    ConnectionClosedError,
    InvalidStatusCode,
    WebSocketException,
)

from .exceptions import (
    AlreadyConnected,
    InvalidApiToken,
    NoCardsFound,
    RequestLimitReached,
    WebsocketError,
)
from .utils import (
    get_dummy_message,
    get_exception,
    handle_charge_points,
    handle_grid,
    handle_session_messages,
    handle_setting_change,
    handle_settings,
    handle_status,
)

URL = "wss://motown.bluecurrent.nl/haserver"
BUTTONS = ("START_SESSION", "STOP_SESSION", "SOFT_RESET", "REBOOT")


class Websocket:
    """Class for handling requests and responses for the BlueCurrent Websocket Api."""

    _connection: Optional[WebSocketClientProtocol] = None
    _has_connection: bool = False
    auth_token: Optional[str] = None
    receiver: Callable
    receive_event: Optional[Event] = None
    receiver_is_coroutine: bool

    def __init__(self) -> None:
        pass

    def get_receiver_event(self) -> Event:
        """Return cleared receive_event when connected."""

        self._check_connection()
        if self.receive_event is None:
            self.receive_event = Event()

        self.receive_event.clear()
        return self.receive_event

    async def validate_api_token(self, api_token: str) -> bool:
        """Validate an api token."""
        await self._connect()
        await self._send({"command": "VALIDATE_API_TOKEN", "token": api_token})
        res = await self._recv()
        await self.disconnect()

        if res["object"] == "ERROR":
            raise get_exception(res)

        if not res.get("success"):
            raise InvalidApiToken
        self.auth_token = "Token " + res["token"]
        return True

    async def get_email(self) -> str:
        """Return the user email"""
        if not self.auth_token:
            raise WebsocketError("token not set")
        await self._connect()
        await self.send_request({"command": "GET_ACCOUNT"})
        res = await self._recv()
        await self.disconnect()

        if res["object"] == "ERROR":
            raise get_exception(res)

        if not res.get("login"):
            raise WebsocketError("No email found")
        return cast(str, res["login"])

    async def get_charge_cards(self) -> list[dict[str, Any]]:
        """Get the charge cards."""
        if not self.auth_token:
            raise WebsocketError("token not set")
        await self._connect()
        await self.send_request({"command": "GET_CHARGE_CARDS"})
        res: dict[str, Any] = await self._recv()
        await self.disconnect()
        cards = cast(list[dict[str, Any]], res.get("cards"))

        if res["object"] == "ERROR":
            raise get_exception(res)

        if len(cards) == 0:
            raise NoCardsFound
        return cards

    async def connect(self, api_token: str) -> None:
        """Validate api_token and connect to the websocket."""
        if self._has_connection:
            raise WebsocketError("Connection already started.")
        await self.validate_api_token(api_token)
        await self._connect()

    async def _connect(self) -> None:
        """Connect to the websocket."""
        try:
            self._connection = await connect(URL)
            self._has_connection = True
        except Exception as err:
            self.check_for_server_reject(err)
            raise WebsocketError("Cannot connect to the websocket.") from err

    async def send_request(self, request: dict[str, Any]) -> None:
        """Add authorization and send request."""
        if not self.auth_token:
            raise WebsocketError("Token not set")

        request["Authorization"] = self.auth_token
        await self._send(request)

    async def loop(self, receiver: Callable) -> None:
        """Loop the message_handler."""

        self.receiver = receiver
        self.receiver_is_coroutine = asyncio.iscoroutinefunction(receiver)

        # Needed for receiving updates
        await self._send(
            {
                "command": "HELLO",
                "Authorization": self.auth_token,
                "header": "homeassistant",
            }
        )

        while True:
            stop = await self._message_handler()
            if stop:
                break

    async def _message_handler(self) -> bool:
        """Wait for a message and give it to the receiver."""

        message: dict[str, Any] = await self._recv()

        # websocket has disconnected
        if not message:
            return True

        object_name = message.get("object")

        if not object_name:
            raise WebsocketError("Received message has no object.")

        # handle ERROR object
        if object_name == "ERROR":
            raise get_exception(message)

        # if object other than ERROR has an error key it will be send to the receiver.
        error = message.get("error")

        # ignored objects
        if (
            ("RECEIVED" in object_name and not error)
            or object_name == "HELLO"
            or "OPERATIVE" in object_name
        ):
            return False
        if object_name == "CHARGE_POINTS":
            handle_charge_points(message)
        elif object_name == "CH_STATUS":
            handle_status(message)
        elif object_name == "CH_SETTINGS":
            handle_settings(message)
        elif "GRID" in object_name:
            handle_grid(message)
        elif object_name in (
            "STATUS_SET_PUBLIC_CHARGING",
            "STATUS_SET_PLUG_AND_CHARGE",
        ):
            handle_setting_change(message)
        elif any(button in object_name for button in BUTTONS):
            handle_session_messages(message)
        else:
            return False

        self.handle_receive_event()

        await self.send_to_receiver(message)

        # Fix for api sending old start_datetime
        if object_name == "STATUS_START_SESSION" and not error:
            await self.send_to_receiver(get_dummy_message(message["evse_id"]))

        return False

    async def send_to_receiver(self, message: dict[str, Any]) -> None:
        """Send data to the given receiver."""
        if self.receiver_is_coroutine:
            await self.receiver(message)
        else:
            self.receiver(message)

    async def _send(self, data: dict[str, Any]) -> None:
        """Send data to the websocket."""
        self._check_connection()
        try:
            data_str = json.dumps(data)
            assert self._connection is not None
            await self._connection.send(data_str)
        except (ConnectionClosed, InvalidStatusCode) as err:
            self.handle_connection_errors(err)

    async def _recv(self) -> Any:
        """Receive data from de websocket."""
        self._check_connection()
        assert self._connection is not None
        try:
            data = await self._connection.recv()
            return json.loads(data)
        except (ConnectionClosed, InvalidStatusCode) as err:
            self.handle_connection_errors(err)
            return None

    def handle_connection_errors(self, err: WebSocketException) -> None:
        """Handle connection errors."""
        if self._has_connection:
            self._has_connection = False
            self.handle_receive_event()
            self.check_for_server_reject(err)
            raise WebsocketError("Connection was closed.")

    async def disconnect(self) -> None:
        """Disconnect from de websocket."""
        self._check_connection()
        assert self._connection is not None
        if not self._has_connection:
            raise WebsocketError("Connection is already closed.")
        self._has_connection = False
        self.handle_receive_event()
        await self._connection.close()

    def _check_connection(self) -> None:
        """Throw error if there is no connection."""
        if self._connection is None:
            raise WebsocketError("No connection with the api.")

    def handle_receive_event(self) -> None:
        "Set receive_event if it exists"
        if self.receive_event is not None:
            self.receive_event.set()

    def check_for_server_reject(self, err: Exception) -> None:
        """Check if the client was rejected by the server"""

        if isinstance(err, InvalidStatusCode):
            reason = err.headers.get("x-websocket-reject-reason")
            if reason is not None:
                if "Request limit reached" in reason:
                    raise RequestLimitReached("Request limit reached") from err
                if "Already connected" in reason:
                    raise AlreadyConnected("Already connected")
        if isinstance(err, ConnectionClosedError) and err.code == 4001:
            raise RequestLimitReached("Request limit reached") from err
