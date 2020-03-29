"""This script provides an example on how to use the microImage classes to
load, process and save images.

It requires either:
- an image file (e.g. test_image.png)
- an image folder containing multiple frames (e.g. test_folder/)
- an 3-D array with the dimensions (nbr of frames, Y, X)"""

# Import the required external module(s)
import matplotlib.pyplot as plt

# Import the loadImage() function from the microImage module
import microImage as mim

# Open the image
"""Path to the file to open. Replace with the path to an existing file or folder."""
test_file = '/path/to/folder/test_image.tif'

# Load the image into an array
imageObject = mim.loadImage(test_file)

# Print some of the attributes of the object
print('Object name:', imageObject.name)
print('Number of frames:', imageObject.n_frames)
print('Image size (Y,X):', imageObject.size)

# Display the image
imageObject.show()
plt.show()

# Apply a background correction
image.backgroundCorrection(signed_bits=True, average='median')

# Duplicate the instance
image2 = image.duplicate()

# Crop the image on a frame from (200,200) to (800,800)
image2.crop(top_left=(200,200), bottom_right=(800,800))

# Use a contrast correction to see the image
image2.contrastCorrection(percentile_min=30, percentile=5, rescale=True)

# Select the frame to be displayed
image2.setFrame(10)

# Display the new cropped and corrected image
image2.show()
plt.show()

# Save the displayed image
image2.saveFrame('/path/to/new/folder/and/frame.tif', bit_depth=16, rescale=False)

# Save the raw array as a gif animation
image2.saveStack('/path/to/new/folder/and/stack.gif', bit_depth=8, save_raw=True)
