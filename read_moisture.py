from machine import Pin
from machine import ADC
import time

# empirical value dry dirt
DIRT_DRY = 3801
# empirical value wt dirt
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
    # X = (analogValue-Wet)/(Dry-Wet)*100
    moisture = 100 - ((analogValue - DIRT_WET) / (DIRT_DRY-DIRT_WET)) * 100

    return moisture