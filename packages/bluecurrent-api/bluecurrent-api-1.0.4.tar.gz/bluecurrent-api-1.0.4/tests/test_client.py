from src.bluecurrent_api.client import Client
import pytest
from pytest_mock import MockerFixture


def test_create_request():
    client = Client()
    client.websocket.auth_token = '123'

    # command
    request = client._create_request("GET_CHARGE_POINTS")
    assert request == {'command': 'GET_CHARGE_POINTS'}

    # evse_id
    request = client._create_request("GET_STATUS", '101')
    assert request == {'command': 'GET_STATUS', 'evse_id': '101'}

    # value
    request = client._create_request("SET_PLUG_AND_CHARGE", '101', True)
    assert request == {'command': 'SET_PLUG_AND_CHARGE',
                       'evse_id': '101', 'value': True}

    # card_uid / session_token
    request = client._create_request("START_SESSION", '101', card_uid='1234')
    assert request == {'command': 'START_SESSION',
                       'evse_id': '101', 'session_token': '1234'}


@pytest.mark.asyncio
async def test_requests(mocker: MockerFixture):

    test_send_request = mocker.patch(
        "src.bluecurrent_api.client.Websocket.send_request")
    client = Client()

    await client.get_charge_points()
    test_send_request.assert_called_with(
        {'command': 'GET_CHARGE_POINTS'})

    await client.get_status('101')
    test_send_request.assert_called_with(
        {'command': 'GET_CH_STATUS', 'evse_id': '101'})

    await client.get_settings('101')
    test_send_request.assert_called_with(
        {'command': 'GET_CH_SETTINGS', 'evse_id': '101'})

    await client.get_grid_status('101')
    test_send_request.assert_called_with(
        {'command': 'GET_GRID_STATUS', 'evse_id': '101'})

    await client.set_linked_charge_cards_only('101', True)
    test_send_request.assert_called_with(
        {'command': 'SET_PUBLIC_CHARGING', 'evse_id': '101', 'value': False})

    await client.set_plug_and_charge('101', True)
    test_send_request.assert_called_with(
        {'command': 'SET_PLUG_AND_CHARGE', 'evse_id': '101', 'value': True})

    await client.block('101', False)
    test_send_request.assert_called_with(
        {'command': 'SET_OPERATIVE', 'evse_id': '101'})

    await client.block('101', True)
    test_send_request.assert_called_with(
        {'command': 'SET_INOPERATIVE', 'evse_id': '101'})

    await client.reset('101')
    test_send_request.assert_called_with(
        {'command': 'SOFT_RESET', 'evse_id': '101'})

    await client.reboot('101')
    test_send_request.assert_called_with(
        {'command': 'REBOOT', 'evse_id': '101'})

    await client.start_session('101', '123')
    test_send_request.assert_called_with(
        {'command': 'START_SESSION', 'evse_id': '101', 'session_token': '123'})

    await client.stop_session('101')
    test_send_request.assert_called_with(
        {'command': 'STOP_SESSION', 'evse_id': '101'})
