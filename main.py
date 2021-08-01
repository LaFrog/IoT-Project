import pycom
import _thread
import ubinascii
import hashlib
from network import WLAN
import urequests as requests
import machine
from machine import Pin
import time
from dht import DHT # https://github.com/JurassicPork/DHT_PyCom
from mqtt import MQTTClient

import ujson
# Read config file where all sensitive data are
with open('config.json') as f:
    config = json.load(f)
#
import read_dht
import read_moisture

# Ubidots TOKEN, get from setting
TOKEN = config['ubidots']["TOKEN"]

# Function for building the json to send the Ubidots request
# Use TOKEN from Ubidots
def build_json(variable1, greenhouseTemp, variable2, greenhouseHumidity, variable3, greenhousMoisture, variable4, position):
    try:
        lat = 59.1392
        lng = 12.9553
        data = {variable1: {"value": greenhouseTemp},
                variable2: {"value": greenhouseHumidity},
                variable3: {"value": greenhousMoisture},
                variable4: {"value": position, "context": {"lat": lat, "lng": lng}}}
        return data
    except:
        return None

# Function for sending the request using REST-API to Ubidots. Reference the REST API reference https://ubidots.com/docs/api/
def post_var(device, greenhouseTemp, greenhouseHumidity, greenhousMoisture, position):
    try:
        url = "https://industrial.api.ubidots.com/"
        url = url + "api/v1.6/devices/" + device
        headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
        data = build_json("Temperature", greenhouseTemp, "Humidity", greenhouseHumidity, "Moisture", greenhousMoisture, "Position", position)
        if data is not None:
            print(data)
            req = requests.post(url=url, headers=headers, json=data)
            return req.json()
        else:
            pass
    except:
        pass

# Function for start the sending function after a certain delay
def interval_send(t_):
    while True:
        send_value()
        time.sleep(t_)

# Function for sending data to MQTT and Ubidots 
def send_value():
    try:
        # Read Temperature and Humidity from a sub module
        print("")
        print('Reading Sensors')
        dht_T, dht_RH = read_dht.value()
        print('Temperature:', dht_T)
        print('Humidity:', dht_RH)
        print("")

        # Read Moisture from a sub module      
        moisture = read_moisture.value()
        print('Moisture:', moisture)
        print("")

        # send data to MQTT
        c.publish(topic_pub,'{"Greenhouse_sensors": {"dht temp":' + str(dht_T) + ',"dht RH":' + str(dht_RH) + ',"Soil Moisture Value":' + str(moisture) + '}')
        print('Sensor data sent to MQTT..')

        # Read a setting from config, in case I want to use only Grafana in the end
        useUbidots = config['ubidots']["useUbidots"]
        print("useUbidots: ", useUbidots)
        if (useUbidots == "FALSE"):
            print("Bypassing Ubidots")
        else:
            # If setting is true - send data to Ubidots
            greenhouseTemp = dht_T # Data values
            greenhouseHumidity = dht_RH # Data values
            greenhousMoisture = moisture

            post_var("pycom", greenhouseTemp, greenhouseHumidity, greenhousMoisture, 1)
            print('Sensor data sent to Ubidots..')
        print("")
               
    except (NameError, ValueError, TypeError):
        print('Failed to send!')
        print("")

# Setting up the MQTT-connection
topic_pub = config['mqtt']["topic_pub"]
topic_sub = config['mqtt']["topic_sub"]
broker_url = config['mqtt']["broker_url"]
client_name = ubinascii.hexlify(hashlib.md5(machine.unique_id()).digest()) # create a md5 hash of the pycom WLAN mac

print("Client Name: ", client_name)

c = MQTTClient(client_name,broker_url)
c.connect()
c.subscribe(topic_sub)

# Set upload delay from setting
uploadDelayInSeconds = config['upload']["uploadDelayInSeconds"]

# Start a thread that sending data with an interval
_thread.start_new_thread(interval_send,[uploadDelayInSeconds])
    