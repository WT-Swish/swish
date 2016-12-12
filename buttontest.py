import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

GPIO.setup(11,GPIO.IN)
input = GPIO.input(11)


prev = False
inpu = GPIO.input(11)

while True:
    prev = inpu
    inpu = GPIO.input(11)
    if inpu and not prev:
        print("Button Pressed")
    elif prev and not inpu:
        print("Button Released")
