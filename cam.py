from picamera import PiCamera, Color
import os
import sys
from time import sleep
import time
from datetime import datetime
dt_now_filename = (datetime.now().strftime('%d%m%Y_%H%M%S'))
dt_now_str = (datetime.now().strftime('%H:%M:%S\n%b %d,%Y'))
camera = PiCamera()
a = (os.path.join(sys.path[0], "HIDS_Logs/Log_"))
b = dt_now_filename
c = '.jpg'
filename = a + b + c
print(filename)
print(dt_now_filename)
print(dt_now_str)

def capture():
    camera.annotate_background = Color('black')
    camera.annotate_foreground = Color('white')
    # camera.start_preview()
    camera.annotate_text = dt_now_str
    #sleep(2)
    camera.capture(filename)
    print("Captured!!")
    # camera.stop_preview()

# capture()