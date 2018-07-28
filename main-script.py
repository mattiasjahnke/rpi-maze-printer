import RPi.GPIO as GPIO
import subprocess, time

buttonPin = 16
holdTime = 2	# Duration to hold down the button before shutting down
tapTime = 0.01

def tap():
	print("Tap recognized!")
	subprocess.call(["python", "mazy.py", "20"])
	subprocess.call(["python", "printer.py"])


def hold():
	print("Hold recognized!")
	print("Good bye!")
	subprocess.call(["shutdown", "-h", "now"])

GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Sleeping a little..")
time.sleep(20)
print("Aight I'm ready to go!")

prevButtonState = GPIO.input(buttonPin)
prevTime = time.time()
tapEnable = False
holdEnable = False


while(True):
	buttonState = GPIO.input(buttonPin)
	t = time.time()

	# Has button state changed?
	if buttonState != prevButtonState:
		prevButtonState = buttonState
		prevTime = t
	else:
		if (t - prevTime) >= holdTime:
			if holdEnable == True:
				hold()
				holdEnable = False
				tapEnable = False
		elif (t - prevTime) >= tapTime:
			if buttonState == True:
				if tapEnable == True:
					tap()
					tapEnable = False
					holdEnable = False
			else:
				tapEnable = True
				holdEnable = True
