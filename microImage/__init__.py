from glob import glob
import numpy as np
import os
from PIL import Image, ImageSequence
import pims

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

# ----------------------------------------------------
# Check that the extensions in the list are authorized
def _check_extensions(list, extensions=['.tif','.png','.bmp','.gif','.jpg']):

    new_list = []

    # Process all the items of the list
    for file in list:
        file_name, file_extension = os.path.splitext(file)

        # Save in the new list on if the extension is authorized
        if file_extension in extensions:
            new_list.append(file)

    # Check that the new list is not empty
    if len(new_list) == 0:
        raise Exception('The directory does not contain any valid file.')
    else:
        return new_list

# ------------------------------
# Open all the files in a folder
def _open_folder(path):

    # Check all the files in the folder
    file_in_folder = glob( os.path.join(path, '*.*') )

    # Check that the files in the folder can be opened
    file_in_folder = _check_extensions(file_in_folder)

    # Open all the images
    sequence = pims.ImageSequence(path)

    return np.array(sequence)

# ----------------------
# Open the selected file
def _open_file(path):

    # Check the extension of the given file
    file_path = _check_extensions( [path] )
    path = file_path[0]

    # Load the image(s)
    sequence = Image.open(path)

    # Deal with stacks (.tif) and animations (.gif)
    if 'n_frames' in dir(sequence):

        # Extract all frames
        stack = []
        for frame in ImageSequence.Iterator(sequence):
            stack.append( np.copy(np.array(frame)) )

        imageArray = np.array(stack)

    # Convert simple image type
    else:
        imageArray = np.array(sequence)

        # Format the shape of all image arrays
        imageArray = np.reshape( imageArray, (1, *imageArray.shape) )

    return imageArray

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# ----------------------------------
# Load an image, a stack or a folder
def loadImage(path):

    # Check if it is a folder
    if os.path.isdir(path):
        imageArray = _open_folder(path)

    # Check if it is a file
    elif os.path.isfile(path):
        imageArray = _open_file(path)

    # Abort if the file is not recognized
    else:
        raise Exception('The input path is neither a file nor a directory.')

    # Return the appropriate object
    return imageArray
