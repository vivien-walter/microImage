# MicroIMAGE

___

## General

### Description

- **Version:** 2.0
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

---

## Table of contents

1. [Installation](#installation)
  * [Requirements](#requirements)
  * [Installation using the setup.py script](#script)
2. [How-to use the module](#howto)
  * [Basic Input/Output functions](#io)
    * Opening an image
    * Saving an image on the computer
  * Image correction and modification
    * Background correction
    * Contrast correction
    * Crop the image
  * Using the ImageStack class

---

## Installation <a name="installation"></a>

### Requirements <a name="requirements"></a>

The following modules are required to run MicroImage:

- Bottleneck
- Matplotlib
- NumPy
- pims
- Pillows
- Scikit-image

If you install the module using the setup.py script, you do NOT need to install first the module above.

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

#### Opening an image

To load an image, simply use the *openImage()* function:

```python
from microImage import openImage

imageArray = openImage('./path/to/folder/or/image.image_extension')
```

The *imageArray* output is a NumPy array of shape **(frames, Y pixel, X pixel)**.
To open a folder containing multiple frames, just type the path to the folder.

#### Saving an image on the computer

To save an array as an image, you can use the *saveImage()* function:

```python
from microImage import saveImage

saveImage(imageArray, './path/to/new/file.tif', bit_depth=16, rescale=True)
```

The function will automatically detect if you are trying to save a single frame or a stack/animation.

You can specify the bit depth of the output image (8 or 16 bits, 8 bits only for gif animations) using the *bit_depth* argument. The function will always try to cover the full bit depth with the given pixel values; this can be prevented with the argument *rescale=False*.

If an extension is not specified, in the path of the file to create, the default extension .tif will be used. This can be changed by using the argument *default* to specify another default format (e.g *default='.png'*)

### Image correction and modification

#### Background correction

Assuming the input array is a stack of image (> 1 frame), microImage can be used to remove the static background of the stack using the function *backgroundCorrection()*

```python
from microImage import backgroundCorrection

correctedArray = backgroundCorrection(imageArray, signed_bits=True, average='median', correction='division')
```

If the images come from a signed bit array, it should be specified using the argument *signed_bits*.

The type of *average* used can be selected between mean or median, and the type of *correction* has to be picked between division and subtraction, using their respective arguments.

#### Contrast correction

The contrast of the image contained in the array can be modified with the function *contrastCorrection()*

```python
from microImage import contrastCorrection

correctedArray = contrastCorrection(imageArray, signed_bits=True, average='median', correction='division')
```

#### Crop the image

S

### Using the ImageStack class

Bla
