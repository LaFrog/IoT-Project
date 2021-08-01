# Monitoring Temperature, Humidity and Soil Moisture of a plant in a Greenhouse. 
#### By Michael Ågren (ma226en)

## Summary
With help by this tutorial, you can create your own monitoring system. It can be installed anywhere where you want to see how your plants are having it. It is built to read Temperature and Humidity in the environment it is installed, and it also have a Soil Moisture sensor for one plant.


Estimated time: **~10-15 hours**


## Objective
The initiative for this project was to monitor a newly built greenhouse in my garden. There was a need to remotely control the watering of the plants in the greenhouse. The aim was to build something that measure the state of the plants and decide if turning on and off the automatic watering based on that.
The insight this give is that the technical part of the project is quite easy and straight forward but the algorithms for turning on and of the watering needs completely different skills. This means that the automated triggering of the water valve is not implemented.
But still, you can see how the greenhouse and the plants are having it and then manually start the automatic watering remotely with for example "Home Assistant" (but that is moved to another project).  

## Bill of Material
This is a list of what components that are used in this project.

- **Microcontroller**
Pycom LoPy4 is used because it is easy to configure and program with MicroPython. It also works with a lot of networks (LoRa, Sigfox, Wi-Fi, Bluetooth). Where I live there are no coverage for Sigfox and Lora. Fortunately the greenhouse is in the Wi-Fi-coverage.
Price: [€38.45](https://pycom.io/product/lopy4/)
- **Expansion Board**
Pycom Expansion Board 3.0
The expansion board is used for simplifying the connections from the controller to the sensors.
Price: [€17.60](https://pycom.io/product/expansion-board-3-0/)
- **Digital temperature and humidity sensor DHT11**
DHT11 is used because it is cheap and easy to implement and it give good enough quality of the measurements. And it is two sensors in one unit which is good in this project.
Price: [€5.24](https://www.electrokit.com/produkt/digital-temperatur-och-fuktsensor-dht11/)
- **Soil Moisture sensor FC-28**
This sensor is cheap and works okay for now. The quality of the measurements isn't as good as for the more expensive ones. It also has a short "time to live" according to other users but it will work during one greenhouse season, I presume, and that is good enough.
Price: [€3.10](https://www.electrokit.com/en/product/soil-hygrometer-module/)
- **Breadboard 170 hole**
You need something to connect all the sensors and wires in.
Price: [€3.53](https://www.electrokit.com/en/product/breadboard-170-hole/)
- **Jumper wires**
Whatever wires will do and this kit should be enough, I complemented with some longer ones that I already had. 
Price: [€3.53](https://www.electrokit.com/en/product/test-wires-100mm-m-m-30pcs/

**Total Cost: €71.45 (plus shipping costs)**

This is all material you need to fulfil the purpose with this tutorial.
I have complemented the project with a couple of components to make it live in a standalone environment, the greenhouse - pretty much outside conditions, with no electricity.
I also soldered a longer "signal cable" from the breadboard to the soil moisture sensor to be able to switch plant to measure in the greenhouse.

### Optional components
- **Case**
This is not necessary but nice to have especially when it is in a greenhouse. I used one case that I already had. This one from Clas Ohlson is just an example.
Price: [~€7.00](https://www.clasohlson.com/se/Kopplingsl&aring;da,-extra-h&ouml;g-IP66/p/36-5408)
- **Power bank**
I used one that I already had. It is important that it is big enough or can deliver power at the same time as it is being charged from the solar panel.
Price (estimated): ~€20.00
- **Solar cell charger**
Again, I used one that I already had, this one from Clas Ohlson is just an example.
Price: [~€50.00](https://www.clasohlson.com/se/Kopplingsl&aring;da,-extra-h&ouml;g-IP66/p/36-5408)

**Estimated Optional Cost: ~€77 (plus eventual shipping costs)**

## Computer Setup
I had no experience with this kind of IDE's so I choosed to use VSCode (Visual Studio Code) because I'm using Visual Studio C# in my daytime work. I hoped that there should be some advantages by that, but I don't think there are any. I believe I could have chosen Atom as well. 
This project is done with a computer with Windows 10, so all links are referring to the Windows 10 environment. 

#### Follow these steps to complete the hardware setup [(acc. to Pycom)](https://docs.pycom.io/gettingstarted/#step-1-setting-up-the-hardware):
* Insert the controller into the expansion board
* Connect the expansion board to the computer with an USB data cable (not a charger cable)

#### Installing software on the computer
- If you need Windows drivers, you can get them with installation instructions at [pycom](https://docs.pycom.io/gettingstarted/software/drivers/#windows)
- Pymakr requires that you download [Node.js](https://nodejs.org/en/) and follow the instructions in the installer. 
- Download and install [VSCode](https://code.visualstudio.com/) according to the instructions in the installer.
- Start VSCode and goto extensions. Search for, and install the Pymakr plugin

![](https://i.imgur.com/uq49ScF.png)

- Download the [“Pycom Firmware Update tool"](https://software.pycom.io/findupgrade?product=pycom-firmware-updater&type=all&platform=win32&redirect=true)
- Update the firmware on the Controller and the Expansion Board [acc. to Pycom](https://docs.pycom.io/updatefirmware/device/)

#### Uploading code
- Create your first project to see if everything is working.
    * Create a file in VSCode in an empty folder and name it "main.py"
    * Insert the following code: 
    ```micropython=1
    import pycom # "pycom" will be an error in your
    # IDE because it's not on your computer, but on 
    # the device
    import time

    pycom.heartbeat(False)

    while True: #Forever loop
    pycom.rgbled(0xFF0000)  # Red
    time.sleep(1) #sleep for 1 second

    pycom.rgbled(0xFF3300)  # Orange
    time.sleep_ms(1000) #sleep for 1000 ms

    pycom.rgbled(0x00FF00)  # Green
    time.sleep(1)
    ```
    * Press upload in the bottom of the VSCode IDE.
    * After a while the LED on the controller will start blinking if everything is okay.

## Putting everything together

Now when you know that your device and your programming environment is working it's time to start building the electronics.

First, I started with a test-rig where I tested the sensors and calibrated the moisture sensor.

![](https://i.imgur.com/PFumEgt.jpg) ![](https://i.imgur.com/iOxMB7a.jpg) ![](https://i.imgur.com/6NmXIRf.jpg) ![](https://i.imgur.com/xjmUkRg.jpg)

I did four tests with ten measurements (used the MQTT-Explorer):
1. Empty pot, average  value = 4095
2. Only water, average  value = 0
3. Dry soil, average  value = 3801 
4. Wet soil, average  value = 1077

These measurements I will use in the programming later.

The final electrical solution:

![](https://i.imgur.com/qs1Kdze.png)

## Platform
This project landed in using the cloud-based [Ubidots STEM platform](https://ubidots.com/stem/).
I tried Pybytes and it works okay but I wanted to go for my own installation of Grafana. Before implementing Grafana I tried Ubidots and found that it was very easy to setup, and good enough, so I stayed there.
Ubidots is easy to use and the result looks quite okay, you find a [guide here](https://help.ubidots.com/en/articles/961994-connect-any-pycom-board-to-ubidots-using-wi-fi-over-http) to setup and send data. You have to [sign up on Ubidots](https://industrial.ubidots.com/accounts/signup_industrial/) and create your free account. In the free account you are only aloud to upload 4000 dots (datapoint containing a value and a timestamp) a day. 
I started with uploading every 10 seconds and I ran out of upload quota for a day after a couple of hours. Now it's uploading every five minutes, probably to often for a greenhouse, and it seems to not reach the aloud quota.
The project is prepared for sending to a MQTT-broker as I intended to go for Grafana and my own MQTT-broker. Now it's sending to Fredrik's "mqtt.iotlab.dev" and can be changed easily.

## The Code and Configuration files
You can download the full codebase directly from GitHub: https://github.com/LaFrog/IoT-Project

This code snippet is responsible for getting the sensor data and sending it to Ubidots and the MQTT-broker respectively.
The comments in the code explain what it does.
```MicroPython=1
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

```
I have separated the sensor reading from the main code into separate modules.
This one is for reading "Temperature" and "Humidity".
The pin 'P23' is defined for getting the data from the sensor.

```MicroPython=1
from dht import DHT
from machine import Pin
import time

def value():
    th = DHT(Pin('P23', mode=Pin.OPEN_DRAIN), 0)
    time.sleep(3)
    result = th.read()
    if result.is_valid():
        return(result.temperature,result.humidity)
```
This module handles the reading of the moisture sensor.
I'm using the empirical calibration values for dry and wet soil I got from the test-rig (row 6 and 8. 
I'm defining pin 'P15' for data and pin 'P12' for VCC in the function - value() starting at row 22.
In the same function, at row 27, I read the sensor value with a call to the function moist_sensor().
Then I calculate the moisture in percent with the logic:
X = 100 - (analogValue - WetValue ) / (DryValue - WetValue) * 100 
The sensor value is per my definition (if it's in soil) between the dry and the wet calibrated values. I take the sensor value and subtract the wet value (which is the lowest value) and then divide it with the measuring range. That multiplied with 100 give the persentige. But as the gauge goes from 0-100 and the measure range goes from higher to lower value I have to subtract it from 100 to get the correct value to send.  

```MicroPython=1
from machine import Pin
from machine import ADC
import time

# empirical value dry soil
DIRT_DRY = 3801
# empirical value wet soil
DIRT_WET = 1077

def moist_sensor(p_in, p_out):
    adc = ADC() 
    apin = adc.channel(pin=p_in, attn=ADC.ATTN_11DB)
    p_out = Pin(p_out, mode=Pin.OUT, pull=Pin.PULL_DOWN)
    p_out.value(1)
    time.sleep(2)
    analogValue = apin.value()
    p_out.value(0)
    time.sleep(2)
    
    return analogValue

def value():
    ao = "P15"
    vcc = "P12"
    set = Pin(ao, mode=Pin.IN)
    
    analogValue = moist_sensor(ao, vcc)
    # X = 100 - (analogValue-Wet)/(Dry-Wet)*100
    moisture = 100 - ((analogValue - DIRT_WET) / (DIRT_DRY-DIRT_WET)) * 100

    return moisture
```

All settings are stored in JSON-format in the file config.json. There are my wifi credentials and other connection data stored. My intention was to update the settings file with Telnet or FTP but I haven't succeeded with that yet.  

```JSON   
{
  "wifi": {
            "ssid": "XXXXXXX",
            "ssid_pass": "ZZZZZZZ"
          },

  "mqtt": {
            "user_mqtt": "XXXXXXX",
            "pass_mqtt": "ZZZZZZZ",
            "topic_pub": "devices/ekstocken-sens/",
            "topic_sub": "devices/ekstocken-sens/control",
            "broker_url": "mqtt.iotlab.dev"
          },

  "ubidots": {
            "useUbidots": "TRUE",
            "TOKEN": "XXXX-ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ"
          },

  "upload": {
            "uploadDelayInSeconds" : 300
          }
  }
```


## Transmitting the data
For this project I use Wi-Fi for sending data to internet and that is mostly for the reason that I don't have coverage for other networks where the greenhouse is located. I send both to Ubidots and a MQTT-broker every five minutes.
I'm sending directly to Ubidots with this piece of code. It creates a JSON-formatted string (row 5-15) with REST-API (row 18-20).
```MicroPython=1
# Ubidots TOKEN
TOKEN = config['ubidots']["TOKEN"]

# Builds the json to send the Ubidots request
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

# Sends the request. Please reference the REST API reference https://ubidots.com/docs/api/def post_var(device, greenhouseTemp, greenhouseHumidity, greenhousMoisture, position):
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
        
post_var("pycom", greenhouseTemp, greenhouseHumidity, greenhousMoisture, 1)
```
I also send to a MQTT broker to be able to set up my own Grafana (TBD). The connection data is defined (row 2-11) and then the publishing to the MQTT-broker is done (row 14)
```MicroPython=1
# Setting up the MQTT-connection
topic_pub = config['mqtt']["topic_pub"]
topic_sub = config['mqtt']["topic_sub"]
broker_url = config['mqtt']["broker_url"]
client_name = ubinascii.hexlify(hashlib.md5(machine.unique_id()).digest()) # create a md5 hash of the pycom WLAN mac

print("Client Name: ", client_name)

c = MQTTClient(client_name,broker_url)
c.connect()
c.subscribe(topic_sub)

# send to MQTT
c.publish(topic_pub,'{"Greenhouse_sensors": {"dht temp":' + str(dht_T) + ',"dht RH":' + str(dht_RH) + ',"Soil Moisture Value":' + str(moisture) + '}')
print('Sensor data sent to MQTT..')
```

## Presenting the data 
On Ubidots the dashboards are easy and intuitive to build and can be done directly in the dashboard interface. I have chosen to have gauges for the measurements that shows the last sending. I also have a line char showing the data for a certain interval to show as a curve. There is also a value table for the last ten last sent data.

![](https://i.imgur.com/b41LWC3.jpg)

The MQTT data can be visualized with a "MQTT-Explorer". This picture showing an app from Windows Store where the last sent data and is also compared with the former data if it has changed.

![](https://i.imgur.com/IXQMUHh.jpg)

## Finalizing the design
Now, I'm satisfied with the final result. And I am because of I revised the goal a couple of times during the project.
My initial goal was to set up more applications by my own, like Grafana (or similar) and a MQTT-broker. When I realized that i didn't had coverage for the LoraWan I thought i should set up my on gateway. I also wanted to connect the monitoring system with my, not yet built at that time, automatic watering system. I had to start with the watering system because I'm going for a two-week vacation and my plants will need water. The automatic watering system is built on Ikea's "Knycklan" (ZigBee) connected to "HomeAssistant" and is controllable via an app in my cell phone. Probably I will use "NodeRed" for that integration, but this has to be version 2.0 of this project. 
The reason for not implementing the "Knycklan" integrations depends on first, to short time left to run the monitoring system to get enough real data for analysing. And second, to little skills in gardening for building the algorithms  for starting and stopping the automatic watering.
As a software developer I should have known that this kind of project occupies more time than you first expect. 
With that in mind I should have built the watering system before this project. 
I should have bought two settings of controllers. One for the final project and one for testing and learning. With only one I couldn't start building my project until all testing and learning was done.

### Some pictures of the installation
The greenhouse with the equipment installed. You can see the grey box in the lower left corner.
![](https://i.imgur.com/UtR3NV0.jpg)

The actual plant where the moisture is monitored.
![](https://i.imgur.com/gOUI8ZL.jpg)

The "base station" of the monitoring system behind a pot of carrots.
![](https://i.imgur.com/tHZFhQH.jpg)

The moisture sensor in one pot. I have dug it down five centimetres to get it to measure deeper in the soil - just a theory of mine that it is better.
![](https://i.imgur.com/nDAqWpF.jpg)

The carrot pot removed for viewing the base station with the solar panel exposed to the sun.
![](https://i.imgur.com/Y60O1is.jpg)

Th base station on the work bench for a service and an upload with new code. The moisture cable is still in the pot. 
![](https://i.imgur.com/whDD4m9.jpg)

















