# THIS SCRIPT IS BASED ON:
# https://github.com/simonmonk/raspberrypi_cookbook_ed3/blob/master/python/ch_08_detect_motion.py

import datetime
import os
import uuid
from threading import Thread
from typing import Any, Tuple

# TODO AEO remove for cv2 and numpy
# noinspection PyUnresolvedReferences
import cv2
# noinspection PyUnresolvedReferences
import numpy as np
# noinspection PyUnresolvedReferences
from imutils import resize
# noinspection PyUnresolvedReferences
from imutils.video import VideoStream

print('Script Executing...')

diff_threshold = 500000
script_directory = os.path.dirname(os.path.abspath(__file__))
images_folder = os.path.join(script_directory, 'simple_motion_images')
image_file_prefix = 'motion'
image_file_suffix_old = '0-old'
image_file_suffix = '1-new'
save_raw_enabled = False
save_old_enabled = True
log_only = False

if not os.path.exists(images_folder):
    os.makedirs(images_folder)

print('Begin Video Stream')

vs = VideoStream(src=0).start()


def get_image() -> Tuple[Any, Any]:
    raw_image = vs.read()
    my_image = cv2.cvtColor(raw_image, cv2.COLOR_BGR2GRAY)
    my_image = cv2.blur(my_image, (20, 20))
    # print('raw_image is:', type(raw_image), 'my_image is:', type(my_image))
    return my_image, raw_image


def save_image(new_image: Any, diff_score: Any, timestamp_filename: str, suffix: str = image_file_suffix) -> None:
    diff_score_formatted = '{0:,d}'.format(diff_score).replace(',', '.')
    filename = f'{image_file_prefix}-{timestamp_filename}-{diff_score_formatted}-{suffix}-{str(uuid.uuid4())[:8]}.jpg'
    print(f'filename:{filename}')
    if log_only:
        return
    image_full_path = os.path.join(images_folder, filename)
    cv2.imwrite(image_full_path, new_image)


def main() -> None:
    print('Get First Image')

    prior_saved = False
    old_image, _ = get_image()

    print('Monitoring for Motion!')

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
                # save_image(raw_image, diff_score, timestamp_filename)
                thread = Thread(target=save_image, args=(raw_image, diff_score, timestamp_filename))
                thread.start()
            else:
                # save_image(new_image, diff_score, timestamp_filename)
                if not prior_saved and save_old_enabled:
                    thread0 = Thread(target=save_image, args=(old_image, diff_score, timestamp_filename,
                                                              image_file_suffix_old))
                    thread0.start()
                thread = Thread(target=save_image, args=(new_image, diff_score, timestamp_filename))
                thread.start()
            prior_saved = True
        else:
            prior_saved = False

        old_image = new_image


if __name__ == '__main__':
    main()
