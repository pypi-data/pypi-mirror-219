# Blue Current Api

[![Documentation Status](https://readthedocs.com/projects/blue-current-homeassistantapi/badge/?version=latest&token=00ce4a850aedc0993b7075a8b2d5f8de98251adcdb4eada1f1fb3c02fee80039)](https://blue-current-homeassistantapi.readthedocs-hosted.com/en/latest/?badge=latest)

Python wrapper for the blue current api

The library is an asyncio-driven library that interfaces with the Websocket API provided by Blue Current. This was made for the Blue Current Home Assistant integration.

## Usage

### Requirements

- Python 3.9 or newer
- websockets
- asyncio

### Installation

```python
pip install bluecurrent-api
```

### Api token

Using this library requires a Blue Current api token. You can generate one in the Blue Current driver portal.

## Example

```python
from bluecurrent_api import Client
import asyncio


async def main():
    api_token = 'api_token'
    client = Client()

    # data receiver
    def on_data(data):
        print('received: ', data)

    # connect to the websocket
    await client.connect(api_token)

    # example requests
    async def requests():
        await client.get_charge_points()
        await client.wait_for_response()
        await client.disconnect()

    # start the loop and send requests
    await asyncio.gather(
        client.start_loop(on_data),
        requests()
    )

asyncio.run(main())
```

## Implemented methods

---

<b>The methods validate_token, get_account and get_charge_cards are stand-alone and to be used <u>before</u> connecting to the websocket with connect().</b>

<br>

#### await validate_token(api_token) -> bool

- Validates the given token.

#### await get_account() -> bool

- Returns the account's email.

#### await get_charge_cards(auth_token) -> list

- Returns the users charge cards.

---

#### await connect(auth_token)

- Connects to the websocket.

#### await start_loop(receiver)

- Starts the loop and routes the incoming messages to the given receiver method

#### await wait_for_response()

- Waits until the next message is received.

#### get_next_reset_delta()

- Returns the timedelta to the next request limit reset (00:00 Europe/Amsterdam).

#### await disconnect()

- Stops the connection.

<br>

### Data

---

#### await get_charge_points()

- Gets the chargepoints

#### await get_status(evse_id)

- Gets the status from a chargepoint.

#### await get_settings(evse_id)

- Gets the setting states from a chargepoint.

#### await get_grid_status(evse_id)

- Gets the grid status from a chargepoint.

<br>

### Settings

---

#### await set_public_charging(evse_id, value)

- Sets public charging to True or False.

#### await set_plug_and_charge(evse_id, value)

- Sets plug and charge to True or False.

#### await set_operative(evse_id, value)

- Sets operative to True or False.

<br>

### Actions

---

#### await reset(evse_id)

- Resets the chargepoint.

#### await reboot(evse_id)

- Reboots the chargepoint.

#### await start_session(evse_id card_uid)

- Starts a charge session.

#### await stop_session(evse_id)

- Stops a charge session.
