from PIL import Image
import os
import math
import re
from pdf2image import convert_from_path
import PyPDF2
import img2pdf
from pathlib import Path

from commons.constants import (
    ARTBOOK_OUTPUT_PATH, 
    ASSET_IN_PATH, 
    ASSET_OUT_PATH, 
    GSHEET_REGISTRATION_COL,
    GSHEET_SUBMISSION_CATEGORY, 
    GSHEET_SUBMISSION_COL
)

A4_PX_DIMENSION = (2480, 2480)

def replaceEscapeChars(string):
    """Replaces escape characters with hex (\x03) representing line feed in Photoshop.

    Args:
        string (string): string to replace escape characters

    Returns:
        string: The processed string.
    """
    return re.sub('(?<!(\r))\n', '\x03', string)

# Text

def generateArttextPdf(
    ps,
    dfCompleteRow,
    category,
    fileName
):
    """Generate the text page for a given artist.

    Args:
        ps (PhotoshopApp): The photoshop application object.
        dfCompleteRow (Series): The pandas row representing the artist particulars.
        category (GSHEETS_SUBMISSION_CATEGORY): The category of the artist. 
        fileName (string): The root name of the file to save the assets with.
    """
    ps.modifyLayerText("ArtworkTitle", 
        replaceEscapeChars(f'''{dfCompleteRow[GSHEET_SUBMISSION_COL.ARTWORK_TITLE.value]}''')
    )

    ps.modifyLayerText("ArtworkDesc", 
        replaceEscapeChars(f'''{dfCompleteRow[GSHEET_SUBMISSION_COL.ARTWORK_TEXT.value]}''')
    )

    print(repr(
        replaceEscapeChars(f'''{dfCompleteRow[GSHEET_SUBMISSION_COL.ARTWORK_TEXT.value]}''')
    ))

    ps.modifyLayerText("ArtistDesc", 
        replaceEscapeChars(getParticipantDesc(dfCompleteRow))
    )

    ps.saveAsPdf(
        os.path.join(ARTBOOK_OUTPUT_PATH, category, f"{fileName}_Text.pdf")
    )

# Artwork

def getCenteredOffset(bgSize, imageSize):
    """Get the offset to align and justify the image to the center of the page.

    Args:
        bgSize ((int, int)): W-H coordinates of the background.
        imageSize ((int, int)): W-H coordinates of the image.

    Returns:
        (int, int): The W-H coordinates of the offset of which the image must translate by.
    """
    return ((bgSize[0] - imageSize[0]) // 2, (bgSize[1] - imageSize[1]) // 2)

def generateArtworkPdfFromPdf(imageFilePath, backgroundFilePath, outputFilePath, rotateAngle):
    """Given a PDF of multiple pages, generate a suitably named series of Artwork PDFs

    Args:
        imageFilePath (string): path to the artwork PDF file.
        backgroundFilePath (string): path to the background PDF file.
        outputFilePath (string): path to the output PDF file.
        rotateAngle (int): the anti-clockwise angular translation to oriente the artwork. To be set in submission sheet.
    """
    images = convert_from_path(imageFilePath)
    for id, image in enumerate(images, start=1):
        currOutputFilePath = os.path.splitext(outputFilePath)[0] + f"_{id}" +  os.path.splitext(outputFilePath)[1]
        pasteImageOnBackgroundAndSave(image, backgroundFilePath, currOutputFilePath, rotateAngle)

def pasteImageOnBackgroundAndSave(image, backgroundFilePath, outputFilePath, rotateAngle):
    """Interfaces with PIL API to paste the image onto the backgroun to generate an Artwork PDF.

    Args:
        image (PIL.Image): Image object generated from file path.
        backgroundFilePath (string): path to the background file.
        outputFilePath (string): path to the output file.
        rotateAngle (int): the anti-clockwise angular translation to oriente the artwork. To be set in submission sheet.
    """
    print("pasting...")
    image = image.rotate(rotateAngle, fillcolor=(255, 255, 255, 0), expand=True)
    imageHeight = image.size[1]
    newImageHeight = math.ceil(imageHeight * A4_PX_DIMENSION[0] / image.size[0])
    outfile = os.path.splitext(outputFilePath)[0] + ".pdf"
    
    image = image.resize(
        (A4_PX_DIMENSION[0], newImageHeight),
        Image.ANTIALIAS
    )

    backgroundImage = Image.open(backgroundFilePath)
    offset = getCenteredOffset(backgroundImage.size, image.size)
    backgroundImage.paste(image, offset)
    backgroundImage.save(outfile, format="pdf", resolution=300)

def generateArtworkPdf(imageFilePath, backgroundFilePath, outputFilePath, rotateAngle = 0):
    """Generate a suitably named Artwork PDF

    Args:
        imageFilePath (string): path to the artwork file.
        backgroundFilePath (string): path to the background file.
        outputFilePath (string): path to the output file.
        rotateAngle (int): the anti-clockwise angular translation to oriente the artwork. To be set in submission sheet.
    """
    ext = os.path.splitext(imageFilePath)[1]
    print(ext)
    if ext == '.pdf':
        generateArtworkPdfFromPdf(imageFilePath, backgroundFilePath, outputFilePath, rotateAngle)
    else:
        image = Image.open(imageFilePath)
        pasteImageOnBackgroundAndSave(image, backgroundFilePath, outputFilePath, rotateAngle)

def getGidFromGdriveUrl(url):
    """Parse a Gdrive share link/upload link to retrieve the Gdrive Id.

    Args:
        url (string): Gdrive URL

    Returns:
        string: Gdrive Id
    """
    # To deal with a different gdrive url format
    url = url.replace(r'file/d/', "?id=")
    url = re.sub(r'(\/v.*)', "", url)
    return re.split(r'\?id\=', url)[1]

def getPdfName(dfCompleteRow):
    """Generate the root name of the PDF files for each artist. Note that the naming format is deliberate in consideration of the desirable order of which the pages are arranged in the exported PDF. In this case, they are ordered by school.

    Args:
        dfCompleteRow (Series): Pandas row representing the artist particulars.

    Returns:
        string: the PDF name.
    """
    # Reference title:
    # {CATEGORY}.{Name}
    print(f"{dfCompleteRow[GSHEET_SUBMISSION_COL.CATEGORY.value]}-{dfCompleteRow[GSHEET_REGISTRATION_COL.SCHOOL.value]}-{dfCompleteRow[GSHEET_REGISTRATION_COL.NAME.value]}".replace(" ", "_"))
    return f"{dfCompleteRow[GSHEET_SUBMISSION_COL.CATEGORY.value]}-{dfCompleteRow[GSHEET_REGISTRATION_COL.SCHOOL.value]}-{dfCompleteRow[GSHEET_REGISTRATION_COL.NAME.value]}"\
        .replace(" ", "_")\
        .replace("/", "")

def resolveArtworkFinalUrl(dfCompleteRow):
    """In the submission sheet, each category will have its own three rows of final, wip1 and wip2 submission. 
    This function resolves the supplied category to the row pointing to the final artwork.

    Args:
        dfCompleteRow (Series): Pandas row representing the artist particulars.

    Returns:
        string: The google drive url under the correct final artwork column.
    """
    if dfCompleteRow[GSHEET_SUBMISSION_COL.CATEGORY.value] == GSHEET_SUBMISSION_CATEGORY.COMIC.value:
        return dfCompleteRow[GSHEET_SUBMISSION_COL.COMIC_FINAL.value]
    elif dfCompleteRow[GSHEET_SUBMISSION_COL.CATEGORY.value] == GSHEET_SUBMISSION_CATEGORY.TRAD.value:
        return dfCompleteRow[GSHEET_SUBMISSION_COL.TRAD_FINAL.value]
    elif dfCompleteRow[GSHEET_SUBMISSION_COL.CATEGORY.value] == GSHEET_SUBMISSION_CATEGORY.DIGITAL.value:
        return dfCompleteRow[GSHEET_SUBMISSION_COL.DIGITAL_FINAL.value]

def getParticipantDesc(dfCompleteRow):
    """Generate a formatted description of the artist based on particulars.

    Args:
        dfCompleteRow (Series): Pandas row representing the artist particulars.

    Returns:
        string: The description.
    """
    return f'''{dfCompleteRow[GSHEET_REGISTRATION_COL.NAME.value]} ({dfCompleteRow[GSHEET_REGISTRATION_COL.AGE.value]})\x03{dfCompleteRow[GSHEET_REGISTRATION_COL.SCHOOL.value]}'''

def generateCombinedPdfFromFiles(category:GSHEET_SUBMISSION_CATEGORY=None):
    """Pools together all the generate individual PDF files to generate a compiled multipage PDF document.

    Args:
        category (GSHEET_SUBMISSION_CATEGORY, optional): If specified, only artworks of the given category will be generated. Defaults to None.
    """
    pdfPages = [
        open(os.path.join(ASSET_IN_PATH, "Extravaganza_Cover.pdf"), 'rb'),
        ]
    
    if not category: 
        pdfPages.append(
            open(os.path.join(ASSET_IN_PATH, "Extravaganza_Foreword.pdf"), 'rb'),
            open(os.path.join(ASSET_IN_PATH, "Extravaganza_WS.pdf"), 'rb')
        )

    pdfWriter =PyPDF2.PdfFileWriter()
    
    for folder in os.listdir(os.path.join(ASSET_OUT_PATH, "artbook")):
        print(folder)
        if \
            category != None \
            and folder != category.value:
            continue

        if folder == GSHEET_SUBMISSION_CATEGORY.COMIC.value:
            categoryPage = "Extravaganza_Comic.pdf"
        if folder == GSHEET_SUBMISSION_CATEGORY.DIGITAL.value:
            categoryPage = "Extravaganza_Digital.pdf"
        if folder == GSHEET_SUBMISSION_CATEGORY.TRAD.value:
            categoryPage = "Extravaganza_Traditional.pdf"

        pdfPages.append(
            open(os.path.join(ASSET_IN_PATH, categoryPage), 'rb')
        )

        for file in os.listdir(os.path.join(ASSET_OUT_PATH, "artbook", folder)):
            print(file)
            pdfPages.append(
                open(os.path.join(ASSET_OUT_PATH, "artbook", folder, file), 'rb')
            )
    
    pdfPages.append(
        open(os.path.join(ASSET_IN_PATH, "Extravaganza_Back.pdf"), 'rb')
        )

    for page in pdfPages:
        # pageReader = PyPDF2.PdfFileReader(page)
        # print("PDF SIZE: ", pageReader.pages[0].mediabox)
        pdfPage = PyPDF2.PdfFileReader(page).getPage(0)
        # pdfPage.compress_content_streams()
        pdfWriter.addPage(pdfPage)

    pdfOutputFile = open(os.path.join(ASSET_OUT_PATH, "Extravaganza_Artbook.pdf"), 'wb')
    pdfWriter.write(pdfOutputFile)

    for page in pdfPages:
        page.close()
