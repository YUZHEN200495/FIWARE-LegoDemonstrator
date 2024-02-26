from time import sleep
from simulator import Device, ChargerDevice
import paho.mqtt.client as mqtt
from paho.mqtt.client import Client
import json
from typing import Union


def send_data(device_id: str, attr: str, value: Union[int, float, str]):
    topic = f"/idFZy8D9KzFko7db/{device_id}/attrs/{attr}"
    return client.publish(topic, value)

def generate() -> list:
    with open("devices.json", "r") as f:
        devices = json.load(f)

    out = []
    for device in devices:
        out.append(Device(device))
    out.append(ChargerDevice("electricVehicleChargingStation001"))
    out.append(ChargerDevice("electricVehicleChargingStation002"))
    return out

devices = generate()



client = mqtt.Client("Lucca")
client.username_pw_set(
    "LegoDemonstrator",
    "Lego12Demo34nstr56ator"
)
client.connect("mosquitto")

while True:
    for device in devices:
        steps = device.step()
        for step in steps:
            send_data(*step)
    sleep(10)
