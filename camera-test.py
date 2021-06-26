from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.led = False

# print('start preview')
# camera.start_preview()

print('taking photo in 3 seconds...')
sleep(3)

# print('stop preview')
# camera.stop_preview()

print('CLICK!')
camera.capture('foo.jpg')

print('taking video in 3 seconds...')
sleep(3)

camera.start_recording('foo.h264')
camera.wait_recording(10)
camera.stop_recording()

camera.close()
