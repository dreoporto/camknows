import os
import sys
from typing import List, Tuple, Optional

import cv2
import numpy as np

SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


class Motion:

    def __init__(self):
        self.diff_threshold = 3000000

    def detect_motion_from_images(self, directory: str, extension: str) -> None:

        images_directory = os.path.join(SCRIPT_DIRECTORY, directory)
        images_list: List[str] = []

        if not os.path.exists(images_directory):
            print('Invalid directory:', images_directory)
            return

        for file_name in os.listdir(images_directory):
            if file_name.endswith(f'.{extension}'):
                images_list.append(file_name)

        images_list.sort()
        image_count = len(images_list)

        print(f'Processing {image_count} images')

        previous_image = None
        previous_image_file: str = ''

        progress_counter = 0

        for image_file in images_list:

            try:
                progress_counter += 1
                if progress_counter % 10 == 0:
                    print(f'Processing image {progress_counter} of {image_count}: {image_file}')

                current_image = cv2.imread(os.path.join(images_directory, image_file))

                current_image = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)
                current_image = cv2.blur(current_image, (20, 20))

                if previous_image is None:
                    previous_image = current_image
                    previous_image_file = image_file
                    continue

                images_diff = cv2.absdiff(previous_image, current_image)
                diff_score = np.sum(images_diff)

                if diff_score > self.diff_threshold:
                    print('motion detected:', image_file, 'diff score:', diff_score)
                    output_directory = os.path.join(images_directory, 'motion_detected')
                    # print(output_directory)
                    if not os.path.exists(output_directory):
                        os.makedirs(output_directory)
                    cv2.imwrite(os.path.join(output_directory, previous_image_file), previous_image)
                    cv2.imwrite(os.path.join(output_directory, image_file), current_image)

                previous_image = current_image
                previous_image_file = image_file

            except Exception:
                print('ERROR:', sys.exc_info())


def parse_args(args: List[str]) -> Tuple[str, str]:
    format_message = 'USAGE: python3 motion.py images-directory jpg'
    args_length = 2

    if len(args) != args_length:
        print('Invalid number of arguments')
        print(format_message)
        return '', ''

    images_directory = args[0]
    extension = args[1]

    # remove starting / if given
    if images_directory[0] == '/':
        images_directory = images_directory[1:]

    full_path = os.path.join(SCRIPT_DIRECTORY, images_directory)
    if not os.path.exists(full_path):
        print('Invalid directory argument:', full_path)
        print(format_message)
        return '', ''

    if extension not in ['jpg', 'png']:
        print('Invalid extension')
        print(format_message)
        return '', ''

    return images_directory, extension


def main() -> None:
    images_directory, extension = parse_args(sys.argv[1:])
    if images_directory == '':
        return

    motion = Motion()
    motion.detect_motion_from_images(images_directory, extension)


if __name__ == '__main__':
    main()
