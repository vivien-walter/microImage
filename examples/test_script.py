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

# Add a time stamp on the image array
stampedArray = mim.addTime(contrastedArray, time_unit='s', time_scale=1/200, font_size=180, padding=50, white_text=True, position='top')

# Add a scale bar without text on the image array
markedArray = mim.addBar(stampedArray, space_unit='µm', space_scale=46.21, scale_length=4, thickness=50, add_text=False, white_bar=True, padding=50)

# Save the image in a file
mim.saveImage(markedArray, '/path/to/new/folder/and/image_file.tif', bit_depth=16, rescale=True)

# Make a montage from the image stack
montageArray = mim.makeMontage(markedArray, frames=5, margin=20, white_margin=False)

# Save the montage in a file
mim.saveImage(markedArray, '/path/to/montage_file.png', bit_depth=16, rescale=True)
