#!/usr/bin/env python3
# -*- coding: utf8 -*-#

import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import threading

continue_reading = True


# function to read uid an conver it to a string

def uidToString(uid):
    mystring = ""
    for i in uid:
        mystring = mystring + format(i, '02X')
    return mystring


# Capture SIGINT for cleanup when the script is aborted
def end_read(signal, frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Create a second object of the class MFRC522
MIFAREReader2 = MFRC522.MFRC522(dev=1)

# Welcome message
print("Welcome to the MFRC522 data read example")
print("Press Ctrl-C to stop.")

# This loop keeps checking for chips.
# If one is near it will get the UID and authenticate

def thread_one(name):
    while continue_reading:

        # Scan for cards
        (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # If a card is found
        if status == MIFAREReader.MI_OK:
            print ("Card detected")

            # Get the UID of the card
            (status, uid) = MIFAREReader.MFRC522_SelectTagSN()

            # If we have the UID, continue
            if status == MIFAREReader.MI_OK:
                print("Card read UID: %s" % uidToString(uid))

def thread_two(name):
    while continue_reading:

        # Scan for cards
        (status2, TagType2) = MIFAREReader2.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # If a card is found
        if status2 == MIFAREReader2.MI_OK:
            print ("Card detected")

            # Get the UID of the card
            (status2, uid2) = MIFAREReader2.MFRC522_SelectTagSN()

            # If we have the UID, continue
            if status2 == MIFAREReader2.MI_OK:
                print("Card read UID: %s" % uidToString(uid2))

x = threading.Thread(target=thread_one, args=(1,))

x.start()

y = threading.Thread(target=thread_two, args=(1,))

y.start()
