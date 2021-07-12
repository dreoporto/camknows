import datetime
import os
# import sys    # TODO AEO TEMP
import uuid
from fractions import Fraction
from time import sleep

# noinspection PyUnresolvedReferences
import picamera

# CAMERA / APP CONFIG SETTINGS
MAIN_DIRECTORY = 'media-files'
IMAGE_FILE = 'dre-moe'
WAIT_TIME = 2  # TODO AEO TEMP
LOOP = False  # TODO AEO TEMP
AWB_DELAY = 3  # allow awb to catch up
RESOLUTION = (2592, 1944)
SHOW_TIMESTAMP = True

# low light config settings
ISO = 640
# default is 30 (30 fps); USE RANGE INSTEAD
# camera.framerate = Fraction(1, 8)
FRAMERATE_RANGE = (Fraction(1, 6), Fraction(30, 1))
SHUTTER_SPEED = 125000


def capture_image(path: str) -> None:

    print(f'{get_timestamp()}\tSetup PiCamera')
    camera = picamera.PiCamera()
    camera.resolution = RESOLUTION
    camera.led = False

    if SHOW_TIMESTAMP:
        camera.annotate_background = picamera.Color('black')
        camera.annotate_text = get_timestamp()

    camera.iso = ISO
    camera.framerate_range = FRAMERATE_RANGE
    camera.shutter_speed = SHUTTER_SPEED

    # print camera settings
    print(f'{get_timestamp()}\tCAMERA SETTINGS:')
    print('shutter speed:', camera.shutter_speed)
    print('exposure speed:', camera.exposure_speed)
    print('brightness', camera.brightness)
    print('exposure_compensation', camera.exposure_compensation)
    print('awb_mode', camera.awb_mode)
    print('exposure_mode', camera.exposure_mode)
    print('framerate', camera.framerate)
    print('framerate_range', camera.framerate_range)

    try:
        print(f'{get_timestamp()}\tAWB Delay for {AWB_DELAY} seconds')
        sleep(AWB_DELAY)
        print(f'{get_timestamp()}\tTaking Photo...')
        camera.capture(path)
        print(f'{get_timestamp()}\tPhoto Complete')
    finally:
        camera.close()
        print(f'{get_timestamp()}\tCamera Closed')


def get_timestamp():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def do_motion_capture():

    # setup directory and output format
    subdirectory = datetime.datetime.now().strftime('%Y/%m/%d')
    time_suffix = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    directory_path = os.path.join(MAIN_DIRECTORY, subdirectory)

    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    # i like guids
    filename = f'{IMAGE_FILE}-{time_suffix}-{str(uuid.uuid4())[:8]}.jpg'
    filepath = os.path.join(directory_path, filename)

    # print(f'{get_timestamp()}\tCLICK!\tnext photo in {WAIT_TIME} seconds...')  # , end='\r\r')
    # sys.stdout.flush()

    capture_image(filepath)

    print(f'{get_timestamp()}\tsleeping for {WAIT_TIME} seconds')
    sleep(WAIT_TIME)


def main() -> None:

    while True:
        do_motion_capture()

        if not LOOP:
            break


if __name__ == '__main__':
    main()
