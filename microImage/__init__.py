import os

import microImage.correction as corr
import microImage.image_classes as img
import microImage.input_output as io
import microImage.modification as mod

##-\-\-\-\-\-\-\-\-\-\-\
## INPUT/OUTPUT FUNCTIONS
##-/-/-/-/-/-/-/-/-/-/-/

# ----------------------------------
# Open the image and return an array
def openImage(path):
    imageArray = io.loadImage(path)
    return imageArray

# ---------------------------------------
# Open the image and load it into a class
def loadImage(path, name = None):

    # Open the image
    imageArray = io.loadImage(path)

    # Extract the name of the file
    if name is None:
        a,name = os.path.split(path)
        if name == "":
            a,name = os.path.split(a)

    return img.getImageClass(imageArray, name=name)

# -----------------------------
# Save the image frame or stack
def saveImage(array, path, default=".tif", bit_depth=8, rescale=True):
    io.saveImage(array, path, default=default, bit_depth=bit_depth, rescale=rescale)

##-\-\-\-\-\-\-\-\
## IMAGE CORRECTION
##-/-/-/-/-/-/-/-/

# ---------------------------------------
# Remove the background of an image stack
def backgroundCorrection(array, signed_bits=False, average='mean', correction='division'):

    # Apply the background correction
    corrected_array = corr.backgroundCorrection(array,
        signed_bits=signed_bits,
        average=average,
        correction=correction
        )

    return corrected_array

# ---------------------------------
# Correct the contrast of the image
def contrastCorrection(array, min=None, max=None, percentile=10, percentile_min=None, rescale=True):

    # Get the limits
    old_limits, new_limits = corr.setContrastCorrection(array,
        min=min,
        max=max,
        percentile=percentile,
        percentile_min=percentile_min,
        rescale=rescale
        )

    # Process the array
    corrected_array = corr.doContrastCorrection(array, old_limits, new_limits)

    return corrected_array

##-\-\-\-\-\-\-\-\-\
## IMAGE MANIPULATION
##-/-/-/-/-/-/-/-/-/

# -------------------------------------
# Crop the image using the given points
def cropImage(array, top_left=(0,0), bottom_right=None):
    return mod.crop(array, top_left=top_left, bottom_right=bottom_right)
