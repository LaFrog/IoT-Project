from dht import DHT
from machine import Pin
import time

# Type 0 = dht11
# Type 1 = dht22



def value():
    th = DHT(Pin('P23', mode=Pin.OPEN_DRAIN), 0)
    time.sleep(3)
    result = th.read()
    # print('Temp:', result.temperature)
    # print('RH:', result.humidity)
    if result.is_valid():
        return(result.temperature,result.humidity)