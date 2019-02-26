import RPi.GPIO as GPIO
import time
import threading


class HC_SR04:
    def __init__(self):
        GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(GPIO_ECHO, GPIO.IN)
        self.start_time = None
        self.end_time = None
        self.measure_lock = threading.Condition()

    def measure_time_to_distance(self, measure_time):
        # multiply with speed of sound (34300 cm/s)
        # and division by two
        return (measure_time * 34300.0) / 2

    def distance_to_measure_time(self, measure_time):
        return (measure_time * 2.0) / 34300

    def trigger_measurement(self, max_measure_time):
        # set Trigger High
        GPIO.output(GPIO_TRIGGER, True)
        # set Trigger after 0.1ms low
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)

        print("register start measurement")
        # register callback for saving start time of measurement
        start_measurement = lambda x: self.measurement_started(max_measure_time)
        GPIO.remove_event_detect(GPIO_ECHO)
        GPIO.add_event_detect(GPIO_ECHO, GPIO.FALLING, callback=start_measurement)

    def measurement_started(self, max_measure_time):
        print("setting measuring = true")
        self.measure_lock.acquire()
        self.end_time = None
        self.start_time = time.time()
        self.measure_lock.notifyAll()
        self.measure_lock.release()

        # setup timeout
        print("timeout timer started %f s" % max_measure_time)

        # register callback for saving end time of measurement
        GPIO.remove_event_detect(GPIO_ECHO)
        GPIO.add_event_detect(GPIO_ECHO, GPIO.RISING, callback=self.measurement_ended)
        print("register end measurement trigger")

    def measurement_ended(self, event):
        print("measurement complete")
        self.measure_lock.acquire()
        self.end_time = time.time()
        self.measure_lock.notifyAll()
        self.measure_lock.release()
        print("measurement end time set")

    # max measure distance is in cm
    def distance(self, max_measure_distance):
        max_measure_time = self.distance_to_measure_time(max_measure_distance)

        self.trigger_measurement(max_measure_time)

        print("waiting for measureement")
        while True:
            self.measure_lock.acquire()
                self.measure_lock.release()
            if self.start_time is None:
                # print("measurement not yet started")
                self.measure_lock.release()
                continue
            
            time_elapsed = time.time() - self.start_time
            if time_eleapsed > max_measure_time:
                print("measurement done")
                if self.end_time is None:
                    self.measure_lock.release()
                    return None

                # elapsed time
                time_elapsed = self.end_time - self.start_time
                distance = measure_time_to_distance(time_elapsed)
                self.measure_lock.release()

            self.measure_lock.release()


if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO_TRIGGER = 16
    GPIO_ECHO = 18

    sensor = HC_SR04()
    while True:
        dist = sensor.distance(8)
        if dist is None:
            # print ("Entfernung zu gross")
            pass
        else:
            print ("Entfernung = %.1f cm" % dist)
        # time.sleep(0.1)
     

