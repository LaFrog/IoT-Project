from machine import UART
import machine
import os
from network import WLAN
import json

uart = UART(0, baudrate=115200)
os.dupterm(uart)

machine.main('main.py')

with open('config.json') as f:
    config = json.load(f)


wlan = WLAN() # get current object, without changing the mode
if machine.reset_cause() != machine.SOFT_RESET:
    wlan.init(mode=WLAN.STA)
    # configuration below MUST match your home router settings!!
    wlan.ifconfig(config=('10.250.50.188', '255.255.0.0', '10.250.50.1', '10.250.50.1')) # (ip, subnet_mask, gateway, DNS_server)
    print(wlan.ifconfig(id=1))


wlan = WLAN(mode=WLAN.STA)
wlan.antenna(WLAN.INT_ANT)

# Assign your Wi-Fi credentials
wlan.connect(config["wifi"]["ssid"], auth=(WLAN.WPA2, config["wifi"]["ssid_pass"]), timeout=5000)

while not wlan.isconnected ():
    machine.idle()
print("Connected to Wifi\n")

print("ifcongig: ", wlan.ifconfig(id=1))

#nets = wlan.scan()
#for net in nets:
#    if net.ssid == config['Ekstocken']:
#        print('Network found!')
#        wlan.connect(net.ssid, auth=(net.sec, config['familjenagren']), timeout=5000)
#        while not wlan.isconnected():
#            machine.idle() # save power while waiting
#        print('WLAN connection succeeded!')
#        break


