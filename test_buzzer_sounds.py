#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

Buzzer = 11    # pin11

CL = [0, 131, 147, 165, 175, 196, 211, 248]
   # C is the frequency list of the bass note, the first digit is 0 for placeholder use, and it is not used later
   # In addition to 0, the order is 1do, 2re, 3mi, 4fa, 5sol, 6la, 7si
CM = [0, 262, 294, 330, 350, 393, 441, 495]
   # Frequency of Middle C notes

CH = [0, 525, 589, 661, 700, 786, 882, 990]
  # Frequency of High C notes

song_0 = [      CL[1], CL[2], CL[3], CL[4], CL[5], CL[6], CL[7],
                CM[1], CM[2], CM[3], CM[4], CM[5], CM[6], CM[7],
                CH[1], CH[2], CH[3], CH[4], CH[5], CH[6], CH[7] ]
 # song_0 represents the note list from the bass do to the high si
beat_0 = [      2, 2, 2, 2, 2, 2, 2,
                2, 2, 2, 2, 2, 2, 2,
                2, 2, 2, 2, 2, 2, 2  ]
 # song_0's beat, 2 means 2 1/8 beats. A 1/8 beat is a 0.5 second delay.
song_1 = [      CM[3], CM[5], CM[6], CM[3], CM[2], CM[3], CM[5], CM[6],
                        CH[1], CM[6], CM[5], CM[1], CM[3], CM[2], CM[2], CM[3],
                        CM[5], CM[2], CM[3], CM[3], CL[6], CL[6], CL[6], CM[1],
                        CM[2], CM[3], CM[2], CL[7], CL[6], CM[1], CL[5] ]
# Notes of song1
beat_1 = [      1, 1, 3, 1, 1, 3, 1, 1,
                        1, 1, 1, 1, 1, 1, 3, 1,
                        1, 3, 1, 1, 1, 1, 1, 1,
                        1, 2, 1, 1, 1, 1, 1, 1,
                        1, 1, 3 ]
# Beats of song 1, 1 means 1/8 beats
song_2 = [      CM[1], CM[1], CM[1], CL[5], CM[3], CM[3], CM[3], CM[1],
                        CM[1], CM[3], CM[5], CM[5], CM[4], CM[3], CM[2], CM[2],
                        CM[3], CM[4], CM[4], CM[3], CM[2], CM[3], CM[1], CM[1],
                        CM[3], CM[2], CL[5], CL[7], CM[2], CM[1]        ]
# Notes of song2
beat_2 = [      1, 1, 2, 2, 1, 1, 2, 2,
                        1, 1, 2, 2, 1, 1, 3, 1,
                        1, 2, 2, 1, 1, 2, 2, 1,
                        1, 2, 2, 1, 1, 3 ]
# Beats of song 2, 1 means 1/8 beats,0.5 second


def setup():
    GPIO.setmode(GPIO.BOARD)                # Numbers GPIOs by physical location
    GPIO.setup(Buzzer, GPIO.OUT)    # Set pins' mode is output
    global Buzz                                             # Assign a global variable to replace GPIO.PWM
    Buzz = GPIO.PWM(Buzzer, 440)    # 440 is initial frequency.
    Buzz.start(50)                                  # Start Buzzer pin with 50% duty ration


def on():
	GPIO.output(BuzzerPin, GPIO.LOW)
	#Low level is ringing
def off():
	GPIO.output(BuzzerPin, GPIO.HIGH)
	#High level is to stop ringing
def beep(x):    #3 seconds after ringing for 3 seconds
	on()
	time.sleep(x)
	off()
	time.sleep(x)

def loop():
    while True:
#--------------------------------------------
        print '\n\n    Playing Low C notes...'
        for i in range(0, 7):         # Play song 0's C bass note
                Buzz.ChangeFrequency(song_0[i])
                # Change the frequency according to the note of the song
                print i      #Print the value of i
                time.sleep(beat_0[i] * 0.5)
                # Delay each note by 1 second according to the list of beats, 2 beats*0.5s=1s

        print '\n\n    Playing Middle C notes...'
        for i in range(7, 14):         # Play song 0
                Buzz.ChangeFrequency(song_0[i]) # Change the frequency along the song note
                print i
                time.sleep(beat_0[i] * 0.5)     # delay a note for beat * 0.5s

        print '\n\n    Playing High C notes...'
        for i in range(14, 21):         # Play song 0
                Buzz.ChangeFrequency(song_0[i]) # Change the frequency along the song note
                print i
                time.sleep(beat_0[i] * 0.5)     # delay a note for beat * 0.5s
        Buzz.ChangeFrequency(0.5)  #A tune ends with 3 seconds interval
        time.sleep(3)
    #--------------------------------------------
        print '\n    Playing song 1...'
        for i in range(0, len(song_1)):         # Play song 1
                    Buzz.ChangeFrequency(song_1[i]) # Change the frequency along the song note
                    time.sleep(beat_1[i] * 0.5)     # delay a note for beat * 0.5s
        Buzz.ChangeFrequency(0.5) #A tune ends with 3 seconds interval
        time.sleep(3)
    #--------------------------------------------
        print '\n\n    Playing song 2...'
        for i in range(0, len(song_2)):         # Play song 1
                Buzz.ChangeFrequency(song_2[i]) # Change the frequency along the song note
                time.sleep(beat_2[i] * 0.5)     # delay a note for beat * 0.5s
        Buzz.ChangeFrequency(0.5)
        time.sleep(3)


def destory():
    Buzz.stop()                                     # Stop the buzzer
    GPIO.output(Buzzer, 1)          # Set Buzzer pin to High
    GPIO.cleanup()                          # Release resource

if __name__ == '__main__':              # Program start from here
    setup()
    try:
            loop()
    except KeyboardInterrupt:       # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
            destory()
