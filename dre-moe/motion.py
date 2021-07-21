import os
from typing import List

import cv2
import numpy as np


class Motion:

    def __init__(self):
        self.script_directory = os.path.dirname(os.path.abspath(__file__))
        self.diff_threshold = 3000000

    def detect_motion_from_images(self, directory: str, extension: str):

        images_directory = os.path.join(self.script_directory, directory)
        images_list: List[str] = []

        for file_name in os.listdir(images_directory):
            if file_name.endswith(f'.{extension}'):
                images_list.append(file_name)

        print(f'Processing {len(images_list)} images')

        previous_image = None
        previous_image_file: str = ''

        for image_file in images_list:
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


def main():
    images_directory = 'media-files'
    extension = 'jpg'

    motion = Motion()
    motion.detect_motion_from_images(images_directory, extension)


if __name__ == '__main__':
    main()
