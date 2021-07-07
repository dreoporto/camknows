import datetime
import os.path
import sys
import uuid
from time import sleep

# noinspection PyUnresolvedReferences
from picamera import PiCamera

MAIN_DIRECTORY = 'media-files'
TEMP_IMAGE_FILE = 'dre-moe-temp'
WAIT_TIME = 20
LOOP = True


def capture_image(path: str) -> None:
    camera = PiCamera()
    camera.resolution = (1280, 720)
    camera.led = False

    try:
        camera.capture(path)
    finally:
        camera.close()


def do_motion_capture():

    display_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    time_suffix = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

    if not os.path.exists(MAIN_DIRECTORY):
        os.mkdir(MAIN_DIRECTORY)

    # i like guids
    filename = f'{TEMP_IMAGE_FILE}-{time_suffix}-{uuid.uuid4()}.jpg'
    filepath = os.path.join(MAIN_DIRECTORY, filename)

    print(f'{display_time}\tCLICK!\tnext photo in {WAIT_TIME} seconds...', end='\r')
    sys.stdout.flush()

    capture_image(filepath)

    sleep(WAIT_TIME)


def main() -> None:

    while True:
        do_motion_capture()

        if not LOOP:
            break


if __name__ == '__main__':
    main()
