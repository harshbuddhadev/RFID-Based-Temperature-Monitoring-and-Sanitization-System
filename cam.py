from picamera import PiCamera, Color
import os
import sys
from time import sleep
import time
from datetime import datetime

dt_now_filename = (datetime.now().strftime('%d%m%Y_%H%M%S')) #Create Filename with current time
dt_now_str = (datetime.now().strftime('%H:%M:%S\n%b %d,%Y')) #Fetch time for Photo Annotations
camera = PiCamera() #Initialize Camera

#Create Filename
a = (os.path.join(sys.path[0], "HIDS_Logs/Log_"))
b = dt_now_filename
c = '.jpg'
filename = a + b + c
print(filename)
print(dt_now_filename)
print(dt_now_str)
#Create Filename

def capture():
    camera.annotate_background = Color('black') # Set Background color for annotation
    camera.annotate_foreground = Color('white') # Set Foreground color for annotation
    # camera.start_preview()
    camera.annotate_text = dt_now_str # Pass Annotation Values
    #sleep(2)
    camera.capture(filename) #Capture Image and save to specified location
    print("Captured!!")
    # camera.stop_preview()

# capture()