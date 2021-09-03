import datetime
import os
import sys
from typing import List, Tuple

import cv2


class VideoProcessor:

    def __init__(self):
        self.script_directory = os.path.dirname(os.path.abspath(__file__))

    # noinspection PyMethodMayBeStatic
    def convert_to_video(self, images_directory: str, output_file: str, extension: str) -> None:

        images_list: List[str] = []
        for image in os.listdir(images_directory):
            if image.endswith(f'.{extension}'):
                images_list.append(image)

        images_list.sort()

        print(f'Processing {len(images_list)} images')

        character_code = cv2.VideoWriter_fourcc(*'MP4V')
        frames_per_second = 1

        frame_image = cv2.imread(os.path.join(images_directory, images_list[0]))
        frame_height, frame_width, _ = frame_image.shape

        video = cv2.VideoWriter(output_file + '.mp4', character_code, frames_per_second, (frame_width, frame_height))

        image_index = 0

        try:
            for image in images_list:
                image_index += 1
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if image_index % 10 == 0:
                    print(f'{timestamp}\t\tprocessing image {image_index}')
                video.write(cv2.imread(os.path.join(images_directory, image)))
        finally:
            cv2.destroyAllWindows()
            video.release()


def parse_args(args: List[str]) -> Tuple[str, str, str]:
    format_message = (f'\nUSAGE:\n' 
                      '$ python3 video_processor.py images-directory video-file-name jpg\n'
                      'EXAMPLE:\n'
                      '$ python3 video_processor.py media-files/2021/07/25 video-20210725 jpg')
    args_length = 3

    if len(args) != args_length:
        print('Invalid number of arguments')
        print(format_message)
        return '', '', ''

    images_directory = args[0]
    output_file = args[1]
    extension = args[2]
    full_path = parse_directory_path(images_directory)

    if full_path == '':
        print('Invalid directory argument:', images_directory)
        print(format_message)
        return '', '', ''

    if extension not in ['jpg', 'png']:
        print('Invalid extension: must be jpg or png')
        print(format_message)
        return '', '', ''

    return full_path, output_file, extension


def parse_directory_path(directory_path: str) -> str:
    parsed_path = ''

    if os.path.exists(directory_path):
        parsed_path = directory_path
    else:
        if directory_path[0] == '/':
            parsed_path = directory_path[1:]

        parsed_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), parsed_path)

        if not os.path.exists(parsed_path):
            parsed_path = ''

    return parsed_path


def main() -> None:
    images_directory, output_file, extension = parse_args(sys.argv[1:])
    if images_directory == '':
        return

    processor = VideoProcessor()
    processor.convert_to_video(images_directory, output_file, extension)


if __name__ == '__main__':
    main()
