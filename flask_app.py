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
import datetime


from flask import Flask, render_template
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

    def GPIO_Setup():
        # Buzzer1
        GPIO.setup(BUZZER1, GPIO.OUT, initial=GPIO.HIGH)

        # Buzzer2
        GPIO.setup(BUZZER2, GPIO.OUT, initial=GPIO.HIGH)

        # Set up the door sensor pins.
        GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(DOOR_SENSOR_PIN2, GPIO.IN, pull_up_down = GPIO.PUD_UP)

        # set up door one's LED pins
        GPIO.setup(DOOR_ONE_RED_LED_PIN, GPIO.OUT)   # Set ledPin as output
        GPIO.output(DOOR_ONE_RED_LED_PIN, GPIO.LOW)  # Set ledPin to LOW to turn Off the LED
        GPIO.setup(DOOR_ONE_GREEN_LED_PIN, GPIO.OUT)   # Set ledPin as output
        GPIO.output(DOOR_ONE_GREEN_LED_PIN, GPIO.LOW)  # Set ledPin to LOW to turn Off the LED

        # setup door two's LED pins
        GPIO.setup(DOOR_TWO_RED_LED_PIN, GPIO.OUT)   # Set ledPin as output
        GPIO.output(DOOR_TWO_RED_LED_PIN, GPIO.LOW)  # Set ledPin to LOW to turn Off the LED
        GPIO.setup(DOOR_TWO_GREEN_LED_PIN, GPIO.OUT)   # Set ledPin as output
        GPIO.output(DOOR_TWO_GREEN_LED_PIN, GPIO.LOW)  # Set ledPin to LOW to turn Off the LED

    continue_reading = True
    isOpen = None
    isOpen2 = None
    door_one = False
    door_two = False

    def door_one_action(type, waitTime):
        global entry_scanned
        global count
        entry_scanned = True
        if(type == "bad"):
            if not GPIO.input(DOOR_ONE_RED_LED_PIN):
                GPIO.output(DOOR_ONE_RED_LED_PIN, GPIO.HIGH)
                GPIO.setup(BUZZER1, GPIO.OUT, initial=GPIO.LOW)
            if(timeNow() > addSecs(waitTime, -1.9) and timeNow() < addSecs(waitTime, -1.8)):
                GPIO.setup(BUZZER1, GPIO.OUT, initial=GPIO.HIGH)
            if(timeNow() > addSecs(waitTime, -1.7) and timeNow() < addSecs(waitTime, -1.6)):
                GPIO.setup(BUZZER1, GPIO.OUT, initial=GPIO.LOW)
            if(timeNow() > addSecs(waitTime, -1.5) and timeNow() < addSecs(waitTime, -1.4)):
                GPIO.setup(BUZZER1, GPIO.OUT, initial=GPIO.HIGH)
            if(timeNow() > addSecs(waitTime, -1.3) and timeNow() < addSecs(waitTime, -1.2)):
                GPIO.setup(BUZZER1, GPIO.OUT, initial=GPIO.LOW)
            if(timeNow() > addSecs(waitTime, -1.1) and timeNow() < addSecs(waitTime, -1)):
                GPIO.setup(BUZZER1, GPIO.OUT, initial=GPIO.HIGH)
            if(timeNow() > addSecs(waitTime, -0.9) and timeNow() < addSecs(waitTime, -0.8)):
                GPIO.setup(BUZZER1, GPIO.OUT, initial=GPIO.LOW)
            if(timeNow() > addSecs(waitTime, -0.7) and timeNow() < addSecs(waitTime, -0.6)):
                GPIO.setup(BUZZER1, GPIO.OUT, initial=GPIO.HIGH)
            if(timeNow() > addSecs(waitTime, -0.5) and timeNow() < addSecs(waitTime, -0.4)):
                GPIO.setup(BUZZER1, GPIO.OUT, initial=GPIO.LOW)
            if(timeNow() > addSecs(waitTime, -0.3) and timeNow() < addSecs(waitTime, -0.2)):
                GPIO.setup(BUZZER1, GPIO.OUT, initial=GPIO.HIGH)
        else:
            count += 1
            if not GPIO.input(DOOR_ONE_GREEN_LED_PIN):
                GPIO.output(DOOR_ONE_GREEN_LED_PIN, GPIO.HIGH)
                GPIO.setup(BUZZER1, GPIO.OUT, initial=GPIO.LOW)
            if(waitTime < currentTimePlusSeconds(1.8)):
                GPIO.setup(BUZZER1, GPIO.OUT, initial=GPIO.HIGH)

    def door_two_action(type, waitTime2):
        global exit_scanned
        global count
        exit_scanned = True
        if(type == "bad"):
            if not GPIO.input(DOOR_TWO_RED_LED_PIN):
                GPIO.output(DOOR_TWO_RED_LED_PIN, GPIO.HIGH)
                GPIO.setup(BUZZER2, GPIO.OUT, initial=GPIO.LOW)
            if(timeNow() > addSecs(waitTime2, -1.9) and timeNow() < addSecs(waitTime2, -1.8)):
                GPIO.setup(BUZZER1, GPIO.OUT, initial=GPIO.HIGH)
            if(timeNow() > addSecs(waitTime2, -1.7) and timeNow() < addSecs(waitTime2, -1.6)):
                GPIO.setup(BUZZER2, GPIO.OUT, initial=GPIO.LOW)
            if(timeNow() > addSecs(waitTime2, -1.5) and timeNow() < addSecs(waitTime2, -1.4)):
                GPIO.setup(BUZZER2, GPIO.OUT, initial=GPIO.HIGH)
            if(timeNow() > addSecs(waitTime2, -1.3) and timeNow() < addSecs(waitTime2, -1.2)):
                GPIO.setup(BUZZER2, GPIO.OUT, initial=GPIO.LOW)
            if(timeNow() > addSecs(waitTime2, -1.1) and timeNow() < addSecs(waitTime2, -1)):
                GPIO.setup(BUZZER2, GPIO.OUT, initial=GPIO.HIGH)
            if(timeNow() > addSecs(waitTime2, -0.9) and timeNow() < addSecs(waitTime2, -0.8)):
                GPIO.setup(BUZZER2, GPIO.OUT, initial=GPIO.LOW)
            if(timeNow() > addSecs(waitTime2, -0.7) and timeNow() < addSecs(waitTime2, -0.6)):
                GPIO.setup(BUZZER2, GPIO.OUT, initial=GPIO.HIGH)
            if(timeNow() > addSecs(waitTime2, -0.5) and timeNow() < addSecs(waitTime2, -0.4)):
                GPIO.setup(BUZZER2, GPIO.OUT, initial=GPIO.LOW)
            if(timeNow() > addSecs(waitTime2, -0.3) and timeNow() < addSecs(waitTime2, -0.2)):
                GPIO.setup(BUZZER2, GPIO.OUT, initial=GPIO.HIGH)
        else:
            if (count > 0 ):
                count -= 1
            else:
                count = 0
            if not GPIO.input(DOOR_TWO_GREEN_LED_PIN):
                GPIO.output(DOOR_TWO_GREEN_LED_PIN, GPIO.HIGH)
                GPIO.setup(BUZZER2, GPIO.OUT, initial=GPIO.LOW)
            if(waitTime2 < currentTimePlusSeconds(1.8)):
                GPIO.setup(BUZZER2, GPIO.OUT, initial=GPIO.HIGH)


    # def door_two_action_OLD(type):
    #     if(type == "bad"):
    #         GPIO.output(DOOR_TWO_RED_LED_PIN, GPIO.HIGH)
    #         for number in range(50):
    #             GPIO.setup(BUZZER2, GPIO.OUT, initial=GPIO.LOW)
    #             time.sleep(0.01)
    #             GPIO.setup(BUZZER2, GPIO.OUT, initial=GPIO.HIGH)
    #             time.sleep(0.01)
    #         time.sleep(2)
    #         GPIO.output(DOOR_TWO_RED_LED_PIN, GPIO.LOW)
    #     else:
    #         global entry_scanned
    #         exit_scanned = True
    #         print("exit scanned")
    #         GPIO.output(DOOR_TWO_GREEN_LED_PIN, GPIO.HIGH)
    #         GPIO.setup(BUZZER2, GPIO.OUT, initial=GPIO.LOW)
    #         time.sleep(0.2)
    #         GPIO.setup(BUZZER2, GPIO.OUT, initial=GPIO.HIGH)
    #         time.sleep(9.8)
    #         GPIO.output(DOOR_TWO_GREEN_LED_PIN, GPIO.LOW)
    #         exit_scanned = False
    #         print("exit no longer scanned")


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
            isOpen2 = GPIO.input(DOOR_SENSOR_PIN2)
            if (isOpen2):
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

    # method to add seconds to the time passed in
    def addSecs(tm, secs):
        fulldate = tm
        fulldate = fulldate + datetime.timedelta(0, secs)
        return fulldate

    def currentTimePlusSeconds(seconds):
        currentTime = datetime.datetime.now()
        newTime = addSecs(currentTime, seconds)
        return newTime

    def timeNow():
        return datetime.datetime.now()

    # Create an object of the class MFRC522 for device 0
    MIFAREReader = MFRC522.MFRC522()

    # Create a second object of the class MFRC522 for device 1
    MIFAREReader2 = MFRC522.MFRC522(dev=1)

    # Welcome message
    print("Welcome to the MFRC522 data read example")
    print("Press Ctrl-C to stop.")



    def rfid_scanner_one(name):

        waitTimeGood = timeNow()
        waitTimeBad = timeNow()
        waitSecs = timeNow()
        global entry_scanned
        entry_scanned = False

        while continue_reading:
            # Scan for cards
            if (waitTimeGood > timeNow()):
                door_one_action("good", waitTimeGood)
                waitSecs = currentTimePlusSeconds(10)
            elif (waitTimeBad > timeNow()):
                door_one_action("bad", waitTimeBad)
                waitSecs = currentTimePlusSeconds(1)
            else:
                waitTimeGood = timeNow()
                waitTimeBad = timeNow()
                GPIO.output(DOOR_ONE_RED_LED_PIN, GPIO.LOW)
                GPIO.setup(BUZZER1, GPIO.OUT, initial=GPIO.HIGH)
                GPIO.output(DOOR_ONE_GREEN_LED_PIN, GPIO.LOW)
                if (waitSecs < timeNow()):
                    entry_scanned = False
            print("reader one running")
            if not entry_scanned:
                (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

                # If a card is found
                if status == MIFAREReader.MI_OK:
                    print ("Card detected on reader 1")

                    # Get the UID of the card
                    (status, uid) = MIFAREReader.MFRC522_SelectTagSN()

                    # If we have the UID, continue
                    if status == MIFAREReader.MI_OK:
                        # set the wait time for the event loop

                        guid = tff.find_guid_in_csv_file('uid.csv', uidToString(uid))
                        if(guid == False):
                            print("Card UID: %s Not found!" % uidToString(uid))
                            # door_one_action("bad", waitTime)
                            waitTimeBad = currentTimePlusSeconds(2)
                        else:
                            print("Card read GUID: %s" % guid)
                            # door_one_action("good", waitTime)
                            waitTimeGood= currentTimePlusSeconds(2)

    def rfid_scanner_two(name):

        waitTimeGood2 = timeNow()
        waitTimeBad2 = timeNow()
        waitSecs2 = timeNow()
        global exit_scanned
        exit_scanned = False

        while continue_reading:
            # Scan for cards
            if (waitTimeGood2 > timeNow()):
                door_two_action("good", waitTimeGood2)
                waitSecs2 = currentTimePlusSeconds(10)
            elif (waitTimeBad2 > timeNow()):
                door_two_action("bad", waitTimeBad2)
                waitSecs2 = currentTimePlusSeconds(1)
            else:
                waitTimeGood2 = timeNow()
                waitTimeBad2 = timeNow()
                GPIO.output(DOOR_TWO_RED_LED_PIN, GPIO.LOW)
                GPIO.setup(BUZZER2, GPIO.OUT, initial=GPIO.HIGH)
                GPIO.output(DOOR_TWO_GREEN_LED_PIN, GPIO.LOW)
                if (waitSecs2 < timeNow()):
                    exit_scanned = False
            print("reader two runnung")        
            if not exit_scanned:
                (status2, TagType2) = MIFAREReader2.MFRC522_Request(MIFAREReader.PICC_REQIDL)

                # If a card is found
                if status2 == MIFAREReader2.MI_OK:
                    print ("Card detected on reader 2")

                    # Get the UID of the card
                    (status2, uid2) = MIFAREReader2.MFRC522_SelectTagSN()

                    # If we have the UID, continue
                    if status2 == MIFAREReader2.MI_OK:
                        # set the wait time for the event loop

                        guid = tff.find_guid_in_csv_file('uid.csv', uidToString(uid2))
                        if(guid == False):
                            print("Card UID: %s Not found!" % uidToString(uid2))
                            # door_one_action("bad", waitTime)
                            waitTimeBad2 = currentTimePlusSeconds(2)
                        else:
                            print("Card read GUID: %s" % guid)
                            # door_one_action("good", waitTime)
                            waitTimeGood2 = currentTimePlusSeconds(2)

    # Setup the GPIO pins
    GPIO_Setup()

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
    return "hello world"

@app.route("/count")
def count():
    global count
    return render_template("home.html", count=count)

# setup values
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
count = 0

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
