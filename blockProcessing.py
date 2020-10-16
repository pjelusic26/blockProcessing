import math
import warnings
import numpy as np
from PIL import Image
import PIL
from skimage import color, transform

class squareBlocks:
    
    def blockDivide(img, blockNumber):
        """Divides grayscale square image into a number of square blocks.

        Arguments:
            img {string} -- path to input image.
            blockNumber {int} -- number of output square blocks.

        Raises:
            Warning: raised if input image is not square.
            Warning: raised if input image is not grayscale.

        Returns:
            ndarray -- array with a depth of {blockNumber}. Each layer represents one square image block.
        """

        imgArray = np.array(Image.open(img))

        if len(imgArray.shape) != 2:
            warnings.warn("Method will transform input image into grayscale.")
            imgArray = color.rgb2ycbcr(imgArray)
            imgArray = imgArray[:, :, 0]

        if imgArray.shape[0] != imgArray.shape[1]:
            warnings.warn("Method will transform input image into square format.")
            imgArray = transform.resize(imgArray, (np.amin(imgArray.shape), np.amin(imgArray.shape)))

        # Define dimension of image
        dimension = imgArray.shape[0]

        # Set number of slices per axis
        axisSlice = int(math.sqrt(blockNumber))

        # Size of each block
        arraySize = int(dimension / axisSlice)

        # Shape of numpy array to be filled
        blocksArray = np.zeros((arraySize, arraySize, blockNumber))

        # Split the image into vertical blocks
        split_a = np.split(imgArray, axisSlice, axis = 0)

        # Set counter to zero
        counter = 0

        for i in range(axisSlice):
            for j in range(axisSlice):

                # Split vertical blocks into square blocks
                split_b = np.split(split_a[i], axisSlice, axis = 1)

                # Fill array with blocks
                blocksArray[:, :, counter] = split_b[j]

                # Increase counter
                counter += 1

        return blocksArray

    def blockMerge(array):
        """Merges square blocks into a single image.

        Arguments:
            array {ndarray} -- 3D array containing image blocks.

        Returns:
            ndarray -- single image.
        """

        # Dimension of the input image
        blockSize = array.shape[0]

        # Number of blocks along an axis
        axisBlocks = int(math.sqrt(array.shape[2]))

        # Dimension of the output image
        dimension = array.shape[0] * axisBlocks

        # Creating Numpy Array for output image
        outputImage = np.zeros((dimension, dimension))

        # Starting position of x, y and z dimensions of array
        x, y, z = 0, 0, 0

        while y < dimension:
            while x < dimension:

                # Filling the array block by block
                outputImage[y : (y + blockSize), 
                            x : (x + blockSize)] = array[:, :, z]

                x += blockSize
                z += 1

            y += blockSize
            x = 0

        return outputImage

    def saveBlock(array):
        """Saves Image or each Image Block as JPG.

        Arguments:
            array {ndarray} -- input Image or Image Blocks.

        Returns:
            None.
        """

        # Blocks
        if len(array.shape) == 3:
            for i in range(array.shape[2]):
                imgObject = Image.fromarray(array[:, :, i].astype('uint8'), 'L')
                imgName = f"block_{i}.jpg"
                imgObject.save(imgName)

        # Single image
        elif len(array.shape) == 2:
            imgObject = Image.fromarray(array[:, :].astype('uint8'), 'L')
            imgName = f"block_image.jpg"
            imgObject.save(imgName)