import datetime
import json
import os
# import sys    # TODO AEO TEMP
import uuid
from fractions import Fraction
from time import sleep

# noinspection PyUnresolvedReferences
import picamera

CONFIG_FILE = 'dre-moe-config.json'
# TODO AEO NEXT: move config settings to JSON
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

# TODO AEO NEXT: change most PRINTs to LOG to allow disable/level


class Camera:

    # def __init__(self):
    #     with open(CONFIG_FILE) as json_file:
    #         self.config = json.load(json_file)

    def _setup_camera(self, camera) -> None:

        print(f'{self.get_timestamp()}\tSetup PiCamera')
        camera.resolution = RESOLUTION
        camera.led = False

        camera.iso = ISO
        camera.framerate_range = FRAMERATE_RANGE
        camera.shutter_speed = SHUTTER_SPEED

        # print camera settings
        print(f'{self.get_timestamp()}\tCAMERA SETTINGS:')
        print('shutter speed:', camera.shutter_speed)
        print('exposure speed:', camera.exposure_speed)
        print('brightness', camera.brightness)
        print('exposure_compensation', camera.exposure_compensation)
        print('awb_mode', camera.awb_mode)
        print('exposure_mode', camera.exposure_mode)
        print('framerate', camera.framerate)
        print('framerate_range', camera.framerate_range)

    def _capture_image(self, camera, directory_path: str) -> None:

        print(f'{self.get_timestamp()}\tAWB Delay for {AWB_DELAY} seconds')
        sleep(AWB_DELAY)

        print(f'{self.get_timestamp()}\tTaking Photo...')
        if SHOW_TIMESTAMP:
            camera.annotate_background = picamera.Color('black')
            camera.annotate_text = self.get_timestamp()

        time_suffix = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        filename = f'{IMAGE_FILE}-{time_suffix}-{str(uuid.uuid4())[:8]}.jpg'
        filepath = os.path.join(directory_path, filename)

        camera.capture(filepath)

        print(f'{self.get_timestamp()}\tPhoto Complete')

    def _do_motion_capture(self):

        # setup directory and output format
        subdirectory = datetime.datetime.now().strftime('%Y/%m/%d')
        directory_path = os.path.join(MAIN_DIRECTORY, subdirectory)

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        with picamera.PiCamera() as camera:
            try:
                self._setup_camera(camera)
                self._capture_image(camera, directory_path)
            # except:
            # TODO AEO log error
            finally:
                camera.close()
                print(f'{self.get_timestamp()}\tCamera Closed')

        print(f'{self.get_timestamp()}\tsleeping for {WAIT_TIME} seconds')
        sleep(WAIT_TIME)

    def start_motion_capture_loop(self):

        while True:
            self._do_motion_capture()

            if not LOOP:
                break

    # noinspection PyMethodMayBeStatic
    def get_timestamp(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
