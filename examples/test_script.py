"""This script provides an example on how to load an image and/or a folder
using the module MicroImage.
It also demonstrates how to display the image using the matplotlib module

It requires either:
- an image file (e.g. test_image.png)
- an image folder containing multiple frames (e.g. test_folder/)"""

# Import the required external module(s)
import matplotlib.pyplot as plt

# Import the loadImage() function from the microImage module
from microImage import loadImage

# Open the image
"""Path to the file to open. Replace with the path to an existing file or folder."""
test_file = '/path/to/folder/test_image.tif'

# Load the image into an array
imageArray = loadImage(test_file)

# Display the shape of the array
print(imageArray.shape)

# Display the image
plt.imshow(imageArray[0], cmap='gray')
plt.show()
