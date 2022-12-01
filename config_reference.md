# CamKnows™ Configuration Reference

CamKnows™ settings for motion detection and image capture can be customized using the
`camknows_config.json` file. 
This provides a level of control that goes beyond commercial off the shelf products, 
allowing you to tailor CamKnows to your specific environmental requirements and applications.

Default settings are provided in the existing `camknows_config.json` file.  Feel free to experiment and customize to 
your needs based on the information provided below.

## Image Capture

## Motion Detection

## Image Files

## Timestamp

## Camera Settings (`manual_*`)

## Utility

## Expert Settings

### `main_directory`

The main directory where image files are stored.

- `media-files` stores images under `camknows/camknows/media-files`

### `image_file_prefix`

Prefix text added to all image file names

- `camknows` stores images as `camknows*.jpg`

### `logger_level`

Sets the logging level for log files stored under `camknows/camknows/logs`. 
Useful for troubleshooting and config customization. 

- Options: `INFO`, `DEBUG`, `NOTSET`

### `wait_time` (expert)

Time delay in seconds for the image detection loop.  
Useful for configuration **fine-tuning and troubleshooting only**. Should be set to `0`

### `do_loop` (expert)

Enables the image detection loop. Should be set to `true`.  
By setting to `false`, only the startup image will be captured; then the program will exit.

### `awb_delay` (expert)

Delay time in seconds to allow Auto White Balance to be set. Should be set to `3`

### `resolution_width`, `resolution_height`

**Image Resolution** - Sets the resolution of captured/processed and saved images, which is set to a default of `1024` by `768`.  Setting this too high will impact application performance, including capture speed.

### `rotation`

**Rotate Image** - Sets the rotation for images; useful for adjustments based on your camera's position. Example: for a camera that is hanging upside-down, set this value to `180`.

### `zoom`

Applies a **digital zoom** to the captured image.
Format is `(x, y, w, h)` with a default of `(0, 0, 100, 100)`.
Each value ranges from 0.0 to 1.0, to indicate the proportion of the image to include.
Example: `(0, 0, 100, 100)` begins at 0% x/y and captures 100% of the image width/height,
so the entire image is included.

### `show_image_timestamp`

Include a timestamp at the top of the image.

### `image_timestamp_text_size`

Set the image timestamp text size.

### `use_video_port` (expert)

Accelerates image capture by using the video stream.

### `enable_manual_mode` (expert)

Enables other manual settings (those that start with `manual_`) to be configured.  

### `manual_iso` 

ISO setting for camera hardware.  Set to `0` to allow automatic configuration.

### `manual_framerate_range_from`

Lowest setting for framerate range.  Default is 30 fps.

### `manual_framerate_range_to`

Highest setting for framerate range.  Default is 30 fps.

### `manual_shutter_speed` 

Shutter speed setting for camera hardware.  Set to `0` to allow automatic configuration.

### `manual_awb_mode`

Set to `off` to disable Auto White Balance mode.

### `manual_awb_gains_red`, `manual_awb_gains_blue`

Manual settings for White Balance (TODO AEO link to reference).

### `print_camera_settings` (expert)

Output camera settings to the command line. Useful when experimenting with settings and code.

### `timestamp_format`

Format for image timestamps, which are placed at the top-center of captured images using the camera firmware.

### `timestamp_filename_format`

Format for file timestamps, which are included in saved image file names. 

- Setting: `%Y-%m-%d-%H-%M-%S-%f` *(year, month, date, hour, minute, second, millisecond)*
- Output: camknows-**2022-10-01-09-04-35-661034**-7a9f5e3d.jpg

### `diff_score_in_filename`

Include the diff score in the saved image file name. 
Useful for fine-tuning the `diff_threshold` setting.
On startup and time-lapse expiration, a random string will be used instead of a diff score.

Examples:
- camknows-2022-10-12-07-28-49-106391-**4.277.890**.jpg
- camknows-2022-10-12-07-28-45-199350-**bae9920f**.jpg

### `diff_threshold`

**Sensitivity for motion capture** - This is set to `2000000` by default.  Adjust this setting based on the number of images being captured.  The calculated difference is included in the names of saved files to assist with these adjustments.  

- File name format: `camknows-[TIMESTAMP]-[DIFF_SCORE].jpg`
- Example: `camknows-2021-09-04-09-41-13-535487-4.156.094.jpg`

In the above example, the `diff_score` between current and prior image in the video stream is calculated to be 4,156,094, well above the threshold of 2,000,000.

Environmental conditions such as direct sunlight can affect sensitivity.

### `enable_led` (expert)

Enable/disable the camera device led, which is lit when the camera is running. 
Certain Raspberry Pi models such as the Zero and 3B+ do not support this setting, so the led will always illuminate if the camera is running.

### `time_lapse_seconds`

**Elapsed Time** to capture images, regardless of motion detection. This is set to `3600` seconds, or 1 hour, by default.  With this setting, a new image will be saved one hour from the time the last image was saved.  This feature assures you that the system is up and running in the event there is no movement. A `diff_score` is not included in the file name in these instances.  Example: `camknows-2021-09-04-09-41-06-577426-af3b73de.jpg`

### `setup_timeout_seconds` (expert)

(TODO AEO)

### `enable_image_debugging` (expert)

For faster processing with CamKnows, motion detection data is always converted to grayscale and blurred.
It is also resized depending on the `motion_image_percent` setting. 
This does not impact motion capture images, but sometimes you may want to see what these conversions 
are producing to troubleshoot motion detection.

If `enable_image_debugging` is enabled, this converted motion detection data will be saved as  
additional **_p0.jpg* (previous) and **_p1.jpg* (current) images to a *processed* subdirectory.
This is helpful when troubleshooting motion detection.

### `motion_frames_threshold`

Set the number of consecutive motion detection image frames for an image to be saved.

### `motion_image_percent`

**Reduce Motion Data** - Reduce the amount of data used for motion detection by resizing the image data to this percent.  Default is `100` for no reduction.  This **does not** affect the images that are saved.  This can help reduce false positives by removing excess image detail/noise.  It can also be used to improve processing performance, especially in slower devices such as a Raspberry Pi Zero.

### `crop_dimensions`

Crop the image data, by setting the x1, x2, y1, y2 values. 
If x2 or y2 are set to 0 this setting is ignored.
This is useful for excluding unwanted data from motion detection and saved files,
without distorting the saved image.
Since the timestamp is set using camera firmware, this setting may exclude the image timestamp depending on configuration.

Example: A setting of [1, 1024, 1, 568] will crop a 1024x768 image by removing the 
bottom of the image data.
