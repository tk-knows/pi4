# https://electronicshobbyists.com/raspberry-pi-analog-sensing-mcp3008-raspberry-pi-interfacing/
# Importing modules
import spidev # To communicate with SPI devices
from numpy import interp	# To scale values
from time import sleep	# To add delay
import RPi.GPIO as GPIO	# To use GPIO pins
# Start SPI connection
spi = spidev.SpiDev() # Created an object
spi.open(0,0)	
# Initializing LED pin as OUTPUT pin
led_pin = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)
# Creating a PWM channel at 100Hz frequency
pwm = GPIO.PWM(led_pin, 100)
pwm.start(0) 
# Read MCP3008 data
def analogInput(channel):
  spi.max_speed_hz = 1350000
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data
while True:
    output0 = analogInput(0) # Reading from CH0
    output0 = interp(output0, [0, 1023], [0, 100])
    # print("Chnl 0: {}".format(output0*3.3/100))
    output2 = analogInput(2) # Reading from CH2
    output2 = interp(output2, [0, 1023], [0,3300] )
    print("Chnl 0: {}, Chnl 2: {}".format(output0*3.3/100, output2))
    pwm.ChangeDutyCycle(output0)
    sleep(2.0)