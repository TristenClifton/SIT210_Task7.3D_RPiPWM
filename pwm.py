import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

def resetDistanceSensor():
	GPIO.setup(ECHO,GPIO.OUT)
	GPIO.output(ECHO, GPIO.LOW)
	GPIO.setup(ECHO,GPIO.IN)

#Designate pins
LED = 3
TRIG = 5
ECHO = 7
#Eable pins
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(LED, GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.output(TRIG, False)
print "Waiting For Sensor To Settle"
time.sleep(2)

pi_pwm = GPIO.PWM(LED,700)		#create PWM instance with frequency
pi_pwm.start(0)				#start PWM of required Duty Cycle 

    


def ReadDistance():
	
	readDuration = 0.2
	
	startReadtime = time.time()	
	pulse_durations = []
	
	while( time.time() < (startReadtime + readDuration)):
	
		GPIO.output(TRIG, True)
		time.sleep(0.00001)
		GPIO.output(TRIG, False)
		pulse_start = time.time()
		
		
		timeoutTime = time.time() + 0.5
		
		while(GPIO.input(ECHO)==0 and (time.time() < timeoutTime)):
			pulse_start = time.time()
		
		while(GPIO.input(ECHO)==1 and (time.time() < timeoutTime)):
			pulse_end = time.time()
			
		if(time.time() > timeoutTime):
			#timeout Caught
			print("timeout caught")
			resetDistanceSensor()
			return ReadDistance()
		
		distance = round(((pulse_end - pulse_start)* 17150), 0)
		
		if(distance <= 0):
			#exception Caught Reset
			print("exception caught")
			resetDistanceSensor()
			return ReadDistance()
		
		if(distance > 2000):
			#exception Caught Reset
			print("exception caught")
			resetDistanceSensor()
			return ReadDistance()

	return distance
	
while(True):
	maxDistance = 30
	distance = ReadDistance()
	print(distance)
	
	if(distance > maxDistance):
		pi_pwm.ChangeDutyCycle(0)	
	else:
		if(distance > 0):
			closeness = int(round( (100-(distance/maxDistance)*100) ,0) )
			pi_pwm.ChangeDutyCycle(closeness)	
	time.sleep(0.1)

GPIO.cleanup()
