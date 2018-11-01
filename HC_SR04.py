import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO_TRIGGER = 16
GPIO_ECHO = 18

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def measure_time_to_distance(measure_time):
    # multiply with speed of sound (34300 cm/s)
    # and division by two
    return (measure_time * 34300.0) / 2

def distance_to_measure_time(measure_time):
    return (measure_time * 2.0) / 34300

def distance(maxMeasureDistance):
    # We CANNOT measure faster than 60ms, because
    # then the ECHO signal gets fucked up (from the datasheet)
    maxMeasureTime = 0.060 #  distance_to_measure_time(maxMeasureDistance)
    print("maxMeasureTime = %f" % maxMeasureTime)
    # set Trigger High
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.1ms low
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    startTime = time.time()
    endTime = time.time()
 
    # store start time
    while GPIO.input(GPIO_ECHO) == 0:
        startTime = time.time()
 
    # store arrival
    while GPIO.input(GPIO_ECHO) == 1:
        endTime = time.time()
        timeElapsed = endTime - startTime
        if timeElapsed > maxMeasureTime:
            return None
 
    # elapsed time
    timeElapsed = endTime - startTime
    # multiply with speed of sound (34300 cm/s)
    # and division by two
    distance = measure_time_to_distance(timeElapsed)
 
    return distance
 

while True:
    dist = distance(8)
    distances = [ distance(8) for i in xrange(10) ]
    if dist is not None:
        print ("Entfernung = %.1f cm" % dist)
    # time.sleep(0.5)
 

