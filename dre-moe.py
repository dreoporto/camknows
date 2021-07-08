import datetime
import os
import sys
import uuid
from fractions import Fraction
from time import sleep

# noinspection PyUnresolvedReferences
from picamera import PiCamera

MAIN_DIRECTORY = 'media-files'
IMAGE_FILE = 'dre-moe'
WAIT_TIME = 2  # TODO AEO TEMP
LOOP = False  # TODO AEO TEMP


def capture_image(path: str) -> None:
    # camera = PiCamera()
    camera = PiCamera(resolution=(2592, 1944), framerate=Fraction(1, 8))
    # camera.resolution = (2592, 1944)
    camera.led = False
    # camera.awb_mode = 'off'
    camera.iso = 640
    camera.shutter_speed = 125000
    # camera.framerate = 8

    # camera.shutter_speed = camera.exposure_speed
    # camera.exposure_mode = 'sports'

    print('shutter speed:', camera.shutter_speed)
    print('exposure speed:', camera.exposure_speed)
    print('brightness', camera.brightness)
    print('exposure_compensation', camera.exposure_compensation)
    print('awb_mode', camera.awb_mode)
    print('exposure_mode', camera.exposure_mode)
    print('framerate', camera.framerate)

    try:
        camera.capture(path)
    finally:
        camera.close()


def do_motion_capture():

    # setup directory and output format
    subdirectory = datetime.datetime.now().strftime('%Y/%m/%d')
    display_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    time_suffix = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    directory_path = os.path.join(MAIN_DIRECTORY, subdirectory)

    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    # i like guids
    filename = f'{IMAGE_FILE}-{time_suffix}-{uuid.uuid4()}.jpg'
    filepath = os.path.join(directory_path, filename)

    print(f'{display_time}\tCLICK!\tnext photo in {WAIT_TIME} seconds...')  # , end='\r\r')
    sys.stdout.flush()

    capture_image(filepath)

    sleep(WAIT_TIME)


def main() -> None:

    while True:
        do_motion_capture()

        if not LOOP:
            break


if __name__ == '__main__':
    main()
