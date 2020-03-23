# MicroIMAGE

## General

### Description

- **Version:** 1.0
- **Author:** Vivien WALTER
- **Contact:** walter.vivien@gmail.com

**MicroIMAGE** is a Python 3.x module used to load all common types of images used in microscopy and format them as **Numpy arrays**.

### Compatibility

The module can currently open the following type(s) of image:
- .TIFF images and stacks
- .GIF images and animations
- .PNG, .BMP and .JPG standard images
- Directories of multiple frames

## Installation

### Requirements

The following modules are required to run MicroImage:

- NumPy
- pims
- Pillows

If you install the module using the setup.py script, you do NOT need to install first the module above.

### Installation using the setup.py script

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

## How-to use the module

The **examples/** folder provides a .py script as well as a Jupyter notebook to load and display an image using MicroImage.

### Loading an image

To load an image, simply use the *loadImage()* function:

```python
from microImage import loadImage

imageArray = loadImage('./path/to/folder/or/image.image_extension')
```

The *imageArray* output is a NumPy array of shape **(frames, Y pixel, X pixel)**.
To open a folder containing multiple frames, just type the path to the folder.
