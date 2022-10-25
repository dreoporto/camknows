# CamKnows™

## Summary

CamKnows™ is a Computer Vision motion detection application for the Raspberry Pi.

With the combined powers of both the Raspberry Pi and its Camera Module, CamKnows captures images when motion is detected, based on configured sensitivity.  This is accomplished by calculating the difference between two consecutive images to determine if motion has occurred.  An extensive set of configuration options allow for the customization of various settings, including motion sensitivity and time lapse image capture.

CamKnows is useful for monitoring activity, where customization options are critical.  This makes it a handy addition to existing systems you may already have in place.

"What's going on ...?  The camera knows."

## How it works

CamKnows is built with Python 3 and the following libraries:

- PiCamera - image capture
- OpenCV - Computer Vision capabilities, including image difference calculation and image manipulation
- Numpy - mathematical functions and data arrays

The PiCamera `capture` method obtains data from the Camera Module in the form of a numpy multidimensional data array.  Various capabilities provided by the PiCamera library are leveraged to ensure efficient and effective image capture.  Resolution, rotation, and timestamp settings for PiCamera can be customized in the `camknows_config.json` file.

OpenCV methods for image manipulation are used to simplify image data. The `absdiff` method calculates how much data has changed.  When this number exceeds a threshold, an image file is saved.  This threshold is customized using the `diff_threshold` setting detailed below.

CamKnows saves an image at a minimum of every hour by default, assuring you that the system is running properly. This setting can also be customized.

## Prerequisites

- Raspberry Pi Zero, 3 or 4
- [Raspberry Pi OS](https://www.raspberrypi.org/software/) running Stretch distribution or later
- [Camera Module](https://www.raspberrypi.org/documentation/accessories/camera.html#camera-modules)
- OpenCV and required libraries installed

For the above requirements, detailed install steps are available here: [How to Install OpenCV for Python on a Raspberry Pi](https://www.pendragonai.com/how-to-install-opencv-for-python-on-a-raspberry-pi/)

## Installation

To install the `camknows` code on your Raspberry Pi:

```
$ git clone https://github.com/dreoporto/camknows.git
```

### External Storage and File Share

To ensure adequate storage of files, adding external storage *with automatic mounting* to your Raspberry Pi is encouraged: https://www.raspberrypi.org/documentation/computers/configuration.html#external-storage-configuration

A Samba File Share makes it simple to view images that have been saved: https://magpi.raspberrypi.org/articles/samba-file-server

Once you have these setups complete, install CamKnows directly on your file share to save files for remote access on your local network.

## Usage

### Command Line Execution

```
$ cd camknows/camknows

$ python3 camknows.py
```

### Crontab Entry

With CamKnows configured and working as desired, a crontab entry will ensure that it runs at startup.  Here is an example that starts the application *if it is not already running*.  

```
# run every minute, unless already running
* * * * * flock -n /tmp/camknows-lock python3 /mnt/usbdisk1/camknows/camknows/camknows.py > /mnt/usbdisk1/myjob.log 2>&1
```

For dedicated Raspberry Pi setups running only the essentials (i.e., [RPi OS Lite](https://www.raspberrypi.org/software/operating-systems/)), a crontab entry with a set priority can be useful:

```
* * * * * flock -n /tmp/camknows-lock nice -n -10 python3 /mnt/usbdisk1/camknows/camknows/camknows.py > /mnt/usbdisk1/myjob.log 2>&1
```

The `nice` option above can only be included with a root user crontab entry, by running `sudo crontab -e`.  Be sure to only have one entry in either the `pi` user (`crontab -e`) or `root` (`sudo ...`) user.

## Important Configuration Settings

CamKnows functionality can be customized by modifying the default settings stored in the `camknows_config.json` file.  

### Sensitivity: `diff_threshold`

This is set to `2000000` by default.  Adjust this setting based on the number of images being captured.  The calculated difference is included in the names of saved files to assist with these adjustments.  

- File name format: `camknows-[TIMESTAMP]-[DIFF_SCORE].jpg`
- Example: `camknows-2021-09-04-09-41-13-535487-4.156.094.jpg`

In the above example, the `diff_score` between current and prior image in the video stream is calculated to be 4,156,094, well above the threshold of 2,000,000.

Environmental conditions such as direct sunlight can affect sensitivity.

### Motion Frames Threshold: `motion_frames_threshold`

Set the number of consecutive motion detection image frames for an image to be saved.

### Elapsed Time: `time_lapse_seconds`

This is set to `3600` seconds, or 1 hour, by default.  With this setting, a new image will be saved one hour from the time the last image was saved.  This feature assures you that the system is up and running in the event there is no movement. A `diff_score` is not included in the file name in these instances.  Example: `camknows-2021-09-04-09-41-06-577426-af3b73de.jpg`

### Image Resolution: `resolution_width`, `resolution_height`

Sets the resolution of captured/processed and saved images, which is set to a default of `1024` by `768`.  Setting this too high will impact application performance, including capture speed.

### Rotate Image: `rotation`

Sets the rotation for images; useful for adjustments based on your camera's position. Example: for a camera that is hanging upside-down, set this value to `180`.

### Reduce Motion Data: `motion_image_percent`

Reduce the amount of data used for motion detection by resizing the image data to this percent.  Default is `100` for no reduction.  This **does not** affect the images that are saved.  This can help reduce false positives by removing excess image detail/noise.  It can also be used to improve processing performance, especially in slower devices such as a Raspberry Pi Zero.

## Output - Motion Capture Images

For more efficient file organization and management, images are saved to a series of subdirectories, based on the file date.  Example: `camknows/media-files/2021/09/04/camknows-2021-09-04-09-41-13-535487-4.156.094.jpg`

## Acknowledgements

In addition to PiCamera and OpenCV, I have found Simon Monk’s [Raspberry Pi Cookbook](https://www.oreilly.com/library/view/raspberry-pi-cookbook/9781492043218/), now in its 3rd Edition, to be an invaluable resource for leveraging the capabilities of these diminutive but powerful devices to solve real problems. I cannot recommend it enough.

*Copyright (c) 2021-2022 Andre Oporto*
