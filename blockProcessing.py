import math
import warnings

import numpy as np
from PIL import Image
import PIL
from skimage import color, transform

import glob
import os
from pathlib import Path

class blockProc:
    
    @staticmethod
    def blockDivide(img, blocksWidth, blocksHeight):
        """Divides input image into {blocksWidth} * {blocksHeight} blocks.

        Args:
            img (string): Path to input image.
            blocksWidth (int): Desired number of blocks per axis.
            blocksHeight (int): Desired number of blocks per axis.

        Raises:
            AttributeError: If axis dimension is not divisible with {blocksWidth}.
            AttributeError: If axis dimension is not divisible with {blocksHeight}.

        Returns:
            [ndarray]: Array of blocks, with third axis representing the number of blocks.
        """

        # Read image
        imgArray = np.array(Image.open(img))

        # Warning if image is not grayscale and transform to grayscale
        if len(imgArray.shape) != 2:
            warnings.warn("Method will transform input image into grayscale.")
            imgArray = color.rgb2ycbcr(imgArray)
            imgArray = imgArray[:, :, 0]

        # Set output array depth
        arraySizeZ = blocksWidth * blocksHeight
        
        # Size of each block
        arraySizeX = int(imgArray.shape[1] / blocksWidth)
        arraySizeY = int(imgArray.shape[0] / blocksHeight)

        if imgArray.shape[0] % blocksHeight != 0:
            raise AttributeError(
        f"Can not compute ({imgArray.shape[0]} / {blocksHeight}). Please provide a number of blocks divisible with original height.")

        if imgArray.shape[1] % blocksWidth != 0:
            raise AttributeError(
        f"Can not compute ({imgArray.shape[1]} / {blocksWidth}). Please provide a number of blocks divisible with original height.")

        # Shape of numpy array to be filled
        outputBlocks = np.zeros((arraySizeY, arraySizeX, arraySizeZ))

        # Split the Y channel of the image into vertical blocks
        split_a = np.split(imgArray, blocksHeight, axis = 0)

        # Set counter to zero
        counter = 0

        for i in range(blocksHeight):
            for j in range(blocksWidth):

                # Split vertical blocks into square blocks
                split_b = np.split(split_a[i], blocksWidth, axis = 1)

                # Fill Numpy array with blocks
                outputBlocks[:, :, counter] = split_b[j]

                # Increase counter
                counter += 1

        return outputBlocks

    @staticmethod
    def blockMerge(array, imgWidth, imgHeight):
        """Merges image blocks into a grayscale image.

        Args:
            array (ndarray): Containing image blocks with third axis representing the number of blocks.
            imgWidth (int): Width of full image.
            imgHeight (int): Height of full image.

        Returns:
            (ndarray): Array containing full grayscale image.
        """

        # Dimension of the input image
        blockSizeX = array.shape[1]
        blockSizeY = array.shape[0]

        # Number of blocks along an axis
        blocksAlongX = imgWidth / blockSizeX
        blocksAlongY = imgHeight / blockSizeY

        # Creating Numpy Array for output image
        outputImage = np.zeros((imgHeight, imgWidth))

        # Counter for indexing each block from input array
        depthCounter = 0

        # Starting position of X
        x = 0

        # Starting position of Y
        y = 0

        while y < imgHeight:
            while x < imgWidth:
                outputImage[y : (y + blockSizeY), 
                            x : (x + blockSizeX)] = array[:, :, depthCounter]
                x += blockSizeX
                depthCounter += 1

            y += blockSizeY
            x = 0

        return outputImage

    @staticmethod
    def saveBlock(array):
        """Saves blocks or full image as JPG.

        Args:
            array (ndarray): Contains either blocks or full image.
        """

        # Source Directory
        src_folder = os.getcwd()
        # Source Path
        src_pth = Path(src_folder).resolve()

        # Blocks
        if len(array.shape) == 3:

            # Creating folder for blocks
            dst_folder = Path(src_folder+'/savedBlocks/').resolve()
            Path(dst_folder).mkdir(exist_ok = True)

            # Saving blocks
            for i in range(array.shape[2]):
                imgObject = Image.fromarray(array[:, :, i].astype('uint8'), 'L')
                imgName = f"{str(dst_folder)}/block_{i}.jpg"
                imgObject.save(imgName)

        # Single image
        elif len(array.shape) == 2:
    
            # Creating folder for blocks
            dst_folder = Path(src_folder+'/savedImage/').resolve()
            Path(dst_folder).mkdir(exist_ok = True)

            # Saving image
            imgObject = Image.fromarray(array[:, :].astype('uint8'), 'L')
            imgName = f"{str(dst_folder)}/imageFull.jpg"
            imgObject.save(imgName)