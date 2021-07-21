import datetime
import json
import os
import uuid
from fractions import Fraction
from time import sleep

# noinspection PyUnresolvedReferences
import picamera

CONFIG_FILE = 'dre_moe_config.json'

# TODO AEO NEXT: create LOG utility with LEVEL(INFO, DEBUG, STATUS, WARN, ERROR) and OUTPUT (print, file) options
# defer and add to Notion board?


class Camera:

    def __init__(self):
        self.script_directory = os.path.dirname(os.path.abspath(__file__))

        with open(os.path.join(self.script_directory, CONFIG_FILE)) as json_file:
            self.config = json.load(json_file)

    def _setup_camera(self, camera) -> None:

        self._log('Setup PiCamera')
        resolution_width = self.config['resolution_width']
        resolution_height = self.config['resolution_height']
        camera.rotation = self.config['rotation']
        camera.resolution = (resolution_width, resolution_height)
        camera.led = False

        if self.config['enable_manual_mode']:
            # useful for low light settings
            # ex: framerate range (Fraction(1, 6), Fraction(30, 1)) allows slow shutter speed
            camera.iso = self.config['manual_iso']
            framerate_range_from = Fraction(self.config['manual_framerate_range_from'])
            framerate_range_to = Fraction(self.config['manual_framerate_range_to'])
            camera.framerate_range = (framerate_range_from, framerate_range_to)
            camera.shutter_speed = self.config['manual_shutter_speed']

        self._print_camera_settings(camera)

    def _print_camera_settings(self, camera):

        if not self.config['print_camera_settings']:
            return

        self._log('CAMERA SETTINGS:')
        self._log(f'shutter speed\t\t\t{camera.shutter_speed}')
        self._log(f'exposure speed\t\t\t{camera.exposure_speed}')
        self._log(f'brightness\t\t\t{camera.brightness}')
        self._log(f'exposure_compensation\t\t{camera.exposure_compensation}')
        self._log(f'awb_mode\t\t\t{camera.awb_mode}')
        self._log(f'exposure_mode\t\t\t{camera.exposure_mode}')
        self._log(f'framerate\t\t\t{camera.framerate}')
        self._log(f'framerate_range\t\t\t{camera.framerate_range}')

    def _capture_image(self, camera, directory_path: str) -> None:

        # allow awb to catch up
        awb_delay = self.config['awb_delay']
        self._log(f'AWB Delay for {awb_delay} seconds')
        sleep(awb_delay)

        self._log('Taking Photo...')
        if self.config['show_timestamp']:
            camera.annotate_background = picamera.Color('black')
            camera.annotate_text = self._get_timestamp()

        image_file = self.config['image_file']
        time_suffix = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        filename = f'{image_file}-{time_suffix}-{str(uuid.uuid4())[:8]}.jpg'
        filepath = os.path.join(directory_path, filename)

        camera.capture(filepath)

        self._log('Photo Complete')

    def _do_motion_capture(self):

        # setup directory and output format
        main_directory = self.config['main_directory']
        subdirectory = datetime.datetime.now().strftime('%Y/%m/%d')
        directory_path = os.path.join(self.script_directory, main_directory, subdirectory)

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
                self._log('Camera Closed')

        wait_time = self.config['wait_time']
        self._log(f'sleeping for {wait_time} seconds')
        sleep(wait_time)

    def start_motion_capture_loop(self):

        do_loop = self.config['do_loop']

        while True:
            self._do_motion_capture()

            if not do_loop:
                break

    def _get_timestamp(self):
        return datetime.datetime.now().strftime(self.config['timestamp_format'])

    def _log(self, message: str):
        print(f'{self._get_timestamp()}\t{message}')