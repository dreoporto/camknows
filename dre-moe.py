# noinspection PyUnresolvedReferences
from picamera import PiCamera

import uuid
from time import sleep
import os.path

MAIN_DIRECTORY = 'media-files'
TEMP_IMAGE_FILE = 'dre-moe-temp'
WAIT_TIME = 30
LOOP = True


def capture_image(path: str) -> None:
    camera = PiCamera()
    camera.led = False

    try:
        camera.capture(path)
    finally:
        camera.close()


def do_motion_capture():
    if not os.path.exists(MAIN_DIRECTORY):
        os.mkdir(MAIN_DIRECTORY)

    filename = f'{TEMP_IMAGE_FILE}-{uuid.uuid4()}.jpg'
    filepath = os.path.join(MAIN_DIRECTORY, filename)

    print('CLICK!')

    capture_image(filepath)


def main() -> None:

    while True:
        do_motion_capture()

        if not LOOP:
            break

        print(f'taking photo in {WAIT_TIME} seconds...')
        sleep(WAIT_TIME)


if __name__ == '__main__':
    main()
