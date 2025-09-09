import network
import time
import dht
from machine import Pin
import urequests
import json

dht_sensor = dht.DHT11(Pin(5))
led = Pin(8, Pin.OUT)

current_state = ""
last_temp = ""


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to network")
        wlan.connect(WIFI_SSID, WIFI_PASS)
        while not wlan.isconnected():
            time.sleep(1)
    print("IP:", wlan.ifconfig()[0])


def control_switch(state):
    service = "turn_on" if state else "turn_off"
    url = f"{HA_URL:}/services/switch/{service}"
    data = {"entity_id": ENTITY_ID}

    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json",
    }
    try:
        response = urequests.post(url, json=data, headers=headers)
        print(
            f"Response status: {response.status_code}, Response text: {response.text}"
        )
        response.close()

        if response.status_code == 200:
            current_state = state
            print(f"Switch switched to: {state}")
        else:
            print(f"Request failed with status: {response.status_code}")
            response.close()
    except Exception as e:
        print("Switch connection error", e)


def read_sensor():
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()
        return temp, hum
    except Exception as e:
        print("DHT sensor read error", e)
        return None, None


def send_sensor_data(temp, hum):
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json",
        "Connection": "close",
    }
    temp_data = {
        "state": temp,
        "attributes": {
            "unit_of_measurement": "",
            "device_class": "temperature",
            "friendly_name": "ESP32 Temperatura",
        },
    }

    try:
        response = urequests.post(
            f"{HA_URL}/states/{TEMP_SENSOR}", json=temp_data, headers=headers
        )
        print(f"Temp Response: {response.status_code}")
        response.close()
    except Exception as e:
        print("Switch connection error", e)

    hum_data = {
        "state": hum,
        "attributes": {
            "unit_of_measurement": "%",
            "friendly_name": "ESP32 humidity",
            "device_class": "humidity",
        },
    }

    try:
        response = urequests.post(
            f"{HA_URL}/states/{HUM_SENSOR}", json=hum_data, headers=headers
        )
        response.close()
    except Exception as e:
        print("Humidity sensor send error", e)


connect_wifi()

while True:
    temp, hum = read_sensor()
    print(temp, hum)

    if temp is not None and hum is not None:
        print(f"Temp: {temp}°C, Humidity: {hum}%")
        led.value(not led.value())

        send_sensor_data(temp, hum)
        print(
            f"Temp: {temp}, Current state: {current_state}, Action needed: {temp <= 24 and not current_state}"
        )
        if temp >= 26 and current_state != False:
            control_switch(True)
        elif temp <= 24 and not current_state != True:
            control_switch(True)

    time.sleep(1)
