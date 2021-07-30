import datetime
import json
import os
import sys
import time
import uuid
from fractions import Fraction
from time import sleep
from typing import Any

# TODO AEO remove for cv2 and numpy
# noinspection PyUnresolvedReferences
import cv2
# noinspection PyUnresolvedReferences
import numpy as np
# noinspection PyUnresolvedReferences
import picamera

CONFIG_FILE = 'dre_moe_config.json'

# TODO AEO add python logging in place of print usage


# noinspection PyBroadException
class Camera:

    def __init__(self):
        self.script_directory = os.path.dirname(os.path.abspath(__file__))

        with open(os.path.join(self.script_directory, CONFIG_FILE)) as json_file:
            self.config = json.load(json_file)

        self.last_image_time: float
        self.previous_processed_image: Any = None
        self.diff_threshold: int = self.config['diff_threshold']
        self.resolution_width: int = self.config['resolution_width']
        self.resolution_height: int = self.config['resolution_height']

    def _setup_camera(self, camera: Any) -> None:

        self._log('Setup PiCamera')
        camera.rotation = self.config['rotation']
        camera.resolution = (self.resolution_width, self.resolution_height)
        camera.led = self.config['enable_led']

        if self.config['enable_manual_mode']:
            # useful for consistent images and low light settings
            # ex: framerate range (Fraction(1, 6), Fraction(30, 1)) allows for slower shutter speeds for low light
            camera.iso = self.config['manual_iso']
            framerate_range_from = Fraction(self.config['manual_framerate_range_from'])
            framerate_range_to = Fraction(self.config['manual_framerate_range_to'])
            camera.framerate_range = (framerate_range_from, framerate_range_to)
            camera.shutter_speed = self.config['manual_shutter_speed']
            camera.awb_mode = self.config['manual_awb_mode']
            camera.awb_gains = (self.config['manual_awb_gains_red'], self.config['manual_awb_gains_blue'])

        self._print_camera_settings(camera)

    def _print_camera_settings(self, camera: Any) -> None:

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
        self._log(f'awb_mode:\t\t\t{camera.awb_mode}')
        self._log(f'awb_gains:\t\t\t{camera.awb_gains}')

    def _capture_image(self, camera: Any) -> None:

        # allow awb to catch up
        awb_delay = self.config['awb_delay']
        self._log(f'AWB Delay for {awb_delay} seconds')
        sleep(awb_delay)

        self._log('Capturing Image...')
        if self.config['show_timestamp']:
            camera.annotate_background = picamera.Color('black')
            camera.annotate_text = self._get_timestamp()

        # capturing this now: we want exact times for file and image timestamps
        timestamp_filename = datetime.datetime.now().strftime(self.config['timestamp_filename_format'])

        image_array = np.empty((self.resolution_height * self.resolution_width * 3,), dtype=np.uint8)
        camera.capture(image_array, 'bgr')
        image_array = image_array.reshape((self.resolution_height, self.resolution_width, 3))
        self._check_for_motion(image_array, timestamp_filename)

        self._log('Image Capture Complete')

    def _check_for_motion(self, image_array: Any, timestamp_filename: str) -> None:

        processed_image = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
        processed_image = cv2.blur(processed_image, (20, 20))

        if self.previous_processed_image is None:
            # save first image!
            self._save_image_from_motion(image_array, timestamp_filename)
            self.previous_processed_image = processed_image
            return

        images_diff = cv2.absdiff(self.previous_processed_image, processed_image)
        diff_score = np.sum(images_diff)

        if diff_score > self.diff_threshold:
            self._log(f'motion detected:{self._get_timestamp()}\tdiff score:{diff_score}')
            self._save_image_from_motion(image_array, timestamp_filename)
        elif (self.config['time_lapse_seconds'] != 0
              and time.time() - self.last_image_time > self.config['time_lapse_seconds']):
            # we will also save the image if the time lapse is set and expired
            self._log(f'time elapsed:{self._get_timestamp()}')
            self._save_image_from_motion(image_array, timestamp_filename)

        self.previous_processed_image = processed_image

    def _save_image_from_motion(self, image_array: Any, timestamp_filename: str):

        # setup directory and output format
        main_directory = self.config['main_directory']
        subdirectory = datetime.datetime.now().strftime('%Y/%m/%d')
        directory_path = os.path.join(self.script_directory, main_directory, subdirectory)

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        image_file_prefix = self.config['image_file_prefix']
        filename = f'{image_file_prefix}-{timestamp_filename}-{str(uuid.uuid4())[:8]}.jpg'
        image_full_path = os.path.join(directory_path, filename)

        self._log(f'Writing file:{image_full_path}')
        cv2.imwrite(image_full_path, image_array)
        # debugging only!
        # cv2.imwrite(image_file.replace('.', '_p0.'), processed_image)
        # cv2.imwrite(image_file.replace('.', '_p1.'), self.previous_processed_image)

        self._log(f'File created:{filename.split("/")[-1]}')
        self.last_image_time = time.time()

    def _shoot_camera(self, camera: Any) -> None:

        try:
            self._setup_camera(camera)
            self._capture_image(camera)
        except Exception:
            self._log(str(sys.exc_info()))

        wait_time = self.config['wait_time']
        self._log(f'sleeping for {wait_time} seconds')
        sleep(wait_time)

    def start_camera_loop(self) -> None:

        do_loop = self.config['do_loop']

        with picamera.PiCamera() as camera:

            try:
                while True:
                    self._shoot_camera(camera)

                    if not do_loop:
                        break
            except Exception:
                self._log(str(sys.exc_info()))
            finally:
                camera.close()
                self._log('Camera Closed')

    def _get_timestamp(self) -> str:
        return datetime.datetime.now().strftime(self.config['timestamp_format'])

    def _log(self, message: str) -> None:
        print(f'{self._get_timestamp()}\t{message}')
