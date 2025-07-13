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

class Phrases:
    phrases = {
        'welcome back':{
            'audio_path':'welcomeback.wav',
            'audio_length':1.5
        },
        'could not understand':{
            'audio_path':'notunderstand.wav',
            'audio_length':1.5
        },
    }
    activation_words = {
        'next':{'skip', 'next'},
        'previous':{'back','previous', 'last'},
        'louder':{'louder','up','increase'},
        'quiter':{'decrease','down', 'lower'},
        'stop':{'stop','pause'},
        'resume':{'resume','continue'}
    }

    playlist_titles = {
        'summer':'Summer House 2025',
        'chill':'lofi beats',
        'main':'my music universe',
        'house':'Tempelhof 60',
        'test':'TestPlaylist'
    }

    
