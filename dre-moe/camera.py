import datetime
import json
import logging
import os
import time
import traceback
import uuid
from fractions import Fraction
from logging.handlers import TimedRotatingFileHandler
from threading import Thread
from time import sleep
from typing import Any

import cv2
import numpy as np
import picamera

CONFIG_FILE = 'dre_moe_config.json'
LOG_FILE = 'dre_moe.log'
LOG_FILE_SUFFIX = '%Y%m%d'


class Camera:

    def __init__(self):
        self.script_directory = os.path.dirname(os.path.abspath(__file__))
        self.logger = self._setup_logger()

        with open(os.path.join(self.script_directory, CONFIG_FILE)) as json_file:
            self.config = json.load(json_file)

        self.last_image_time: float
        self.last_setup_time: float = 0
        self.previous_processed_image: Any = None
        self.diff_threshold: int = self.config['diff_threshold']
        self.resolution_width: int = self.config['resolution_width']
        self.resolution_height: int = self.config['resolution_height']

    def _setup_logger(self) -> Any:
        logs_directory = os.path.join(self.script_directory, "logs")

        if not os.path.exists(logs_directory):
            os.makedirs(logs_directory)

        logger = logging.getLogger(__name__)
        handler = TimedRotatingFileHandler(os.path.join(logs_directory, LOG_FILE), when="midnight", interval=1)
        handler.suffix = LOG_FILE_SUFFIX
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

        return logger

    def start_camera_loop(self) -> None:

        do_loop = self.config['do_loop']

        with picamera.PiCamera() as camera:

            try:
                while True:
                    self._run_camera(camera)

                    if not do_loop:
                        break
            except Exception:
                self._log(traceback.format_exc(), logging.ERROR)
            finally:
                camera.close()
                self._log('Camera Closed')

    def _run_camera(self, camera: Any) -> None:

        try:
            self._setup_camera(camera)
            self._capture_image_with_motion_detection(camera)
        except Exception:
            self._log(traceback.format_exc(), logging.ERROR)

        wait_time = self.config['wait_time']
        self._log(f'sleeping for {wait_time} seconds')
        sleep(wait_time)

    def _setup_camera(self, camera: Any) -> None:

        if (self.config['setup_timeout_seconds'] != 0
                and time.time() - self.last_setup_time <= self.config['setup_timeout_seconds']):
            # setup timeout configured, and not expired; skip setup
            return

        self._log('Setup PiCamera', logging.INFO)
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
            # TODO AEO DISABLE FOR NOW camera.shutter_speed = self.config['manual_shutter_speed']
            camera.awb_mode = self.config['manual_awb_mode']
            camera.awb_gains = (self.config['manual_awb_gains_red'], self.config['manual_awb_gains_blue'])

        # allow awb to catch up
        awb_delay = self.config['awb_delay']
        self._log(f'AWB Delay for {awb_delay} seconds', logging.INFO)
        sleep(awb_delay)

        self._print_camera_settings(camera)
        self.last_setup_time = time.time()

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

    def _capture_image_with_motion_detection(self, camera: Any) -> None:

        perf_start_time = time.perf_counter()

        self._log('Capturing Image...')
        if self.config['show_image_timestamp']:
            camera.annotate_background = picamera.Color('black')
            camera.annotate_text = self._get_timestamp()
            camera.annotate_text_size = self.config['image_timestamp_text_size']

        # capturing this now: we want exact times for file and image timestamps
        timestamp_filename = datetime.datetime.now().strftime(self.config['timestamp_filename_format'])

        image_array = np.empty((self.resolution_height * self.resolution_width * 3,), dtype=np.uint8)
        camera.capture(image_array, 'bgr', use_video_port=self.config['use_video_port'])
        image_array = image_array.reshape((self.resolution_height, self.resolution_width, 3))

        self._log(f'Image Capture Complete')
        self._log(f'Elapsed Seconds: {time.perf_counter() - perf_start_time:0.4f}')

        self._check_for_motion(image_array, timestamp_filename)

    def _check_for_motion(self, image_array: Any, timestamp_filename: str) -> None:

        perf_start_time = time.perf_counter()

        self._log('Check for motion...')

        processed_image = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
        processed_image = cv2.blur(processed_image, (20, 20))

        if self.previous_processed_image is None:
            # save and set first image!
            self._log(f'saving first image', logging.INFO)
            self._save_image_from_motion(image_array, timestamp_filename)
            self.previous_processed_image = processed_image
            return

        images_diff = cv2.absdiff(self.previous_processed_image, processed_image)
        diff_score = np.sum(images_diff)

        if diff_score > self.diff_threshold:
            self._log(f'motion detected; diff score:{diff_score:,d}', logging.INFO)
            self._save_image_from_motion(image_array, timestamp_filename, processed_image, diff_score)
        elif (self.config['time_lapse_seconds'] != 0
              and time.time() - self.last_image_time > self.config['time_lapse_seconds']):
            # we will also save the image if the time lapse is set and expired
            self._log(f'time elapsed; saving image', logging.INFO)
            self._save_image_from_motion(image_array, timestamp_filename)

        self.previous_processed_image = processed_image

        self._log(f'Motion Check Complete')
        self._log(f'Elapsed Seconds: {time.perf_counter() - perf_start_time:0.4f}')

    def _save_image_from_motion(self, image_array: Any, timestamp_filename: str, processed_image_array: Any = None,
                                diff_score: Any = None):

        # setup directory and output format
        main_directory = self.config['main_directory']
        subdirectory = datetime.datetime.now().strftime('%Y/%m/%d')
        directory_path = os.path.join(self.script_directory, main_directory, subdirectory)

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        image_file_prefix = self.config['image_file_prefix']
        diff_score_in_filename = self.config['diff_score_in_filename']
        image_file_suffix: str = (str(uuid.uuid4())[:8] if (diff_score is None or not diff_score_in_filename)
                                  else '{0:,d}'.format(diff_score).replace(',', '.'))
        filename = f'{image_file_prefix}-{timestamp_filename}-{image_file_suffix}.jpg'
        image_full_path = os.path.join(directory_path, filename)

        self._write_image_file_async(image_full_path, image_array)
        self.last_image_time = time.time()

        self._save_processed_images(directory_path, filename, processed_image_array)

    def _save_processed_images(self, directory_path: str, filename: str, processed_image_array: Any) -> None:
        """
        save processed images if debug enabled
        """
        if not self.config['enable_image_debugging'] or processed_image_array is None:
            return

        processed_directory_path = os.path.join(directory_path, 'processed')

        if not os.path.exists(processed_directory_path):
            os.makedirs(processed_directory_path)

        processed_image_path = os.path.join(processed_directory_path, filename)

        self._write_image_file_async(processed_image_path.replace('.jpg', '_p0.jpg'), self.previous_processed_image)
        self._write_image_file_async(processed_image_path.replace('.jpg', '_p1.jpg'), processed_image_array)

    def _write_image_file_async(self, image_full_path: str, image_array: Any) -> None:
        """
        use threading to write image file and avoid disk io delay
        """
        self._log(f'Writing file:{image_full_path}')

        image_data = image_array.copy()
        thread = Thread(target=cv2.imwrite, args=(image_full_path, image_data))
        thread.start()

        self._log(f'File created:{image_full_path.split("/")[-1]}')

    def _get_timestamp(self) -> str:
        return datetime.datetime.now().strftime(self.config['timestamp_format'])

    def _log(self, message: str, level=logging.NOTSET) -> None:
        if level == logging.NOTSET:
            return
        formatted_message = f'{self._get_timestamp()}\t{message}'
        self.logger.log(level, formatted_message)
        print(formatted_message)
