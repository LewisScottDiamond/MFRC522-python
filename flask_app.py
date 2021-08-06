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
import textFileFunctions as tff


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
    global DOOR_ONE_RED_LED_PIN
    global DOOR_ONE_GREEN_LED_PIN
    global DOOR_TWO_RED_LED_PIN
    global DOOR_TWO_GREEN_LED_PIN

    def buzzer_setup():
        # Buzzer1
        GPIO.setup(BUZZER1, GPIO.OUT, initial=GPIO.HIGH)


        # Buzzer2
        GPIO.setup(BUZZER2, GPIO.OUT, initial=GPIO.HIGH)

    # Set up the door sensor pins.
    GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(DOOR_SENSOR_PIN2, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    # set up the LED pins
    GPIO.setup(DOOR_ONE_RED_LED_PIN, GPIO.OUT)   # Set ledPin as output
    GPIO.output(DOOR_ONE_RED_LED_PIN, GPIO.LOW)  # Set ledPin to LOW to turn Off the LED
    GPIO.setup(DOOR_ONE_GREEN_LED_PIN, GPIO.OUT)   # Set ledPin as output
    GPIO.output(DOOR_ONE_GREEN_LED_PIN, GPIO.LOW)  # Set ledPin to LOW to turn Off the LED

    GPIO.setup(DOOR_TWO_RED_LED_PIN, GPIO.OUT)   # Set ledPin as output
    GPIO.output(DOOR_TWO_RED_LED_PIN, GPIO.LOW)  # Set ledPin to LOW to turn Off the LED
    GPIO.setup(DOOR_TWO_GREEN_LED_PIN, GPIO.OUT)   # Set ledPin as output
    GPIO.output(DOOR_TWO_GREEN_LED_PIN, GPIO.LOW)  # Set ledPin to LOW to turn Off the LED

    continue_reading = True
    isOpen = None
    door_one = False

    def door_one_action(type):
        if(type == "bad"):
            GPIO.output(DOOR_ONE_RED_LED_PIN, GPIO.HIGH)
            for number in range(50):
                GPIO.setup(BUZZER1, GPIO.OUT, initial=GPIO.LOW)
                time.sleep(0.01)
                GPIO.setup(BUZZER1, GPIO.OUT, initial=GPIO.HIGH)
                time.sleep(0.01)
            time.sleep(9)
            GPIO.output(DOOR_ONE_RED_LED_PIN, GPIO.LOW)
        else:
            global entry_scanned
            entry_scanned = True
            print("entry scanned")
            GPIO.output(DOOR_ONE_GREEN_LED_PIN, GPIO.HIGH)
            GPIO.setup(BUZZER1, GPIO.OUT, initial=GPIO.LOW)
            time.sleep(0.2)
            GPIO.setup(BUZZER1, GPIO.OUT, initial=GPIO.HIGH)
            time.sleep(9.8)
            GPIO.output(DOOR_ONE_GREEN_LED_PIN, GPIO.LOW)
            entry_scanned = False
            print("entry no longer scanned")

    def door_two_action(type):
        if(type == "bad"):
            GPIO.output(DOOR_TWO_RED_LED_PIN, GPIO.HIGH)
            for number in range(50):
                GPIO.setup(BUZZER2, GPIO.OUT, initial=GPIO.LOW)
                time.sleep(0.01)
                GPIO.setup(BUZZER2, GPIO.OUT, initial=GPIO.HIGH)
                time.sleep(0.01)
            time.sleep(9)
            GPIO.output(DOOR_TWO_RED_LED_PIN, GPIO.LOW)
        else:
            global entry_scanned
            exit_scanned = True
            print("exit scanned")
            GPIO.output(DOOR_TWO_GREEN_LED_PIN, GPIO.HIGH)
            GPIO.setup(BUZZER2, GPIO.OUT, initial=GPIO.LOW)
            time.sleep(0.2)
            GPIO.setup(BUZZER2, GPIO.OUT, initial=GPIO.HIGH)
            time.sleep(9.8)
            GPIO.output(DOOR_TWO_GREEN_LED_PIN, GPIO.LOW)
            exit_scanned = False
            print("exit no longer scanned")


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


    def sound_buzzer2(type):
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
                print("entry door open")
                if (entry_scanned == False):
                    buzzer1 = threading.Thread(target=sound_buzzer("bad"))
                    buzzer1.start()
                door_one = True
            else:
                print("entry door closed")
                door_one = False
            time.sleep(0.5)

    def check_door2():
        while continue_reading:
            isOpen = GPIO.input(DOOR_SENSOR_PIN2)
            if (isOpen):
                print("exit door open")
                if (exit_scanned == False):
                    buzzer2 = threading.Thread(target=sound_buzzer("bad"))
                    buzzer2.start()
                door_two = True
            else:
                print("exit door closed")
                door_two = False
            time.sleep(0.5)

    def entryScanned():
        global entry_scanned
        entry_scanned = True
        print("entry scanned")
        time.sleep(10)
        entry_scanned = False
        print("entry no longer scanned")

    def exitScanned():
        global exit_scanned
        exit_scanned = True
        print("entry scanned")
        time.sleep(10)
        exit_scanned = False
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
                    guid = tff.find_guid_in_csv_file('uid.csv', uidToString(uid))
                    if(guid == False):
                        print("Card UID: %s Not found!" % uidToString(uid))
                        enter = threading.Thread(target=door_one_action("bad"))
                        enter.start()
                    else:
                        print("Card read UID: %s" % uidToString(uid))
                        enter = threading.Thread(target=door_one_action("good"))
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
                    guid = tff.find_guid_in_csv_file('uid.csv', uidToString(uid2))
                    if(guid == False):
                        print("Card UID: %s Not found!" % uidToString(uid2))
                        exit = threading.Thread(target=door_two_action("bad"))
                        exit.start()
                    else:
                        print("Card read UID: %s" % uidToString(uid2))
                        exit = threading.Thread(target=door_two_action("good"))
                        exit.start()

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


    checkDoor2 = threading.Thread(target=check_door2)
    checkDoor2.start()

@app.route("/")
def hello():
    return "Hello World!"

BUZZER1=17
BUZZER2=14
DOOR_ONE_RED_LED_PIN=21
DOOR_ONE_GREEN_LED_PIN=20
DOOR_TWO_RED_LED_PIN=16
DOOR_TWO_GREEN_LED_PIN=12
DOOR_SENSOR_PIN = 26
DOOR_SENSOR_PIN2 = 19
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
