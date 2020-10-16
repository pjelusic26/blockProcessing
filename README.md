# blockProcessing
Python script for dividing a single image into a number of square blocks.

I needed something like this for my work in weeks past, but found no such modules, so I decided to write it myself. Hopefully someone will find it useful.

Some notes below:
- Only works if the Number of Blocks = 4^n (4, 16, 64, ...)
- Can only divide a square image into square blocks
- Divides both axes to a same number of blocks

TO DO:
- Make other number of blocks possible
- Find a way to input non-square images
- Find a way to divide axes into different number of blocks
