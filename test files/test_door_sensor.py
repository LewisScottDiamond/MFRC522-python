import RPi.GPIO as GPIO
import time
import sys
import signal

# Set Broadcom mode so we can address GPIO pins by number.
GPIO.setmode(GPIO.BCM)

DOOR_SENSOR_PIN = 26


# Initially we don't know if the door sensor is open or closed...
isOpen = None

# Clean up when the user exits with keyboard interrupt
def cleanupLights(signal, frame):
    GPIO.cleanup()
    sys.exit(0)

# Set up the door sensor pin.
GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# Set the cleanup handler for when user hits Ctrl-C to exit
signal.signal(signal.SIGINT, cleanupLights)

while True:
    isOpen = GPIO.input(DOOR_SENSOR_PIN)

    if (isOpen):
        print("open")
    else:
        print("closed")

    time.sleep(0.1)
