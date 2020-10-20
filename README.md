# blockProcessing
Python script for dividing a single image into a finite number of blocks.

I needed something like this for my work in weeks past, but found no such modules, so I decided to write it myself. Hopefully someone will find it useful. Inside the repository you can find the Python script, a Jupyter Notebook example that works and two input images - one square and one horizontal. You can use both of them for the current version of the method.

Some notes below:
- Only works if axis size is divisible with desired number of blocks
- If the input image is RGB, the method transforms it into grayscale

TO DO:
- Find a way to add padding around the image in order to make all number of blocks possible
- Expand the method to be able to output RGB blocks/ images as well
