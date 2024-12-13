import time
from MCP3008 import MCP3008
import RPi.GPIO as GPIO

with open('/home/pi/growApp/except.txt', 'r+') as pump:
    
    
    
    x = 0
    while x < 5:
        pump.write('test ' + str(x))
        pump.write('\n')
        x += 1

