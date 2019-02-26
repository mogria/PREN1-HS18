from picamera import PiCamera
from time import sleep
import io
import time
from PIL import Image
import datetime

t1 = datetime.datetime.now()

camera = PiCamera()
camera.resolution = (640, 360)
#camera.framerate = 50
camera.shutter_speed = 500
camera.iso = 1600
import datetime

#camera.awb_mode = 'off'

#camera.start_preview()
#sleep(2)
#try:
#    for i in range(100,101):
#        camera.capture('/home/pi/Schreibtisch/test/fahrend_' + str(i) + '.jpg')
#    
#finally:
#    camera.stop_preview()
count = 300
# Set up 40 in-memory streams
outputs = [io.BytesIO() for i in range(count)]
start = time.time()
camera.capture_sequence(outputs, 'jpeg', use_video_port=True)
# for filename in camera.capture_continuous('/home/pi/testcase-2/img{timestamp:%Y-%m-%d-%H-%M-%S-%f}.jpg', use_video_port=True):
#     print('Captured %s' % filename)
finish = time.time()
# How fast were we?
print('Captured '+ str(count) +' images at %.2ffps' % (count / (finish - start)))

for test in outputs:
    count = count + 1
    test.seek(0)
    image = Image.open(test)
    image.save('/home/pi/testcase-2/fahrend_' + str(datetime.datetime.now()) + '.jpg')

t2 = datetime.datetime.now()
delta = t2 - t1
delta.total_seconds()
print(delta)

exit()
