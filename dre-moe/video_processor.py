# noinspection PyUnresolvedReferences
import cv2

import datetime
import os
from typing import List


class VideoProcessor:

    def __init__(self):
        self.script_directory = os.path.dirname(os.path.abspath(__file__))

    def convert_to_video(self, images_directory: str, output_file: str, extension: str):

        images_list: List[str] = []
        for image in os.listdir(images_directory):
            if image.endswith(f'.{extension}'):
                images_list.append(image)

        print(f'Processing {len(images_list)} images')

        character_code = cv2.VideoWriter_fourcc(*'MP4V')
        frames_per_second = 1

        frame_image = cv2.imread(os.path.join(self.script_directory, images_directory, images_list[0]))
        frame_height, frame_width, _ = frame_image.shape

        video = cv2.VideoWriter(output_file, character_code, frames_per_second, (frame_width, frame_height))

        image_index = 0

        try:
            for image in images_list:
                image_index += 1
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if image_index % 10 == 0:
                    print(f'{timestamp}\t\tprocessing image {image_index}')
                video.write(cv2.imread(os.path.join(self.script_directory, images_directory, image)))
        finally:
            cv2.destroyAllWindows()
            video.release()


def main():
    images_directory = 'media-files/2021/07/19'
    output_file = 'video.mp4'
    extension = 'jpg'

    processor = VideoProcessor()
    processor.convert_to_video(images_directory, output_file, extension)


if __name__ == '__main__':
    main()
