# IoT Project - Monitoring Temperature and Humidity in a Greenhouse and also the soil moisture of one plant. 
#### By Michael Ågren

## Summary

With help by this tutorial you can create your own monitoring system. It can be installed anywhere where you want see how your plants have it. The initiative for this project was to monitoring a newly built greenhouse in my garden. 

Estimated time: **~XX hours**

Estimated price: **~XX$**

## Objective


## Bill of Material

This is a list of what components that are used in this project.

- **Microcontroller**
Pycom LoPy4 is used because of it is easy to configure and program with MicroPython. It also works with a lot of networks (LoRa, Sigfox, WiFi, Bluetooth). Where I live there are no coverage for Sigfox and Lora. Fortunally the greenhouse is in the WiFi-coverage.
Price: [€38.45](https://pycom.io/product/lopy4/)
- **Expansion Board**
Pycom Expansion Board 3.0
The expansion board is used for simplified the connections from the controller to the sensors.
Price: [€17.60](https://pycom.io/product/expansion-board-3-0/)
- **Digital temperature and humidity sensor DHT11**
DHT11 is used because of it is cheap an easy to implement and it give good enough quality of the measurements. And it is two sensors in one unit which is good in this project.
Price: [€5.24](https://www.electrokit.com/produkt/digital-temperatur-och-fuktsensor-dht11/)
- **Soil hygrometer module**
This sensor is cheap and works okay for now. The quality of the measurements isn't as good as for the more expensive ones. It also have a short "time to live" according to other users but it will work during one greenhous season I presume and that is good enough.
Price: [€3.10](https://www.electrokit.com/en/product/soil-hygrometer-module/)
- **Breadboard 170 hole**
You need something to connect all the sensors and wires in.
Price: [€3.53](https://www.electrokit.com/en/product/breadboard-170-hole/)
- **Jumper wires**
What ever wires will do and this kit should be enough, I complemented with some longer ones that I already have. 
Price: [€3.53](https://www.electrokit.com/en/product/test-wires-100mm-m-m-30pcs/

**Total Cost: €71.45 (plus shipping costs)**

This is all material you need to fulfil the purpose with this tutorial.
I have complemented the project with a couple of components to make it live in an standalone environment, the greenhouse - pretty much outside conditions, with no electricity.
I also soldered a longer "signal cable" from the breadboard to the soil hygrometer sensor to be able to switch plant to measure in the greenhouse.

### Optional components
- **Case**
This is not nessecary but nice to have especially when it is in a greenhouse. I used one case that I already had. This one from Clas Ohlson is just an example.
Price: [~€7.00](https://www.clasohlson.com/se/Kopplingsl&aring;da,-extra-h&ouml;g-IP66/p/36-5408)
- **Powerbank**
I used one that I already had, this one from Clas Ohlson is just an example. It is important that it can deliver power at the same time as it is beeing charged.
Price: [~€20.00](https://www.clasohlson.com/se/Kopplingsl&aring;da,-extra-h&ouml;g-IP66/p/36-5408)
- **Solar cell charger**
Again, I used one that I already had, this one from Clas Ohlson is just an example.
Price: [~€50.00](https://www.clasohlson.com/se/Kopplingsl&aring;da,-extra-h&ouml;g-IP66/p/36-5408)

**Estimated Optional Cost: ~€77 (plus eventual shipping costs)**

## Computer Setup
*How is the device programmed. Which IDE are you using. Describe all steps from flashing the firmware, installing plugins in your favorite editor. How flashing is done on MicroPython. The aim is that a beginner should be able to understand.*

*- Chosen IDE*
*- How the code is uploaded*
*- Steps that you needed to do for your computer.* 
*- Installation of Node.js, extra drivers, etc.*

I had no experience with this kind of IDE's so I choosed to use VSCode (Visual Studio Code) because I'm using Visual Studio C# in my daytime work. I hoped that there should be some advantages by that but I don't think there are any. I could have choosen Atom as well I think. 
This project is done with a computer with Windows 10 so all links are referring to the Windows 10 environment. 

#### Follow these steps to complete the hardware setup [(acc. to Pycom)](https://docs.pycom.io/gettingstarted/#step-1-setting-up-the-hardware):
* Insert the controller into the expansion board
* Connect the expansion board to the computer with an USB data cable (not a charger cable)

#### Installing software on the computer
- If you need Windows drivers you can get them [here](https://docs.pycom.io/gettingstarted/software/drivers/#windows)
- Pymakr requires that you install [Node.js](https://nodejs.org/en/) 
- Download and install [VSCode](https://code.visualstudio.com/)
- Install the [Pymakr plugin]() in VSCode
- Update the firmware on the Controller and the Expansion Board ([acc. to Pycom](https://docs.pycom.io/updatefirmware/device/))
- Download the [“Pycom Firmware Update tool"](https://software.pycom.io/findupgrade?product=pycom-firmware-updater&type=all&platform=win32&redirect=true) 
- Install the update.

#### Uploading code
- Create your first project to se if every thing is working.
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
*How is all the electronics connected? Describe all the wiring, good if you can show a circuit diagram. Be specific on how to connect everything, and what to think of in terms of resistors, current and voltage. Is this only for a development setup or could it be used in production?*

*- Circuit diagram (can be hand drawn)*
*- Electrical calculations*

Now when you know that your device and your programming environment is working it's time to start building the electronics.

First I started with a test-rig where I tested the sensors and calibrated the moisure sensor.

![](https://i.imgur.com/PFumEgt.jpg) ![](https://i.imgur.com/iOxMB7a.jpg) ![](https://i.imgur.com/6NmXIRf.jpg) ![](https://i.imgur.com/xjmUkRg.jpg)

I did four tests with ten measurements (used the MQTT-Explorer):
1. Empty pot, avarage value = 4095
2. Only water, avarage value = 0
3. Dry soil, avarage value = 3801 
4. Wet soil, avarage value = 1077

Theese measurements I will use in the programming later.

The final electrical solution 








## Platform
*Describe your choice of platform. If you have tried different platforms it can be good to provide a comparison.*

*Is your platform based on a local installation or a cloud? Do you plan to use a paid subscription or a free? Describe the different alternatives on going forward if you want to scale your idea.*

*- Describe platform in terms of functionality*
*- Explain and elaborate what made you choose this platform*

This project landed in using the cloud-based [Ubidots STEM platform](https://ubidots.com/stem/).
I tried Pybytes and it works okay but I wanted to go for my own installation of Grafana. Before implementing Grafana I tried Ubidots and find that very easy and good enough so I stayed there.
Ubidots is easy to use and the result looks quite okay, you find a [guide here](https://help.ubidots.com/en/articles/961994-connect-any-pycom-board-to-ubidots-using-wi-fi-over-http) to setup and send data. You have to [sign up on Ubidots](https://industrial.ubidots.com/accounts/signup_industrial/) and create your free account. In the free account you are only aloud to upload 4000 dots (datapoint containing a value and a timestamp) a day. 
I started with uploading every 10 seconds and I ran out of upload quota for a day after a couple of hours. Now it's uploading every five minutes, probably to often for a greenhouse, and it seems to not reach the aloud quota.
The project i prepared for sending to a MQTT-broker as I intended to go for Grafana and my own MQTT-broker. Now it's sending to Fredriks "mqtt.iotlab.dev" and can be changed easily.

## The Code and Configuration files
*Import core functions of your code here, and don’t forget to explain what you have done! Do not put too much code here, focus on the core functionalities. Have you done a specific function that does a calculation, or are you using clever function for sending data on two networks? Or, are you checking if the value is reasonable etc. Explain what you have done, including the setup of the network, wireless, libraries and all that is needed to understand.*

You can download the full codebase directly from GitHub: https://github.com/LaFrog/IoT-Greenhouse-Monitoring

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
I have separating the sensor reading from the main code into separate modules.
This one is for reading "Temperature" and "Humidity".
The pin 'P23' is defined getting the data from the sensor.

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
This module handle the reading of the moisture sensor.
I'm using the empirical calibration values for dry and wet soil I got from the test-rig (row 6 and 8. 
I'm defining pin 'P15' for data and pin 'P12' for VCC in the function - value() starting at row 22.
In the same function,  at row 27, I read the sensor value with a call to the function moist_sensor().
Then I calculate the moisture in persent with the logic:
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
*How is the data transmitted to the internet or local server? Describe the package format. All the different steps that are needed in getting the data to your end-point. Explain both the code and choice of wireless protocols.*

*- How often is the data sent?*
*- Which wireless protocols did you use (WiFi, LoRa, etc …)?*
*- Which transport protocols were used (MQTT, webhook, etc …)*
*- Elaborate on the design choices regarding data transmission and wireless protocols. That is how your choices affect the device range and battery consumption.*

For this project I use WiFi for sending data to internet and that is mostly for the reason that I don't have coverage for other networks where the greenhouse is located. I send both to Ubidots and a MQTT-broker every five minutes.
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
*Describe the presentation part. How is the dashboard built? How long is the data preserved in the database?*

*- Provide visual examples on how the dashboard looks. Pictures needed.*
*- How often is data saved in the database.*
*- Explain your choice of database.*
*- Automation/triggers of the data.*

On Ubidots the dashboard's are easy and intuitive to build and can be done directly in the dashboard interface. I have choosen to have gauges for the measurements that shows the last sending. I also have a line char showing the data for a certain interval to show as a curve. There is also a value table for the last ten last sent data.

![](https://i.imgur.com/b41LWC3.jpg)

The MQTT data can be visualized with a "MQTT-Explorer". This picture showing an app from Windows Store where the last sent data and is also compared with the former data if it has changed.

![](https://i.imgur.com/IXQMUHh.jpg)

## Finalizing the design
*Show the final results of your project. Give your final thoughts on how you think the project went. What could have been done in an other way, or even better? Pictures are nice!*

*- Show final results of the project*
*- Pictures*
*- Video presentation*

Now I'm satisfied with the final result. I am because of I revised the goal a couple of times during the project.
My inital goal was to set up more applications by my own, like Grafana (or similar) and a MQTT-broker. When I realized that i didn't had coverage for the LoraWan I thougt i should set up my on gateway. I also wanted to connect the monitoring system with my, not yet built at that time, automatic watering system. I had to start with the watering system because I'm going for a two week vacation and my plants needs water. The automatic watering system is built on Ikea's "Knycklan" (ZigBee) connected to "HomeAssistant" and is controllable via an app in my phone. Maybe "NodeRed" can do the integration, but that is a compleatly different project.
The reason for my lack of time is mainly due to more work in the real world then expected.
As an developer I should have known that this kind of project occupies more time than you first expect. 
With that in mind I should have built the watering system before this project. 
I should have bought two settings of controllers. One for the final project and one for testing and learning. With only one I couldn't start building my project until all testing and learning was done.

### Some pictures of the installation
The greenhouse with the equipment installed. You can see the grey box in the lower left corner.
![](https://i.imgur.com/UtR3NV0.jpg)

The actual plant where the moisture is monitored.
![](https://i.imgur.com/gOUI8ZL.jpg)

The "base station" of the monitoring system behind a pot of carrots (i think).
![](https://i.imgur.com/tHZFhQH.jpg)

The moisture sensor in one pot. I have digged it down five centimeters to get it to measure deeper in the soil - just a theory of mine that it is better.
![](https://i.imgur.com/nDAqWpF.jpg)

The carrot pot removed for viewing the base station with the solar panel exposed to the sun.
![](https://i.imgur.com/Y60O1is.jpg)

Th base station on the work bench for a service and an upload with new code. The moistur cable is still in the pot. 
![](https://i.imgur.com/whDD4m9.jpg)

















