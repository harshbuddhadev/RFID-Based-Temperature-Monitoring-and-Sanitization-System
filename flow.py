import os
from cam import capture
import cam
from upload import sheetsupdate
from get_temp import temp
import RPi.GPIO as GPIO
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
import time
from gpiozero import Servo
import pigpio
os.popen("sudo pigpiod") #### AGAR NHI CHALA TOH PUT THIS COMMAND MANUALLY ####
from validate import vali
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306



###############################OLED_INIT###############################
i2c = busio.I2C(3, 2)
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
disp.fill(0)
disp.show()
width = disp.width
height = disp.height
image = Image.new("1", (width, height))
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, width, height), outline=0, fill=0)
padding = -2
top = padding
bottom = height - padding
x = 0
font = ImageFont.load_default()
draw.text((x, top + 0), "      TEAM LAZR", font=font, fill=255)
disp.show()
###############################OLED_INIT###############################




os.popen("sudo stty -F /dev/ttyUSB0 9600 time 2 min 100 -hupcl brkint ignpar -icrnl -opost -onlcr -isig -icanon -echo")
# os.popen("sudo pigpiod")


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

relay=21
buzzer=5
servo = 22
red_led=13
green_led=6

GPIO.setup(buzzer,GPIO.OUT)
GPIO.setup(red_led,GPIO.OUT)
GPIO.setup(green_led,GPIO.OUT)
pwm = pigpio.pi() 
pwm.set_mode(servo, pigpio.OUTPUT)
pwm.set_PWM_frequency( servo, 50 )
htemp=40.0
ltemp=30.0


id=[]




##################################TAGSTART###################################
try:
    while True:
        print("Place your Card On the RFID Scanner")
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        draw.text((x, top + 0), "      TEAM LAZR", font=font, fill=255)
        draw.text((x, top + 8), "Place your Card On", font=font, fill=255)
        draw.text((x, top + 16), " the RFID Scanner", font=font, fill=255)
        disp.image(image)
        disp.show()
        tag_var=str(os.popen("sudo head -c 12 /dev/ttyUSB0").read())
        capture()
        GPIO.output(green_led,GPIO.HIGH)
        time.sleep(0.75)
        GPIO.output(green_led,GPIO.LOW)
        print(tag_var)
        tag_valid=False
        id=vali(tag_var)
        if(len(id) > 0):
            tag_valid=True
            print(id)
            print("a")
            draw.rectangle((0, 0, width, height), outline=0, fill=0)
            draw.text((x, top + 0), "      TEAM LAZR", font=font, fill=255)
            draw.text((x, top + 8), "FName: "+id[0], font=font, fill=255)
            draw.text((x, top + 16), "LName: "+id[1], font=font, fill=255)
            draw.text((x, top + 25), "SID : "+id[2], font=font, fill=255)
            disp.image(image)
            disp.show()
        elif(len(id) == 0 ):
            print("updating sheets")
            sheetsupdate("-","-","-",tag_var,"-","Invalid Card")
            GPIO.output(green_led,GPIO.LOW)
            print("both false")
            for i in range(10):
                GPIO.output(buzzer,GPIO.HIGH)
                GPIO.output(red_led,GPIO.HIGH)
                time.sleep(0.2)
                GPIO.output(buzzer,GPIO.LOW)
                GPIO.output(red_led,GPIO.LOW)
                time.sleep(0.2)
        

    
    
##################################TAGEND###################################
    

        temp_var=False
        door_on=False
##################################TEMPSTART###################################
        if(tag_valid):
            print ("Place Your finger on the temprature sensor")
            time.sleep(3)
            bodytemp=temp()
            if(bodytemp>htemp):
                print("High")
                for i in range(10):
                    GPIO.output(buzzer,GPIO.HIGH)
                    GPIO.output(red_led,GPIO.HIGH)
                    time.sleep(0.2)
                    GPIO.output(buzzer,GPIO.LOW)
                    GPIO.output(red_led,GPIO.LOW)
                    time.sleep(0.2)
                
                print("updating sheets")
                sheetsupdate(id[0],id[1],id[2],tag_var,bodytemp,"High Temp")
            elif(bodytemp<=htemp and bodytemp>=ltemp):
                print("Normal")
                temp_var=True
                GPIO.output(buzzer,GPIO.HIGH)
                time.sleep(1)
                GPIO.output(buzzer,GPIO.LOW)
                print("updating sheets")
                sheetsupdate(id[0],id[1],id[2],tag_var,bodytemp,"Good Temp")

                    
            elif(bodytemp<ltemp):
                print("Could Not Detect Temperature Try Again!!!")
                for i in range(3):
                    GPIO.output(buzzer,GPIO.HIGH)
                    GPIO.output(red_led,GPIO.HIGH)
                    time.sleep(1)
                    GPIO.output(buzzer,GPIO.LOW)
                    GPIO.output(red_led,GPIO.LOW)
                    time.sleep(1)
                print("updating sheets")
                sheetsupdate(id[0],id[1],id[2],tag_var,bodytemp,"No Temp")
            

                
##################################TEMPEND###################################


##################################DISPENSE START###################################

        if(temp_var):
            print("Temperature: ",bodytemp)
            GPIO.output(green_led,GPIO.HIGH)
            GPIO.setup(relay,GPIO.OUT)
            print("Place your hand below the dispenser")
            time.sleep(3)
            GPIO.output(relay,GPIO.HIGH)
            time.sleep(1)
            GPIO.output(relay,GPIO.LOW)
            time.sleep(0.3)
            GPIO.output(relay,GPIO.HIGH)
            door_on=True
            GPIO.output(green_led,GPIO.LOW)

##################################DISPENSEEND###################################


##################################DOORSTART###################################

        if(door_on):
            GPIO.output(green_led,GPIO.HIGH)
            print("Gate Open")
            time.sleep(1.5)
            pwm.set_servo_pulsewidth( servo, 500 ) ;#0 degree
            time.sleep(0.5)
            pwm.set_servo_pulsewidth( servo, 1500 ) ;#90 degree
            time.sleep(3.75)
            pwm.set_servo_pulsewidth( servo, 500 ) ;#0 degree
            GPIO.output(green_led,GPIO.LOW)
       
##################################DOOREND###################################


# Reset by pressing CTRL + C
except KeyboardInterrupt:
    cam.capture()
    print("Code stopped by User")
    GPIO.cleanup()
    print("GPIO Cleanup Called!!")
    cam.camera.close()
    





