from blockProcessing import blockProc

# Divide image into blocks
imgBlocks = blockProc.blockDivide('images/inputImage.jpg', blocksWidth = 5, blocksHeight = 8)

# Save image blocks
blockProc.saveBlock(imgBlocks)

# Merge image blocks into single image
imgFull = blockProc.blockMerge(imgBlocks, imgWidth = 1800, imgHeight = 1800)

# Save full image
blockProc.saveBlock(imgFull)