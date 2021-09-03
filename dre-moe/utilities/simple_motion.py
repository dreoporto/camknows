# THIS SCRIPT IS BASED ON:
# https://github.com/simonmonk/raspberrypi_cookbook_ed3/blob/master/python/ch_08_detect_motion.py

import datetime
import os
import uuid
from time import sleep
from threading import Thread
from typing import Any, Tuple

import cv2
import numpy as np
from imutils import resize
from imutils.video import VideoStream

print('Script Executing...')

diff_threshold = 500000
script_directory = os.path.dirname(os.path.abspath(__file__))
images_folder = os.path.join(script_directory, 'simple_motion_images')
image_file_prefix = 'motion'
image_file_suffix_old = '0-old'
image_file_suffix = '1-new'
save_raw_enabled = True
save_old_enabled = True
log_only = False
resolution_width = 640
resolution_height = 480
video_framerate = 32

if not os.path.exists(images_folder):
    os.makedirs(images_folder)

print('Begin Video Stream')

vs = VideoStream(src=0, usePiCamera=True, resolution=(resolution_width, resolution_height),
                 framerate=video_framerate).start()
# allow for camera warmup
sleep(3)


def get_image() -> Tuple[Any, Any]:
    raw_image = vs.read()
    my_image = cv2.cvtColor(raw_image, cv2.COLOR_BGR2GRAY)
    my_image = cv2.blur(my_image, (20, 20))
    # print('raw_image is:', type(raw_image), 'my_image is:', type(my_image))
    return my_image, raw_image


def save_image(new_image: Any, diff_score: Any, timestamp_filename: str, suffix: str = image_file_suffix) -> None:
    diff_score_formatted = '{0:,d}'.format(diff_score).replace(',', '.')
    filename = f'{image_file_prefix}-{timestamp_filename}-{diff_score_formatted}-{suffix}-{str(uuid.uuid4())[:8]}.jpg'
    print(f'Saving File: {filename}')
    if log_only:
        return
    image_full_path = os.path.join(images_folder, filename)
    # use threading for disk io latency
    image_data = new_image.copy()
    thread = Thread(target=cv2.imwrite, args=(image_full_path, image_data))
    thread.start()


def main() -> None:
    print('Get First Image')

    prior_saved = False  # avoids saving redundant images for prior/old image
    old_image, _ = get_image()

    print('Monitoring for Motion')

    while True:
        new_image, raw_image = get_image()
        # print('new_image is:', type(new_image))  # , 'raw_image is:', type(raw_image))

        diff = cv2.absdiff(old_image, new_image)
        diff_score = np.sum(diff)
        # print(diff_score)

        if diff_score > diff_threshold:
            # print(f"Movement detected; Diff Score:{diff_score}")
            timestamp_filename = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
            if save_raw_enabled:
                save_image(raw_image, diff_score, timestamp_filename)
            else:
                if not prior_saved and save_old_enabled:
                    save_image(old_image, diff_score, timestamp_filename, image_file_suffix_old)
                save_image(new_image, diff_score, timestamp_filename)
            prior_saved = True
        else:
            prior_saved = False

        old_image = new_image


if __name__ == '__main__':
    main()
