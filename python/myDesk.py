from getAllDevices import getdevice
from const import Api, Capabilities
import requests 


def get_status(instance,sku,device_id):
    payload = {
        "requestId": "uuid",  
        "payload": {
            "sku": sku,
            "device": device_id
        }
    }
    response = requests.post(Api.get_device_state_url,headers=Api.headers,json=payload) 
    if response.status_code == 200:
        data = response.json()
        for capability in data['payload']['capabilities']:
            if capability['instance']==instance:
                return capability['state']['value']

    else:
        print(f"Error: {response.status_code}, {response.text}")

def control_device(sku,device_id,type,instance,value):
    payload = {
        "requestId": "uuid",
        "payload": {
            "sku": sku,
            "device": device_id,
            "capability": {
            "type": type,
            "instance": instance,
            "value": value
            }
        }
    }
    response = requests.post(Api.control_device_url,headers = Api.headers, json=payload)
    print(response.text)


def toggle(deviceName):
    data = getdevice(deviceName)
    if data: 
        sku = data['sku']
        device_id = data['device']
        instance = Capabilities.light_switch['instance']
        type = Capabilities.light_switch['type']
        lights_status = get_status(instance,sku,device_id)
        control_device(sku,device_id,type,instance, (lights_status+1)%2)

toggle("Anhs Tisch")