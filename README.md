# MicroIMAGE

___

## General

### Description

- **Version:** 2.3.1
- **Author:** Vivien WALTER
- **Contact:** walter.vivien@gmail.com

**MicroIMAGE** is a Python 3.x module used to load all common types of images used in microscopy, edit and save them in any desired format.

### Compatibility

The module can currently open the following type(s) of image:
- .TIFF images and stacks
- .GIF images and animations
- .PNG, .BMP and .JPG standard images
- Directories of multiple frames

It can also save image(s) in the following formats:
- .TIFF images and stacks
- .GIF images and animations (8-bits only)
- .PNG, .BMP and .JPG standard images
- .MP4 video

---

## Table of contents

1. [Installation](#installation)
  * [Requirements](#requirements)
  * [Installation using the setup.py script](#script)
2. [How-to use the module](#howto)
  * [Basic Input/Output functions](#io)
    * [Opening an image](#open)
    * [Saving an image on the computer](#save)
    * [Video generation](#video)
  * [Image correction and modification](#correction)
    * [Background correction](#background)
    * [Contrast correction](#contrast)
    * [Displaying the pixel value distribution](#distribution)
    * [Crop the image](#crop)
    * [Generate a montage](#montage)
  * [Writing labels on images](#label)
    * [Scale bar](#scale)
    * [Time stamps](#time)
3. [Using the ImageStack class](#class)
  * [Loading the image in the class](#load_class)
  * [Navigate in the frames and display them](#frame_class)
  * [Duplicate and modify the image](#edit_class)
  * [Apply a correction on the image](#correct_class)
  * [Modify the space and time scale of the image](#scale_class)
  * [Save the image(s) in a file](#save_class)

---

## Installation <a name="installation"></a>

### Requirements <a name="requirements"></a>

The following modules are required to run MicroImage:

- Bottleneck
- ffmpeg-python
- Matplotlib
- NumPy
- pims
- Pillows
- Scikit-image

If you install the module using the setup.py script, you do NOT need to install first the module above.

In order to generate video, it is required to have **FFMPEG** installed on the computer. Instructions on how to install FFMPEG can be found on [Internet](https://github.com/adaptlearning/adapt_authoring/wiki/Installing-FFmpeg) (e.g. [MacOS](https://github.com/fluent-ffmpeg/node-fluent-ffmpeg/wiki/Installing-ffmpeg-on-Mac-OS-X))

### Installation using the setup.py script <a name="script"></a>

1. Download the module folder on the github repo

- Installation in a **Terminal-based** environment

  2. Open a terminal in the module folder
  3. (Opt.) Start your virtualenv if you use one
  4. Type and run the command
    ```bash
  python3 setup.py install
  ```

- Installation in an **Anaconda** environment

  2. Open Anaconda and go to your Environments
  3. Select the environment you want to install the module into
  4. Click on the arrow next to the name of the environment and select Open a Terminal
  5. Navigate to the module folder
  6. Type and run the command
    ```bash
  python setup.py install
  ```

---

## How-to use the module <a name="howto"></a>

The **examples/** folder provides a .py script as well as a Jupyter notebook to load and display an image using MicroImage.

### Basic Input/Output functions <a name="io"></a>

#### Opening an image <a name="open"></a>

To load an image, simply use the *openImage()* function:

```python
from microImage import openImage

imageArray = openImage('./path/to/folder/or/image.image_extension')
```

The *imageArray* output is a NumPy array of shape **(frames, Y pixel, X pixel)**.
To open a folder containing multiple frames, just type the path to the folder.

#### Saving an image on the computer <a name="save"></a>

To save an array as an image, you can use the *saveImage()* function:

```python
from microImage import saveImage

saveImage(imageArray, './path/to/new/file.tif', bit_depth=16, rescale=True)
```

The function will automatically detect if you are trying to save a single frame or a stack/animation.

You can specify the bit depth of the output image (8 or 16 bits, 8 bits only for gif animations) using the *bit_depth* argument. The function will always try to cover the full bit depth with the given pixel values; this can be prevented with the argument *rescale=False*.

If an extension is not specified, in the path of the file to create, the default extension .tif will be used. This can be changed by using the argument *default* to specify another default format (e.g *default='.png'*)

#### Video generation <a name="video"></a>

It is also possible to save the array as a .mp4 video using the *saveVideo()* function:

```python
from microImage import saveVideo

saveVideo(imageArray, './path/to/new/file.mp4', fps=25)
```

Having **ffmpeg** installed on the computer is required to use this function.

All arrays will be converted to 8-bits prior to be saved. The framerate of the video can be selected using the `fps=` argument.

It is possible to select a specific video codec for the output video using the `video_codec=` argument. The default video codec is *libx264*.

### Image correction and modification <a name="correction"></a>

#### Background correction <a name="background"></a>

Assuming the input array is a stack of image (> 1 frame), microImage can be used to remove the static background of the stack using the function *backgroundCorrection()*

```python
from microImage import backgroundCorrection

correctedArray = backgroundCorrection(imageArray, signed_bits=True, average='median', correction='division')
```

If the images come from a signed bit array, it should be specified using the argument *signed_bits*.

The type of *average* used can be selected between mean or median, and the type of *correction* has to be picked between division and subtraction, using their respective arguments.

#### Contrast correction <a name="contrast"></a>

The contrast of the image contained in the array can be modified with the function *contrastCorrection()*

```python
from microImage import contrastCorrection

correctedArray = contrastCorrection(imageArray, min=None, max=None, percentile=10, percentile_min=None, rescale=True)
```

The user can specify either the *min* and *max* pixel value, or can ask the function to calculate it based on percentiles. The min value is calculated based on *percentile_min* and the max based on *percentile* (from 100%, so 10 corresponds to 90%). If percentile_min is not given, the value of percentile will be used.

The output can be rescaled to the full bit depth with *rescale=True*. If left False, the scale will be based on the old min and max pixel values.

#### Displaying the pixel value distribution <a name="distribution"></a>

It is possible to display the pixel value distribution of the image array, along with the position of the min and max values calculated by the *contrastCorrection()* function. This can be done with the *showPVD()* function.

```python
from microImage import showPVD

showPVD(imageArray, n_bins=10000, min=None, max=None, percentile=10, percentile_min=None, log_scale=None)
```

The function will display the pixel value distribution as an histogram. The number of bins can be controlled by the `n_bins=` argument (default is 1000). The scale of the histogram can be switched to log using the `log_scale=` argument. If left to None, both axes will be shown as normal scales. "x" will use log scale for the X-axis, "y" for the Y-axis, and "xy" (or "yx") will use log scale for both axis.

All other arguments are similar to the one of the function *contrastCorrection()*, besides the `rescale=` which cannot be used here.

#### Crop the image <a name="crop"></a>

The image can be cropped using the *cropImage()* function

```python
from microImage import cropImage

croppedArray = cropImage(imageArray, top_left=(200,200), bottom_right=(800,800))
```

Each limit should be given as (X,Y) coordinates. If left to default, *top_left* will be equal to (0,0) and *bottom_right* to (Xmax, Ymax).

#### Generate a montage <a name="montage"></a>

A stack of images can be turned into a montage of individual frames in a single image. This is done by the function *makeMontage()*

```python
from microImage import makeMontage

montageArray = makeMontage(imageArray, frames=5, column=None, row=None, margin=20, white_margin=False)
```

The arguments `frames=` define the frames that has to be added in the montage. If an integer is given, the function will save every N frames of the stack. If a list is given, the list will be used as list of incides of the frame to save.

The general shape of the montage can be selected using the arguments `column=` and `row=`, respectively the number of columns and rows making the montage table. If any or both of these arguments are set to None, the function will automatically calculate what is required.

The arguments `margin=` allows for drawing margin between each pictures in the montage. If different from 0, it will be used as the thickness in pixels. The color of the margin is selected via the argument `white_margin=`.

### Writing labels on images <a name="label"></a>

The module microImage includes some simple tool to quicky write labels on the images

#### Scale bar <a name="scale"></a>

It is possible to add automatically a simple scale bar on the image using the *addBar()* function

```python
from microImage import addBar

modifiedArray = addBar(imageArray, scale_length=5, thickness=50, padding=20, white_bar=True, space_unit='µm', space_scale=46.21, add_text=True)
```

The scale and space units can be specified using the arguments `space_scale=` and `space_unit=` respectively. If None are given, the function will assume a scale in pixel. The length of the bar (in the given space scale and unit) can be selected using `scale_length=`. The `thickness` and the `padding` surrouding the bar car be selected with their eponymous arguments. User can select between white and black bars using the `white_bar=` boolean argument.

It is possible to add text on top of the bar with the `add_text=` boolean argument. User can select the `font=` .ttf file to use (default: *Arial.ttf*) and the font size with the `font_size=` argument. If let empty, the function will automatically the font size to match the scale bar length.

#### Time stamps <a name="time"></a>

To add time stamps on an image stack, one can use the function *addTime()*

```python
from microImage import addTime

modifiedArray = addTime(imageArray, position='top', padding=20, white_text=True, time_unit='s', time_scale=1/200)
```

Position of the stamp can be selected between top and bottom using the `position=` argument. The scale and time units can be specified using the arguments `time_scale=` and `time_unit=` respectively. The color of the text is selected using the argument `white_text=`.

The text options are the same as the one for the [addBar()](#scale) function.

## Using the ImageStack class <a name="class"></a>

It is possible to extract the images in an ImageStack object rather than in an array. Using an ImageStack object will reduce the versatility as compared to an array, but make the image processing easier to perform.

### Loading the image in the class <a name="load_class"></a>

* To load an image and generate an object, we use the function *loadImage()*

```python
from microImage import loadImage

image = loadImage('./path/to/folder/or/image.image_extension')
```

* Additionally, the ImageStack class can be loaded with an array instead of an image file using the *loadArray()* function

```python
from microImage import loadArray

image = loadArray(imageArray, name='test array')
```

It is essential that the imageArray object here is a 3-D array of dimension **(number of frame, Y, X)**

The element returned by each of these functions is an object with the following attributes:

Name | Type | Description
---|---|---
`image.name` | String | Name of the image stack (usually taken from the path)
`image.n_frames` | Int | Total number of frame in the stack (1 if single image)
`image.size` | 2-D Tuple | Size of the array in each dimension (Y,X)
`image.source` | 3-D Array | Array used to generate the class instance. Is used to reset all corrections. Dimensions are (t,Y,X)
`image.array` | 3-D Array | Originally copy of `image.source`, all modifications and corrections are applied to this array only (except crop). Dimensions are (t,Y,X)
`image.frame` | ImageFrame object | Instance of the class ImageFrame used to handle single frame images. See below
`image.frame_nbr` | Int | Index of the current frame being loaded in `image.frame`

To display the frames, the ImageStack class is calling another class named ImageFrame. This class has the following attributes

Name | Type | Description
--- | --- | ---
`frame.raw` | 2-D Array | Non-contrast corrected version of the frame being displayed. Used for calculation. Dimensions are (Y,X)
`frame.corrected` | 2-D Array | Array containing the frame being displayed, eventually with the selected contrast correction. Dimensions are (Y,X)

### Navigate in the frames and display them <a name="frame_class"></a>

* The frame loaded in the ImageFrame class for image processing can be selected using the command *.setFrame()*

```python
image.setFrame(12)
```

* To dislay the frame (using the matplotlib library), just call the *.show()* command.

```python
image.show(show_raw=False, cmap='gray', title=True)
```

The user can select whether the raw or contrast corrected image can be displayed, the color map and if the title should be displayed or not on the image.

### Duplicate and modify the image <a name="edit_class"></a>

* It is possible to create a copy of the ImageStack object anytime by using the command *.duplicate()*

```python
new_copy = image.duplicate()
```

  All previous modification made on the initial object will be pasted into the copy.

* The image can be cropped to a much smaller size with *.crop()*.

```python
image.crop(top_left=(200,200), bottom_right=(800,800))
```

The change will affect all image arrays in the ImageStack object, but also in the ImageFrame one. Check the [cropImage function](#crop) for details on the arguments of the function.

* In the case of a stack of several frames, the stack can be reduced to a subrange of frames with the command *.reducedRange()*

```python
image.reducedRange(first=10, last=20)
```

If not specified, the *first* and *last* frame of the new subrange will be calculated respectively as the first and the last frame of the `image.source` array.

### Apply a correction on the image <a name="correct_class"></a>

* Background correction similar to the one of the [backgroundCorrection()](#background) function can be applied with the *.backgroundCorrection()* command

```python
image.backgroundCorrection(imageArray, signed_bits=True, average='median', correction='division')
```

* Contrast correction similar to the one of the [contrastCorrection()](#contrast) function can be applied with the *.contrastCorrection()* command

```python
image.contrastCorrection(imageArray, min=None, max=None, percentile=10, percentile_min=None, rescale=True)
```

* The effect of the contrastCorrection on the pixel value distribution can be assessed with the *.showPVD()* command. Check the documentation on the [showPVD()](#distribution) function above for more details.

```python
image.showPVD(min=None, max=None, percentile=10, percentile_min=None, n_bins=1000, log_scale='xy')
```

* All modifications can be reset anytime using the *.reset()* command.

```python
image.reset()
```

This will cancel any background and contrast correction, but not modifications made by the .crop() and .reducedRange() commands.

### Modify the space and time scale of the image <a name="scale_class"></a>

* Set the scales using the *setScale()* function

```python
image.setScale(time_scale=1/200, time_unit='s', space_scale=46.21, space_unit='µm')
```

The `time_scale=` should be given in unit/frame and the `space_scale=` in unit/pixel. Only the called arguments will be modified, the one set to None or not added will be left unchanged.

* Add a scale bar on the image(s) using the *scaleBar()* function

```python
image.scaleBar(frame=0, scale_length=4, add_text=False)
```

The argument `frame=` can used to select on which specific frame the scale bar should be added. If set to None, the scale bar will be added on all frames.

Refer to the function [addBar()](#scale) above for description of other arguments.

* Add time stamps on an image stack using the *timeStamps()* function

```python
image.timeStamps(white_text=True)
```

Refer to the function [addTime()](#time) above for description of all arguments.

### Save the image(s) in a file <a name="save_class"></a>

* The command *.saveStack()* will save the whole stack saved in the ImageStack instance.

```python
image.saveStack('./path/to/new/file.tif', bit_depth=16, rescale=True, save_raw=False)
```

The *save_raw* argument allows the user to select if the corrected or raw array should be save. Check the [saveImage function](#save) for details on the arguments of the function.

* To only save the current frame in the ImageFrame instance, the command *.saveFrame()* can be used.

```python
image.saveFrame('./path/to/new/file.tif', bit_depth=16, rescale=True, save_raw=False)
```

* To save a montage of a selection of frame, the command *.makeMontage()* can be used

```python
image.makeMontage(name='./path/to/montage.tif', frames=[0,2,4,10], bit_depth=16, rescale=True)
```

Refer to the function [makeMontage()](#montage) above for description of all montage-related arguments of the command.

* To save a video file, the command *.saveVideo()* cam be used

```python
image.saveVideo(name='./path/to/montage.mp4', fps=25)
```

Refer to the function [saveVideo()](#video) above for description of all video generation arguments of the command.
