# noinspection PyUnresolvedReferences
from picamera import PiCamera
from time import sleep
import os.path

MAIN_DIRECTORY = 'media-files'
TEMP_IMAGE_FILE = 'dre-moe-temp.jpg'
WAIT_TIME = 5


def capture_image(path: str, pause_length: int = 0) -> None:
    camera = PiCamera()
    camera.led = False

    try:
        print(f'taking photo in {pause_length} seconds...')
        sleep(pause_length)

        print('CLICK!')
        camera.capture(path)
    finally:
        camera.close()


def main() -> None:
    if not os.path.exists(MAIN_DIRECTORY):
        os.mkdir(MAIN_DIRECTORY)

    capture_image(os.path.join(MAIN_DIRECTORY, TEMP_IMAGE_FILE), WAIT_TIME)


if __name__ == '__main__':
    main()
