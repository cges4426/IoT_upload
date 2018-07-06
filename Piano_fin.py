import RPi.GPIO as GPIO
import time
import random
import time
import random
import pdb

GPIO.setmode(GPIO.BCM)  
GPIO.setwarnings(False)
seven_pin = [14, 15, 18, 17, 27, 22 ,23];
seven_names = ['a', 'b', 'c', 'd', 'e', 'f', 'g'] ;
#pin_on = 1 , pin_off = 0
seven_Display = [(1,1,1,1,1,1,0),(0,1,1,0,0,0,0),(1,1,0,1,1,0,1),(1,1,1,1,0,0,1),(0,1,1,0,0,1,1),(1,0,1,1,0,1,1),(1,0,1,1,1,1,1),(1,1,1,0,0,0,0),(1,1,1,1,1,1,1),(1,1,1,1,0,1,1)]

names = ['1', '2', '3', '4', '5', '6', '7', '8']
Freq = [ 261, 294, 330, 349, 392, 440, 494, 523];
LED_pin= [21, 26, 19, 12, 5,  8, 25, 10]
Button_pin  =  [20, 16, 13,  6, 7, 11,  9, 24]

Buzzer_pin = 2
record_pin = 3
numSong_pin = 4

global record_flag #Recording or not, 0 = no, 1 = yes
record_flag= 0

#intialize GPIO setting
def setGPIO():

    for i in range(7):
        GPIO.setup(seven_pin[i], GPIO.OUT)

    for i in range(8):

        GPIO.setup(Button_pin[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(LED_pin[i],GPIO.OUT)

    GPIO.setup(Buzzer_pin,GPIO.OUT)
    GPIO.setup(record_pin , GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(numSong_pin , GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Pushing the button, call the function
def ranSong():
    if(GPIO.input(numSong_pin)==0):
        showNum()
            

# Showing the number on Seven-segment display
def showNum():
    #At most, you can put 10 songs.
    num = random.randint(1, 5)

    for j in range(7):
        if(seven_Display[num][j]==1):
            GPIO.output(seven_pin[j], True)            
    
    time.sleep(1)
    singSong(num)  #call the function, give the song number
    
    for j in range(7):
        GPIO.output(seven_pin[j], False)


def singSong(num):
    # to improve it, you can add tempo to the song
    try:
        p = GPIO.PWM(Buzzer_pin, 50)
        p.start(50)
        Read_file = open(str(num) + '.txt', 'r')
        item = Read_file.readlines()
        print("Song number:" + str(num))
        for row in item:
            for word in row:
                time.sleep(0.01)
                for i in range(8):
                    if (names[i] == word):
                        p.start(50)
                        GPIO.output(Buzzer_pin, True)
                        GPIO.output(LED_pin[i], True)
                        p.ChangeFrequency(Freq[i])
                        time.sleep(0.35)

                        GPIO.output(Buzzer_pin, False)
                        GPIO.output(LED_pin[i], False)
                        p.stop()
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass


#Record the song you play
def recordSong(record_flag):

    #Record the time
    record_start = []
    record_end = []
    record_song = []
    
    print("Start recording...")
    time.sleep(0.5)
    start = time.time()
    record_start.append(start)  #Get the start time
    
    while (record_flag == 1): #Have not push the button again
        try:
            for i in range(8):
                if(GPIO.input(Button_pin[i])==0):
                    record_start.append(time.time())
                    record_song.append(names[i])
            
                    p.start(80)
                    GPIO.output(Buzzer_pin,True)
                    p.ChangeFrequency(Freq[i])
                    #print(names[i])
                    
                    while(GPIO.input(Button_pin[i])==0):                                               
                        GPIO.output(LED_pin[i],True)
                        
                    record_end.append(time.time())
                    #print (record_end)
                    
                elif(GPIO.input(record_pin)==0):  #Push the button again to end the recording
                    record_end.append(time.time())
                    record_flag = 0
                    print("End recording." )
                    print("")
                    time.sleep(0.5)
                    print("That's listen to it again!!")
                    
                    length = len(record_song)
                    start = record_start[0]

                    #Replay again
                    for k in range(length):
                        
                        start_time = record_start[k+1] - start                        
                        time_long = record_end[k] - record_start[k+1]                
                        start = record_end[k]
                        
                        time.sleep(start_time)
                        
                        for j in range(8):               
                            if(names[j]== record_song[k]):
                                p.start(80)
                                GPIO.output(Buzzer_pin,True)
                                GPIO.output(LED_pin[j],True)
                                p.ChangeFrequency(Freq[j])
                                time.sleep(time_long)
                                
                                GPIO.output(Buzzer_pin,False)
                                GPIO.output(LED_pin[j],False)
                                p.stop()
                    print("Done")
                else:
                    GPIO.output(Buzzer_pin,False)
                    GPIO.output(LED_pin[i],False)
                    p.stop()
                

        except KeyboardInterrupt:
          pass

#Anytime to push the button of the piano
def Piano():
    try:
        time.sleep(0.01)
        for i in range(8):
            if(GPIO.input(Button_pin[i])==0):
                p.start(80)
                GPIO.output(Buzzer_pin,True)
                GPIO.output(LED_pin[i],True)
                p.ChangeFrequency(Freq[i])
                time.sleep(0.1)      
            else:
                GPIO.output(Buzzer_pin,False)
                GPIO.output(LED_pin[i],False)
                p.stop()

    except KeyboardInterrupt:
      pass


setGPIO()
p = GPIO.PWM(Buzzer_pin, 80)
p.start(80)

#Detect the situation
try:
    while True:
        if(GPIO.input(numSong_pin)==0):
            showNum()
        elif(GPIO.input(record_pin)==0):
            record_flag = 1
            recordSong(record_flag)
        else:
            Piano()
      
except KeyboardInterrupt:
  pass


p.stop()
GPIO.cleanup()

