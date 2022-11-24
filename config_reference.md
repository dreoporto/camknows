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

Sets the logging level for log fies stored under `camknows/camknows/logs`. 
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


---


### `diff_threshold`

**Sensitivity for motion capture** - This is set to `2000000` by default.  Adjust this setting based on the number of images being captured.  The calculated difference is included in the names of saved files to assist with these adjustments.  

- File name format: `camknows-[TIMESTAMP]-[DIFF_SCORE].jpg`
- Example: `camknows-2021-09-04-09-41-13-535487-4.156.094.jpg`

In the above example, the `diff_score` between current and prior image in the video stream is calculated to be 4,156,094, well above the threshold of 2,000,000.

Environmental conditions such as direct sunlight can affect sensitivity.

### `motion_frames_threshold`

Set the number of consecutive motion detection image frames for an image to be saved.

### `time_lapse_seconds`

**Elapsed Time** to capture images, regardless of motion detection. This is set to `3600` seconds, or 1 hour, by default.  With this setting, a new image will be saved one hour from the time the last image was saved.  This feature assures you that the system is up and running in the event there is no movement. A `diff_score` is not included in the file name in these instances.  Example: `camknows-2021-09-04-09-41-06-577426-af3b73de.jpg`

### `motion_image_percent`

**Reduce Motion Data** - Reduce the amount of data used for motion detection by resizing the image data to this percent.  Default is `100` for no reduction.  This **does not** affect the images that are saved.  This can help reduce false positives by removing excess image detail/noise.  It can also be used to improve processing performance, especially in slower devices such as a Raspberry Pi Zero.
