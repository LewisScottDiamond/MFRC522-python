#!/usr/bin/env python3
# -*- coding: utf8 -*-#

import requests
import threading
import time
import threading
import RPi.GPIO as GPIO
import MFRC522
import signal
import sys
import atexit


from flask import Flask
app = Flask(__name__)

@app.before_first_request
def activate_job():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    global BUZZER1
    global BUZZER2
    global DOOR_SENSOR_PIN

    def buzzer_setup():
        # Buzzer1
        GPIO.setup(BUZZER1, GPIO.OUT)    # Set pins' mode is output
        global buzz1                                             # Assign a global variable to replace GPIO.PWM
        buzz1 = GPIO.PWM(BUZZER1, 1)    # 440 is initial frequency.


        # Buzzer2
        GPIO.setup(BUZZER2, GPIO.OUT)    # Set pins' mode is output
        global buzz2                                             # Assign a global variable to replace GPIO.PWM
        buzz2 = GPIO.PWM(BUZZER2, 1)    # 440 is initial frequency.

    # Set up the door sensor pin.
    GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    continue_reading = True
    isOpen = None
    door_one = False

    def sound_buzzer():
        print("here")
        buzz1.ChangeFrequency(550)
        buzz1.start(1)
        time.sleep(1)
        buzz1.stop(1)

    def sound_buzzer2():
        buzz2.ChangeFrequency(300)
        time.sleep(1)
        buzz2.stop()

    def check_door1():
        while continue_reading:
            isOpen = GPIO.input(DOOR_SENSOR_PIN)
            if (isOpen):
                print("open")
                door1 = threading.Thread(target=change_door1_state)
                door1.start()
            else:
                print("closed")
                door_one = False
            time.sleep(0.5)

    def change_door1_state():
        global door_one
        print("change door one state to true")
        door_one = True
        print("door one = %s" % door_one)
        time.sleep(10)
        print("change door one state to false")
        door_one = False
        print("door one = %s" % door_one)
    # function to read uid an conver it to a string

    def uidToString(uid):
        mystring = ""
        for i in uid:
            mystring = mystring + format(i, '02X')
        return mystring


    # # Capture SIGINT for cleanup when the script is aborted
    # def end_read(signal, frame):
    #     global continue_reading
    #     print("Ctrl+C captured, ending read.")
    #     continue_reading = False
    #     GPIO.cleanup()

    # # Hook the SIGINT
    # signal.signal(signal.SIGINT, end_read)

    # Create an object of the class MFRC522 for device 0
    MIFAREReader = MFRC522.MFRC522()

    # Create a second object of the class MFRC522 for device 1
    MIFAREReader2 = MFRC522.MFRC522(dev=1)

    # Welcome message
    print("Welcome to the MFRC522 data read example")
    print("Press Ctrl-C to stop.")
    def rfid_scanner_one(name):
        while continue_reading:

            # Scan for cards
            (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

            # If a card is found
            if status == MIFAREReader.MI_OK:
                print ("Card detected on reader 1")

                # Get the UID of the card
                (status, uid) = MIFAREReader.MFRC522_SelectTagSN()

                # If we have the UID, continue
                if status == MIFAREReader.MI_OK:
                    print("Card read UID: %s" % uidToString(uid))
                    buzzer1 = threading.Thread(target=sound_buzzer)
                    buzzer1.start()

    def rfid_scanner_two(name):
        while continue_reading:

            # Scan for cards
            (status2, TagType2) = MIFAREReader2.MFRC522_Request(MIFAREReader.PICC_REQIDL)

            # If a card is found
            if status2 == MIFAREReader2.MI_OK:
                print ("Card detected on reader 2")

                # Get the UID of the card
                (status2, uid2) = MIFAREReader2.MFRC522_SelectTagSN()

                # If we have the UID, continue
                if status2 == MIFAREReader2.MI_OK:
                    print("Card read UID: %s" % uidToString(uid2))
                    buzzer2 = threading.Thread(target=sound_buzzer2)
                    buzzer2.start()

    # Setup the buzzers
    buzzer_setup()

    # These thread loops keep checking for chips.
    # If one is near either sensor it will get the UID

    # create and start the thread for the first rfid scanner
    x = threading.Thread(target=rfid_scanner_one, args=(1,))
    x.start()

    # create and start the thread for the second rfid scanner
    y = threading.Thread(target=rfid_scanner_two, args=(1,))
    y.start()

    checkDoor1 = threading.Thread(target=check_door1)
    checkDoor1.start()

@app.route("/")
def hello():
    return "Hello World!"

BUZZER1=17
BUZZER2=14
DOOR_SENSOR_PIN = 26

def start_runner():
    def start_loop():
        not_started = True
        while not_started:
            print('In start loop')
            try:
                r = requests.get('http://127.0.0.1:5000/')
                if r.status_code == 200:
                    print('Server started, quiting start_loop')
                    not_started = False
                print(r.status_code)
            except:
                print('Server not yet started')
            time.sleep(2)

    print('Started runner')
    thread = threading.Thread(target=start_loop)
    thread.start()

def destory():
    global BUZZER1
    global BUZZER2
    buzz1.stop()                                     # Stop the buzzer1
    GPIO.output(BUZZER1, 1)          # Set Buzzer1 pin to High
    buzz2.stop()                                     # Stop the buzzer2
    GPIO.output(BUZZER2, 1)          # Set Buzzer2 pin to High
    GPIO.cleanup()
    print("System stopped")

atexit.register(destory)

if __name__ == "__main__":
    start_runner()
    app.run(host='0.0.0.0')
