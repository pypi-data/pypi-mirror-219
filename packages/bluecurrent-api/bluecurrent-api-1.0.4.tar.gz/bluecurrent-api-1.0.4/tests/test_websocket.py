from unittest.mock import AsyncMock
from websockets.exceptions import InvalidStatusCode, ConnectionClosedError
from websockets.frames import Close

from src.bluecurrent_api.websocket import Websocket
from src.bluecurrent_api.exceptions import WebsocketError, InvalidApiToken, NoCardsFound, RequestLimitReached, AlreadyConnected
from asyncio.exceptions import TimeoutError
import pytest
from pytest_mock import MockerFixture
import asyncio


@pytest.mark.asyncio
async def test_get_receiver_event(mocker: MockerFixture):
    websocket = Websocket()

    with pytest.raises(WebsocketError):
        websocket.get_receiver_event()

    mocker.patch.object(Websocket, '_connection')

    websocket.get_receiver_event()
    assert websocket.receive_event is not None
    assert websocket.receive_event.is_set() == False


@pytest.mark.asyncio
async def test_validate_token(mocker: MockerFixture):
    api_token = '123'
    websocket = Websocket()
    mocker.patch('src.bluecurrent_api.websocket.Websocket._connect')
    mocker.patch('src.bluecurrent_api.websocket.Websocket._send')
    mocker.patch('src.bluecurrent_api.websocket.Websocket.disconnect')

    mocker.patch(
        'src.bluecurrent_api.websocket.Websocket._recv',
        return_value={"object": "STATUS_API_TOKEN",
                      "success": True, "token": "abc"}
    )
    result = await websocket.validate_api_token(api_token)
    assert result == True
    assert websocket.auth_token == "Token abc"

    mocker.patch(
        'src.bluecurrent_api.websocket.Websocket._recv',
        return_value={"object": "STATUS_API_TOKEN",
                      "success": False, 'error': ""}
    )
    with pytest.raises(InvalidApiToken):
        await websocket.validate_api_token(api_token)

    mocker.patch(
        'src.bluecurrent_api.websocket.Websocket._recv',
        return_value={"object": "ERROR",
                      "error": 42, 'message': "Request limit reached"}
    )
    with pytest.raises(RequestLimitReached) as err:
        await websocket.validate_api_token(api_token)


@pytest.mark.asyncio
async def test_get_email(mocker: MockerFixture):
    websocket = Websocket()
    mocker.patch('src.bluecurrent_api.websocket.Websocket._connect')
    mocker.patch('src.bluecurrent_api.websocket.Websocket._send')
    mocker.patch('src.bluecurrent_api.websocket.Websocket.disconnect')
    mocker.patch(
        'src.bluecurrent_api.websocket.Websocket._recv',
        return_value={"object": "ACCOUNT", "login": 'test'}
    )

    with pytest.raises(WebsocketError):
        await websocket.get_email()
    websocket.auth_token = 'abc'
    assert await websocket.get_email() == 'test'

    mocker.patch(
        'src.bluecurrent_api.websocket.Websocket._recv',
        return_value={"object": "ACCOUNT"}
    )
    with pytest.raises(WebsocketError):
        await websocket.get_email()

    mocker.patch(
        'src.bluecurrent_api.websocket.Websocket._recv',
        return_value={"object": "ERROR",
                      "error": 42, 'message': "Request limit reached"}
    )
    with pytest.raises(RequestLimitReached):
        await websocket.get_email()


@pytest.mark.asyncio
async def test_get_charge_cards(mocker: MockerFixture):
    websocket = Websocket()
    mocker.patch('src.bluecurrent_api.websocket.Websocket._connect')
    mocker.patch('src.bluecurrent_api.websocket.Websocket._send')
    mocker.patch('src.bluecurrent_api.websocket.Websocket.disconnect')

    mocker.patch(
        'src.bluecurrent_api.websocket.Websocket._recv',
        return_value={"object": "CHARGE_CARDS", "cards": []}
    )

    with pytest.raises(WebsocketError):
        await websocket.get_charge_cards()
    websocket.auth_token = '123'
    with pytest.raises(NoCardsFound):
        await websocket.get_charge_cards()

    cards = [{"name": "card_1", "uid": "1234", "id": "abc"}]
    mocker.patch(
        'src.bluecurrent_api.websocket.Websocket._recv',
        return_value={"object": "CHARGE_CARDS", "cards": cards}
    )
    result = await websocket.get_charge_cards()
    assert result == cards

    mocker.patch(
        'src.bluecurrent_api.websocket.Websocket._recv',
        return_value={"object": "ERROR",
                      "error": 42, 'message': "Request limit reached"}
    )
    with pytest.raises(RequestLimitReached) as err:
        await websocket.get_charge_cards()


@pytest.mark.asyncio
async def test_connect(mocker: MockerFixture):
    mocker.patch('src.bluecurrent_api.websocket.Websocket._send')
    websocket = Websocket()
    api_token = '123'

    websocket._has_connection = True
    with pytest.raises(WebsocketError):
        await websocket.connect(api_token)


@pytest.mark.asyncio
async def test__connect(mocker: MockerFixture):
    websocket = Websocket()
    mocker.patch.object(Websocket, '_connection')
    mocker.patch(
        'src.bluecurrent_api.websocket.connect',
        create=True,
        side_effect=ConnectionRefusedError
    )
    with pytest.raises(WebsocketError):
        await websocket._connect()

    mocker.patch(
        'src.bluecurrent_api.websocket.connect',
        create=True,
        side_effect=TimeoutError
    )
    with pytest.raises(WebsocketError):
        await websocket._connect()

    mocker.patch(
        'src.bluecurrent_api.websocket.connect',
        create=True,
        side_effect=InvalidStatusCode(
            403, {'x-websocket-reject-reason': 'Request limit reached'})
    )
    with pytest.raises(RequestLimitReached):
        await websocket._connect()

    mocker.patch(
        'src.bluecurrent_api.websocket.connect',
        create=True,
        side_effect=InvalidStatusCode(
            403, {'x-websocket-reject-reason': 'Already connected'})
    )
    with pytest.raises(AlreadyConnected):
        await websocket._connect()


@pytest.mark.asyncio
async def test_send_request(mocker: MockerFixture):
    websocket = Websocket()
    mock_send = mocker.patch.object(Websocket, '_send')

    # without receiver
    with pytest.raises(WebsocketError):
        await websocket.send_request({"command": "GET_CHARGE_POINTS"})

    websocket.receiver = mocker.Mock()

    # without token
    with pytest.raises(WebsocketError):
        await websocket.send_request({"command": "GET_CHARGE_POINTS"})

    websocket.auth_token = '123'

    await websocket.send_request({"command": "GET_CHARGE_POINTS"})

    mock_send.assert_called_with(
        {"command": "GET_CHARGE_POINTS", "Authorization": "123"})


@pytest.mark.asyncio
async def test_loop(mocker: MockerFixture):
    mocker.patch('src.bluecurrent_api.websocket.Websocket._send')
    mocker.patch(
        'src.bluecurrent_api.websocket.Websocket._message_handler', return_value=True)
    websocket = Websocket()

    def receiver():
        pass

    async def async_receiver():
        pass

    await websocket.loop(receiver)
    assert websocket.receiver == receiver
    assert websocket.receiver_is_coroutine == False

    await websocket.loop(async_receiver)
    assert websocket.receiver == async_receiver
    assert websocket.receiver_is_coroutine == True


@pytest.mark.asyncio
async def test_message_handler(mocker: MockerFixture):

    mock_handle_charge_points = mocker.patch(
        'src.bluecurrent_api.websocket.handle_charge_points')
    mock_handle_status = mocker.patch(
        'src.bluecurrent_api.websocket.handle_status')
    mock_handle_grid = mocker.patch(
        'src.bluecurrent_api.websocket.handle_grid')
    mock_handle_settings = mocker.patch(
        'src.bluecurrent_api.websocket.handle_settings')
    mock_handle_setting_change = mocker.patch(
        'src.bluecurrent_api.websocket.handle_setting_change')

    mock_handle_handle_session_messages = mocker.patch(
        'src.bluecurrent_api.websocket.handle_session_messages')

    mocker.patch.object(Websocket, 'handle_receive_event')

    mock_send_to_receiver = mocker.patch(
        'src.bluecurrent_api.websocket.Websocket.send_to_receiver',
        create=True,
        side_effect=AsyncMock()
    )

    websocket = Websocket()

    # CHARGE_POINTS flow
    message = {"object": "CHARGE_POINTS"}
    mocker.patch.object(Websocket, '_recv', return_value=message)
    await websocket._message_handler()
    mock_handle_charge_points.assert_called_with(message)
    mock_send_to_receiver.assert_called_with(message)

    # ch_status flow
    message = {"object": "CH_STATUS"}
    mocker.patch.object(Websocket, '_recv', return_value=message)
    await websocket._message_handler()
    mock_handle_status.assert_called_with(message)
    mock_send_to_receiver.assert_called_with(message)

    # grid_status flow
    message = {"object": "GRID_STATUS"}
    mocker.patch.object(Websocket, '_recv', return_value=message)
    await websocket._message_handler()
    mock_handle_grid.assert_called_with(message)
    mock_send_to_receiver.assert_called_with(message)

    # grid_current flow
    message = {"object": "GRID_CURRENT"}
    mocker.patch.object(Websocket, '_recv', return_value=message)
    await websocket._message_handler()
    mock_handle_grid.assert_called_with(message)
    mock_send_to_receiver.assert_called_with(message)


    # ch_settings flow
    message = {"object": "CH_SETTINGS"}
    mocker.patch.object(Websocket, '_recv', return_value=message)
    await websocket._message_handler()
    mock_handle_settings.assert_called_with(message)
    mock_send_to_receiver.assert_called_with(message)

    # setting change flow
    message = {"object": "STATUS_SET_PLUG_AND_CHARGE"}
    mocker.patch.object(Websocket, '_recv', return_value=message)
    await websocket._message_handler()
    mock_handle_setting_change.assert_called_with(message)
    mock_send_to_receiver.assert_called_with(message)

    # session message flow
    message = {"object": "STATUS_STOP_SESSION"}
    mocker.patch.object(Websocket, '_recv', return_value=message)
    await websocket._message_handler()
    mock_handle_handle_session_messages.assert_called_with(message)
    mock_send_to_receiver.assert_called_with(message)

    mock_get_dummy_message = mocker.patch(
        'src.bluecurrent_api.websocket.get_dummy_message')

    # STATUS_START_SESSION
    message = {"object": "STATUS_START_SESSION", 'evse_id': 'BCU101'}
    mocker.patch.object(Websocket, '_recv', return_value=message)
    await websocket._message_handler()
    mock_handle_handle_session_messages.assert_called_with(message)
    mock_get_dummy_message.assert_called_with('BCU101')

    # no object
    message = {"value": True}
    mocker.patch.object(Websocket, '_recv', return_value=message)
    with pytest.raises(WebsocketError):
        await websocket._message_handler()

    # unknown command
    message = {"error": 0, "object": "ERROR", "message": "Unknown command"}
    mocker.patch.object(Websocket, '_recv', return_value=message)
    with pytest.raises(WebsocketError):
        await websocket._message_handler()

    # unknown token
    message = {"error": 1, "object": "ERROR", "message": "Invalid Auth Token"}
    mocker.patch.object(Websocket, '_recv', return_value=message)
    with pytest.raises(WebsocketError):
        await websocket._message_handler()

    # token not autorized
    message = {"error": 2, "object": "ERROR", "message": "Not authorized"}
    mocker.patch.object(Websocket, '_recv', return_value=message)
    with pytest.raises(WebsocketError):
        await websocket._message_handler()

    # unknown error
    message = {"error": 9, "object": "ERROR", "message": "Unknown error"}
    mocker.patch.object(Websocket, '_recv', return_value=message)
    with pytest.raises(WebsocketError):
        await websocket._message_handler()

    # limit reached
    message = {"error": 42, "object": "ERROR",
               "message": "Request limit reached"}
    mocker.patch.object(Websocket, '_recv', return_value=message)
    with pytest.raises(RequestLimitReached):
        await websocket._message_handler()

    # success false
    message = {"success": False, "error": "this is an error"}
    mocker.patch.object(Websocket, '_recv', return_value=message)
    with pytest.raises(WebsocketError):
        await websocket._message_handler()

    # None message
    message = None
    mocker.patch.object(Websocket, '_recv', return_value=message)
    assert await websocket._message_handler() == True

    # Ignore status
    message = {"object": "STATUS"}
    mocker.patch.object(Websocket, '_recv', return_value=message)
    assert await websocket._message_handler() == False

    # RECEIVED without error
    message = {'object': "RECEIVED_START_SESSION", 'error': ''}
    mocker.patch.object(Websocket, '_recv', return_value=message)
    assert await websocket._message_handler() == False


@pytest.mark.asyncio
async def test_send_to_receiver(mocker: MockerFixture):
    websocket = Websocket()

    mock_receiver = mocker.MagicMock()
    websocket.receiver = mock_receiver
    websocket.receiver_is_coroutine = False

    await websocket.send_to_receiver('test')

    mock_receiver.assert_called_with('test')

    async_mock_receiver = AsyncMock()
    websocket.receiver = async_mock_receiver
    websocket.receiver_is_coroutine = True

    await websocket.send_to_receiver('test')
    async_mock_receiver.assert_called_with('test')


@pytest.mark.asyncio
async def test_disconnect(mocker: MockerFixture):
    websocket = Websocket()
    mocker.patch.object(Websocket, '_connection')
    mocker.patch.object(Websocket, '_check_connection')
    mocker.patch.object(Websocket, 'handle_receive_event')

    test_close = mocker.patch(
        'src.bluecurrent_api.websocket.Websocket._connection.close',
        create=True,
        side_effect=AsyncMock()
    )

    with pytest.raises(WebsocketError):
        await websocket.disconnect()

    websocket._has_connection = True
    await websocket.disconnect()
    assert websocket._has_connection == False
    test_close.assert_called_once()


@pytest.mark.asyncio
async def test_handle_connection_errors(mocker: MockerFixture):
    test_handle_receive_event = mocker.patch.object(
        Websocket, 'handle_receive_event')

    mocker.patch.object(
        Websocket, 'check_for_server_reject')

    websocket = Websocket()

    websocket._has_connection = True
    websocket.receive_event = asyncio.Event()

    with pytest.raises(WebsocketError):
        websocket.handle_connection_errors(None)

    assert websocket._has_connection == False
    test_handle_receive_event.assert_called_once()


@pytest.mark.asyncio
async def test_handle_receive_event():
    websocket = Websocket()

    websocket.receive_event = asyncio.Event()
    websocket.handle_receive_event()
    assert websocket.receive_event.is_set()


def test_check_for_server_reject():
    websocket = Websocket()

    with pytest.raises(RequestLimitReached):
        websocket.check_for_server_reject(InvalidStatusCode(
            403, {'x-websocket-reject-reason': 'Request limit reached'}))

    with pytest.raises(RequestLimitReached):
        websocket.check_for_server_reject(
            ConnectionClosedError(Close(4001, "Request limit reached"), None, None))

    with pytest.raises(AlreadyConnected):
        websocket.check_for_server_reject(InvalidStatusCode(
            403, {'x-websocket-reject-reason': 'Already connected'}))
