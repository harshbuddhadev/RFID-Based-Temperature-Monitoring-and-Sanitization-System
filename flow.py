## Import Libraries
import os
import time
import RPi.GPIO as GPIO
from gpiozero import Servo
import pigpio
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
## Import Libraries


## Import Custom Libraries ##
from cam import capture
import cam
from get_temp import temp
from validate import vali
from upload import sheetsupdate
## Import Custom Libraries ##

## INIT Commands ##
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
os.popen("sudo pigpiod") #Init Pi GPIO
os.popen("sudo stty -F /dev/ttyUSB0 9600 time 2 min 100 -hupcl brkint ignpar -icrnl -opost -onlcr -isig -icanon -echo") #Init Serial Port
## INIT Commands ##

## OLED_INIT ##
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
draw.text((x, top + 0), "	  TEAM LAZR", font=font, fill=255)
disp.show()
## OLED_INIT ##


## Define Pins ##
relay=21
buzzer=5
servo = 22
red_led=13
green_led=6
## Define Pins ##

## Init GPIO ##
GPIO.setup(buzzer,GPIO.OUT)
GPIO.setup(red_led,GPIO.OUT)
GPIO.setup(green_led,GPIO.OUT)
pwm = pigpio.pi() 
pwm.set_mode(servo, pigpio.OUTPUT)
pwm.set_PWM_frequency( servo, 50 )
## Init GPIO ##

## Init Threshold ##
htemp=37.78
ltemp=32.00
## Init Threshold ##

id=[] ## Init Empty Lists for Data




## TAGSTART ##
try:
	while True:
		print("Place your Card On the RFID Scanner")

		draw.rectangle((0, 0, width, height), outline=0, fill=0)
		draw.text((x, top + 0), "	  TEAM LAZR", font=font, fill=255)
		draw.text((x, top + 8), "Place your Card On", font=font, fill=255)
		draw.text((x, top + 16), " the RFID Scanner", font=font, fill=255)
		disp.image(image)
		disp.show()
		
		tag_var=str(os.popen("sudo head -c 12 /dev/ttyUSB0").read()) #Read RFID Tag
		capture() # Capture Image

		GPIO.output(green_led,GPIO.HIGH)
		time.sleep(0.75)
		GPIO.output(green_led,GPIO.LOW)
		
		print(tag_var)
		tag_valid=False
		id=vali(tag_var) #Validate RFID Tag
		
		if(len(id) > 0): #If ID in List
			tag_valid=True
			print(id)

			draw.rectangle((0, 0, width, height), outline=0, fill=0)
			draw.text((x, top + 0), "	  TEAM LAZR", font=font, fill=255)
			draw.text((x, top + 8), "FName: "+id[0], font=font, fill=255)
			draw.text((x, top + 16), "LName: "+id[1], font=font, fill=255)
			draw.text((x, top + 25), "SID : "+id[2], font=font, fill=255)
			disp.image(image)
			disp.show()
		
		elif(len(id) == 0 ): # IF ID Not in List
			print("updating sheets")
			sheetsupdate("-","-","-",tag_var,"-","Invalid Card") #Update Google Sheet
			GPIO.output(green_led,GPIO.LOW)
			for i in range(10):
				GPIO.output(buzzer,GPIO.HIGH)
				GPIO.output(red_led,GPIO.HIGH)
				time.sleep(0.2)
				GPIO.output(buzzer,GPIO.LOW)
				GPIO.output(red_led,GPIO.LOW)
				time.sleep(0.2)
		temp_var=False
		door_on=False
## TAGEND ##


## TEMPSTART ##
		if(tag_valid):
			print ("Place Your finger on the temprature sensor")
			time.sleep(3)
			bodytemp=temp() #Fetch Temperature
			if(bodytemp>htemp): #If Body Temp Higher Than Threshold
				print("High Body Temp")
				for i in range(10): #Ring Buzzer
					GPIO.output(buzzer,GPIO.HIGH)
					GPIO.output(red_led,GPIO.HIGH)
					time.sleep(0.2)
					GPIO.output(buzzer,GPIO.LOW)
					GPIO.output(red_led,GPIO.LOW)
					time.sleep(0.2)
				
				sheetsupdate(id[0],id[1],id[2],tag_var,bodytemp,"High Temp") #Update Google Sheet
			elif(bodytemp<=htemp and bodytemp>=ltemp): #If Temperature within Threshold
				print("Normal Body Temperature")
				temp_var=True
				GPIO.output(buzzer,GPIO.HIGH)
				time.sleep(1)
				GPIO.output(buzzer,GPIO.LOW)
				sheetsupdate(id[0],id[1],id[2],tag_var,bodytemp,"Good Temp") #Update Google Sheet


			elif(bodytemp<ltemp): #If Body Temperature below Threshold
				print("Could Not Detect Temperature Try Again!!!")
				for i in range(3): #Ring Buzzer
					GPIO.output(buzzer,GPIO.HIGH)
					GPIO.output(red_led,GPIO.HIGH)
					time.sleep(1)
					GPIO.output(buzzer,GPIO.LOW)
					GPIO.output(red_led,GPIO.LOW)
					time.sleep(1)
				sheetsupdate(id[0],id[1],id[2],tag_var,bodytemp,"No Temp") #Update Google Sheet
			

				
## TEMPEND ##


## DISPENSE START ###

		if(temp_var): #If Body Temp within Threshold, dispense sanitizer
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

## DISPENSE END ##


## DOORSTART ##

		if(door_on):#If Body Temp within Threshold, Open Door
			GPIO.output(green_led,GPIO.HIGH)
			print("Gate Open")
			time.sleep(1.5)
			pwm.set_servo_pulsewidth( servo, 500 ) ;#0 degree
			time.sleep(0.5)
			pwm.set_servo_pulsewidth( servo, 1500 ) ;#90 degree
			time.sleep(3.75)
			pwm.set_servo_pulsewidth( servo, 500 ) ;#0 degree
			GPIO.output(green_led,GPIO.LOW)
	   
## DOOREND ##

except KeyboardInterrupt:
	print("Code stopped by User")
	cam.capture()
	GPIO.cleanup()
	print("GPIO Cleanup Called!!")
	cam.camera.close()
	print("Camera Closed!")
	if __name__ == "__main__":
		exit()