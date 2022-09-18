import win32com.client
import os
from models.Photoshop import Photoshop
from models.GDrive import GDrive
from models.GSheets import GSheet
from commons import utils

assetPath = os.path.join(os.getcwd(), "assets")
assetInPath = os.path.join(assetPath, "in")
assetOutPath = os.path.join(assetPath, "out")

imageFilePath = os.path.join(assetInPath, "photo_2022-08-20_11-13-16.jpg")
outputFilePath = os.path.join(assetOutPath, "testa-art.pdf")
backgroundFilePath = os.path.join(assetInPath, "seed", "ExtravaganzaBookArtworkTemplate.png")

srcFilePath = os.path.join(assetInPath, "seed", "ExtravaganzaBookArttextTemplate.psd")
destFilePath = os.path.join(assetOutPath, "testa-text.pdf")

if __name__ == "__main__":
    gsheet = GSheet()
    
    # gdrive = GDrive()
    # gdrive.retrieve('13nvV-c4scnwv_0H5Qdfte83XR4wLSYHE', 'hi')


    # ps = Photoshop(srcFilePath)

    # utils.generateArtworkPdf(
    #     imageFilePath,
    #     backgroundFilePath,
    #     outputFilePath
    # )
    # ps.modifyLayerText("ArtworkTitle", 
    # '''Starry Night above the Moon
    # Starry Night above the Moon'''
    # )
    # ps.saveAsPdf(destFilePath)



