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
    global entry_scanned
    global exit_scanned

    def buzzer_setup():
        # Buzzer1
        GPIO.setup(BUZZER1, GPIO.OUT, initial=GPIO.HIGH)


        # Buzzer2
        GPIO.setup(BUZZER2, GPIO.OUT, initial=GPIO.HIGH)

    # Set up the door sensor pin.
    GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    continue_reading = True
    isOpen = None
    door_one = False

    def sound_buzzer(type):
        print("start buzzer")
        if (type == "bad"):
            for number in range(50):
                GPIO.setup(BUZZER1, GPIO.OUT, initial=GPIO.LOW)
                time.sleep(0.01)
                GPIO.setup(BUZZER1, GPIO.OUT, initial=GPIO.HIGH)
                time.sleep(0.01)
        else:
            GPIO.setup(BUZZER1, GPIO.OUT, initial=GPIO.LOW)
            time.sleep(1)
            GPIO.setup(BUZZER1, GPIO.OUT, initial=GPIO.HIGH)


    def sound_buzzer2():
        print("start buzzer")
        if (type == "bad"):
            for number in range(50):
                GPIO.setup(buzzer2, GPIO.OUT, initial=GPIO.LOW)
                time.sleep(0.01)
                GPIO.setup(BUZZER2, GPIO.OUT, initial=GPIO.HIGH)
                time.sleep(0.02)
        else:
            GPIO.setup(BUZZER2, GPIO.OUT, initial=GPIO.LOW)
            time.sleep(0.5)
            GPIO.setup(BUZZER2, GPIO.OUT, initial=GPIO.HIGH)

    def check_door1():
        while continue_reading:
            isOpen = GPIO.input(DOOR_SENSOR_PIN)
            if (isOpen):
                print("open")
                if (entry_scanned == False):
                    buzzer1 = threading.Thread(target=sound_buzzer("bad"))
                    buzzer1.start()
                door_one = True
            else:
                print("closed")
                door_one = False
            time.sleep(0.5)

    def entryScanned():
        global entry_scanned
        entry_scanned = True
        print("entry scanned")
        time.sleep(10)
        entry_scanned = False
        print("entry no longer scanned")

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
                    buzzer1 = threading.Thread(target=sound_buzzer("good"))
                    buzzer1.start()
                    enter = threading.Thread(target=entryScanned())
                    enter.start()

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
                    buzzer2 = threading.Thread(target=sound_buzzer2("good"))
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
entry_scanned = False
exit_scanned = False

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
    GPIO.cleanup()
    print("System stopped")

atexit.register(destory)

if __name__ == "__main__":
    start_runner()
    app.run(host='0.0.0.0')
