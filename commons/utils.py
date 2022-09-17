from PIL import Image
import os
import math
A4_PX_DIMENSION = (2480, 2480)

def getCenteredOffset(bgSize, imageSize):
    return ((bgSize[0] - imageSize[0]) // 2, (bgSize[1] - imageSize[1]) // 2)

def generateArtworkPdf(imageFilePath, backgroundFilePath, outputFilePath):

    image = Image.open(imageFilePath)
    imageHeight = image.size[1]
    newImageHeight = math.ceil(imageHeight * A4_PX_DIMENSION[0] / image.size[0])
    outfile = os.path.splitext(outputFilePath)[0] + ".pdf"

    image = image.resize(
        (A4_PX_DIMENSION[0], newImageHeight),
        Image.ANTIALIAS
    )

    backgroundImage = Image.open(backgroundFilePath)
    print(image.size)
    print(backgroundImage.size)
    offset = getCenteredOffset(backgroundImage.size, image.size)
    backgroundImage.paste(image, offset)

    backgroundImage.save(outfile, format="pdf", quality=100, subsampling=0)