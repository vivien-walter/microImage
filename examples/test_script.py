"""This script provides an example on how to load an image and/or a folder
using the module MicroImage, and then how to process it using the different
functions of the module before saving it.
It also demonstrates how to display the image using the matplotlib module.

It requires either:
- an image file (e.g. test_image.png)
- an image folder containing multiple frames (e.g. test_folder/)"""

# Import the required external module(s)
import matplotlib.pyplot as plt

# Import the loadImage() function from the microImage module
import microImage as mim

# Open the image
"""Path to the file to open. Replace with the path to an existing file or folder."""
test_file = '/path/to/folder/test_image.tif'

# Load the image into an array
imageArray = mim.openImage(test_file)

# Display the shape of the array
print(imageArray.shape)

# Display the first frame of the image
plt.imshow(imageArray[0], cmap='gray')
plt.show()

# Apply a background correction
correctedArray = mim.backgroundCorrection(imageArray, signed_bits=True, average='median')

# Crop the image on a frame from (200,200) to (800,800)
croppedArray = mim.cropImage(correctedArray, top_left=(200,200), bottom_right=(800,800))

# Use a contrast correction to see the image
contrastedArray = mim.contrastCorrection(croppedArray, percentile_min=30, percentile=5, rescale=True)

# Display the new image
plt.imshow(contrastedArray[0], cmap='gray')
plt.show()

# Save the image in a file
mim.saveImage(contrastedArray, '/path/to/new/folder/and/image_file.tif', bit_depth=16, rescale=True)
