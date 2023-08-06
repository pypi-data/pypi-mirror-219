"""Define an object to interact with the BlueCurrent websocket api."""
from datetime import timedelta
from typing import Any, Callable, Optional

from .utils import get_next_reset_delta
from .websocket import Websocket


class Client:
    """Api Client for the BlueCurrent Websocket Api."""

    def __init__(self) -> None:
        """Initialize the Client."""
        self.websocket = Websocket()

    def get_next_reset_delta(self) -> timedelta:
        """Returns the next reset delta"""
        return get_next_reset_delta()

    async def wait_for_response(self) -> None:
        """Wait for next response."""
        await self.websocket.get_receiver_event().wait()

    async def validate_api_token(self, api_token: str) -> bool:
        """Validate an api_token."""
        return await self.websocket.validate_api_token(api_token)

    async def get_email(self) -> str:
        """Get user email."""
        return await self.websocket.get_email()

    async def get_charge_cards(self) -> list[dict[str, Any]]:
        """Get the charge cards."""
        return await self.websocket.get_charge_cards()

    async def connect(self, api_token: str) -> None:
        """Connect to the websocket."""
        await self.websocket.connect(api_token)

    async def start_loop(self, receiver: Callable[[dict[str, Any]], None]) -> None:
        """Start the receive loop."""
        await self.websocket.loop(receiver)

    async def disconnect(self) -> None:
        """Disconnect the websocket."""
        await self.websocket.disconnect()

    async def get_charge_points(self) -> None:
        """Get the charge points."""
        request = self._create_request("GET_CHARGE_POINTS")
        await self.websocket.send_request(request)

    async def get_status(self, evse_id: str) -> None:
        """Get the status of a charge point."""
        request = self._create_request("GET_CH_STATUS", evse_id)
        await self.websocket.send_request(request)

    async def get_settings(self, evse_id: str) -> None:
        """Get the settings of a charge point."""
        request = self._create_request("GET_CH_SETTINGS", evse_id)
        await self.websocket.send_request(request)

    async def get_grid_status(self, evse_id: str) -> None:
        """Get the grid status of a charge point."""
        request = self._create_request("GET_GRID_STATUS", evse_id)
        await self.websocket.send_request(request)

    async def set_linked_charge_cards_only(self, evse_id: str, value: bool) -> None:
        """Set public_charging of a charge point to a value."""
        request = self._create_request("SET_PUBLIC_CHARGING", evse_id, not value)
        await self.websocket.send_request(request)

    async def set_plug_and_charge(self, evse_id: str, value: bool) -> None:
        """Set plug_and_charge of a charge point to a value."""
        request = self._create_request("SET_PLUG_AND_CHARGE", evse_id, value)
        await self.websocket.send_request(request)

    async def block(self, evse_id: str, value: bool) -> None:
        """Set available of a charge point to a value."""
        command = "SET_OPERATIVE"
        if value is True:
            command = "SET_INOPERATIVE"
        request = self._create_request(command, evse_id)
        await self.websocket.send_request(request)

    async def reset(self, evse_id: str) -> None:
        """Reset a charge point."""
        request = self._create_request("SOFT_RESET", evse_id)
        await self.websocket.send_request(request)

    async def reboot(self, evse_id: str) -> None:
        """Reboot a charge point."""
        request = self._create_request("REBOOT", evse_id)
        await self.websocket.send_request(request)

    async def start_session(self, evse_id: str, card_uid: str) -> None:
        """Start a charge session at a charge point."""
        request = self._create_request("START_SESSION", evse_id, card_uid=card_uid)
        await self.websocket.send_request(request)

    async def stop_session(self, evse_id: str) -> None:
        """Stop a charge session at a charge point."""
        request = self._create_request("STOP_SESSION", evse_id)
        await self.websocket.send_request(request)

    def _create_request(
        self,
        command: str,
        evse_id: Optional[str] = None,
        value: Optional[bool] = None,
        card_uid: Optional[str] = None,
    ) -> dict[str, Any]:
        """Create a request."""
        request: dict[str, Any] = {"command": command}

        if evse_id:
            request["evse_id"] = evse_id

        if value is not None:
            request["value"] = value

        if card_uid:
            request["session_token"] = card_uid

        return request
