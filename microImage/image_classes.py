from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np
import os

from microImage.correction import backgroundCorrection, setContrastCorrection, doContrastCorrection
from microImage.input_output import saveImage
from microImage.modification import crop

##-\-\-\-\-\-\-\-\
## PRIVATE FUNCTION
##-/-/-/-/-/-/-/-/

# ---------------------------------------
# Check if the array have multiple frames
def _check_multiple_frames(array):

    # Check the shape of the array
    if array.shape[0] <= 1:
        raise Exception("The function cannot be called as it requires a sequence of frame.")

# ---------------------------------------
# Define the name to the file being saved
def _get_saved_name(name, frame_number=None):

    # Remove existing extension in the name
    name, ext = os.path.splitext(name)

    # Append the frame number
    if frame_number is not None:
        name += '_' + str(frame_number)

    return name + '_saved'

##-\-\-\-\-\-\
## IMAGE CLASS
##-/-/-/-/-/-/

# ----------------------------------------------
# Class to handle a single frame and its display
class ImageFrame:
    def __init__(self, array):

        self.raw = array
        self.corrected = np.copy(array)

        # Initialize limits for contrast correction
        self._isCorrected = False
        self._min_to_correct, self._max_to_correct = None, None
        self._min_corrected, self._max_corrected = None, None

    # ------------------------------------
    # Update the currently displayed frame
    def updateFrame(self, array):

        # Update the attributes
        self.raw = array
        self.corrected = np.copy(array)

        # Apply correction if possible
        if self._isCorrected:
            self.contrastCorrection()

    # ---------------------------------
    # Correct the contrast on the image
    def contrastCorrection(self):
        self.corrected = doContrastCorrection(self.raw, (self._min_to_correct, self._max_to_correct), (self._min_corrected, self._max_corrected))

##-\-\-\-\-\-\
## STACK CLASS
##-/-/-/-/-/-/

# ------------------------------------
# Class to handle a multi-frame object
class ImageStack:
    def __init__(self, array, name='Untitled'):

        # Extract the informations
        self.name = name

        self.source = array
        self.array = np.copy(array)

        self.n_frames = array.shape[0]
        self.size = array.shape[1:]

        # Initialize the current frame
        self.frame = ImageFrame(self.array[0])
        self.frame_nbr = 0

    ##-\-\-\-\-\-\-\-\
    ## IMAGE CORRECTION
    ##-/-/-/-/-/-/-/-/

    # -----------------------------------------
    # Correct the background of the image array
    def backgroundCorrection(self, signed_bits=False, average='mean', correction='division'):

        # Check if it's a sequence
        _check_multiple_frames(self.source)

        # Apply the correction
        self.array = backgroundCorrection(self.source, signed_bits=signed_bits, average=average, correction=correction)

        # Update the displayed frame
        self.frame.updateFrame( self.array[self.frame_nbr] )

    # --------------------------------
    # Modify the contrast of the image
    def contrastCorrection(self, min=None, max=None, percentile=10, percentile_min=None, rescale=True):

        # Save the limits for future contrast corrections in the memory
        old_limits, new_limits = setContrastCorrection(self.frame.raw,
            min=min,
            max=max,
            percentile=percentile,
            percentile_min=percentile_min,
            rescale=rescale
            )
        self.frame._isCorrected = True
        self.frame._min_to_correct, self.frame._max_to_correct = old_limits
        self.frame._min_corrected, self.frame._max_corrected = new_limits

        # Apply the correction
        self.frame.contrastCorrection()

    # -------------------------------
    # Reset the background correction
    def reset(self):

        # Reinitialise all defined values
        self.array = np.copy(self.source)
        self.frame._isCorrected = False
        self.frame.updateFrame( self.array[self.frame_nbr] )

    ##-\-\-\-\-\-\-\-\-\
    ## IMAGE MODIFICATION
    ##-/-/-/-/-/-/-/-/-/

    # -------------------------------------------
    # Duplicate the class instance into a new one
    def duplicate(self):
        return deepcopy(self)

    # ---------------------------------
    # Select a reduced number of frames
    def reducedRange(self, first=0, last=None):

        # Check if it's a sequence
        _check_multiple_frames(self.source)

        # Find the last limit
        if last is None:
            last = self.source.shape[0]

        # Check the values
        if first < 0 or first > last or last > self.source.shape[0]:
            raise Exception("Range selection not valid")

        # Select the range of frames
        self.source = self.source[first:last]
        self.array = self.array[first:last]

        # Reload the frame
        self.frame.updateFrame( self.array[self.frame_nbr] )

    # -------------------------------------
    # Crop all the arrays on the given size
    def crop(self, top_left=(0,0), bottom_right=None):

        # Crop the arrays
        self.source = crop(self.source, top_left=top_left, bottom_right=bottom_right)
        self.array = crop(self.array, top_left=top_left, bottom_right=bottom_right)

        # Reload the frame
        self.frame.updateFrame( self.array[self.frame_nbr] )

    ##-\-\-\-\-\-\-\-\-\-\
    ## DISPLAYING FUNCTIONS
    ##-/-/-/-/-/-/-/-/-/-/

    # ------------------------
    # Change the current frame
    def setFrame(self, number):

        # Check if it's a sequence
        _check_multiple_frames(self.source)

        # Update the memory
        self.frame_nbr = number

    # -----------------------------------------
    # Display the current frame with matplotlib
    def show(self, show_raw=False, cmap='gray', title=True):

        # Show the current frame
        plt.imshow( self.frame.corrected, cmap=cmap )

        # Add the text to the graph
        if title:
            title_text = self.name
            if self.n_frames > 1:
                title_text += ', frame: ' + str(self.frame_nbr + 1)
            plt.title(title_text)

        plt.show()

    ##-\-\-\-\-\
    ## SAVE IMAGE
    ##-/-/-/-/-/

    # -----------------------------------------------
    # Save the frame currently selected and displayed
    def saveFrame(self, name=None, extension='.tif', save_raw=False, bit_depth=16, rescale=True):

        # Define the name
        if name is None:
            name = _get_saved_name(self.name, frame_number=self.frame_nbr + 1)

        # Select the array to save
        if save_raw:
            array = self.frame.raw
        else:
            array = self.frame.corrected

        # Save the image
        saveImage(array, name, default=extension, bit_depth=bit_depth, rescale=rescale)

    # --------------------
    # Save the whole stack
    def saveStack(self, name=None, extension='.tif', save_raw=False, bit_depth=16, rescale=True):

        # Define the name
        if name is None:
            name = _get_saved_name(self.name)

        # Select the array to save
        if save_raw:
            array = self.source
        else:
            array = self.array

        # Save the image
        saveImage(array, name, default=extension, bit_depth=bit_depth, rescale=rescale)

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# ---------------------------
# Load the image into a class
def getImageClass(array, name="Untitled"):

    # Generate the stack
    stack = ImageStack(array, name=name)

    return stack
