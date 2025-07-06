from const import Api
import requests


def getdevice(deviceName):
    response = requests.get(Api.get_device_url, headers=Api.headers)
    if response.status_code == 200:
        data = response.json()  
        for devices in data['data']:
            if devices['deviceName']==deviceName:
                return devices
        else:
            return None
    else:
        print(f"Error fetching Info for {deviceName}: {response.status_code}, {response.text}")
