import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)



GPIO.setup(17,GPIO.IN)
input = GPIO.input(17)


while True:
  if (GPIO.input(17)):
    print("Button Pressed")
