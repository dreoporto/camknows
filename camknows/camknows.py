
from camera import Camera


def main() -> None:

    try:
        camera = Camera()
        camera.start_camera_loop()
    except KeyboardInterrupt:
        print('Application closed (KeyboardInterrupt)')


if __name__ == '__main__':
    main()
