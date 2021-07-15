import datetime
import json
import os
import uuid
from fractions import Fraction
from time import sleep

# noinspection PyUnresolvedReferences
import picamera

CONFIG_FILE = 'dre-moe-config.json'

# TODO AEO NEXT: change most PRINTs to LOG to allow disable/level


class Camera:

    def __init__(self):
        with open(CONFIG_FILE) as json_file:
            self.config = json.load(json_file)

    def _setup_camera(self, camera) -> None:

        print(f'{self.get_timestamp()}\tSetup PiCamera')
        resolution_width = self.config['resolution_width']
        resolution_height = self.config['resolution_height']
        camera.resolution = (resolution_width, resolution_height)
        camera.led = False

        # low light settings
        camera.iso = self.config['iso']
        # (Fraction(1, 6), Fraction(30, 1))
        framerate_range_from = Fraction(self.config['framerate_range_from'])
        framerate_range_to = Fraction(self.config['framerate_range_to'])
        camera.framerate_range = (framerate_range_from, framerate_range_to)
        camera.shutter_speed = self.config['shutter_speed']

        self.print_camera_settings(camera)

    def print_camera_settings(self, camera):

        if not self.config['print_camera_settings']:
            return

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

        # allow awb to catch up
        awb_delay = self.config['awb_delay']
        print(f'{self.get_timestamp()}\tAWB Delay for {awb_delay} seconds')
        sleep(awb_delay)

        print(f'{self.get_timestamp()}\tTaking Photo...')
        if self.config['show_timestamp']:
            camera.annotate_background = picamera.Color('black')
            camera.annotate_text = self.get_timestamp()

        image_file = self.config['image_file']
        time_suffix = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        filename = f'{image_file}-{time_suffix}-{str(uuid.uuid4())[:8]}.jpg'
        filepath = os.path.join(directory_path, filename)

        camera.capture(filepath)

        print(f'{self.get_timestamp()}\tPhoto Complete')

    def _do_motion_capture(self):

        # setup directory and output format
        main_directory = self.config['main_directory']
        subdirectory = datetime.datetime.now().strftime('%Y/%m/%d')
        directory_path = os.path.join(main_directory, subdirectory)

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

        wait_time = self.config['wait_time']
        print(f'{self.get_timestamp()}\tsleeping for {wait_time} seconds')
        sleep(wait_time)

    def start_motion_capture_loop(self):

        do_loop = self.config['do_loop']

        while True:
            self._do_motion_capture()

            if not do_loop:
                break

    def get_timestamp(self):
        return datetime.datetime.now().strftime(self.config['timestamp_format'])
