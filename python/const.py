from credentials import Credentials

class Api():
    get_device_url = "https://openapi.api.govee.com/router/api/v1/user/devices"
    get_device_state_url = "https://openapi.api.govee.com/router/api/v1/device/state"
    control_device_url = "https://openapi.api.govee.com/router/api/v1/device/control"

    headers = {
        "Content-Type": "application/json",
        "Govee-API-Key": Credentials.api_key 
    }

class Capabilities:
    light_switch = {
        'type':'devices.capabilities.on_off',
        'instance':'powerSwitch'
    }