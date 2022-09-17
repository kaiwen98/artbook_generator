import win32com.client
import os
from commons import utils

srcFilePath = os.path.join(os.getcwd(), "ExtravaganzaBookArtTemplate.psd")
destFilePath = os.path.join(os.getcwd(), "ExtravaganzaBookArtTemplate1.pdf")

class Photoshop():
    def __init__(self, srcFilePath):
        self.psApp = win32com.client.Dispatch("Photoshop.Application")


        self.psApp.Open(srcFilePath)
        self.document = self.psApp.Application.ActiveDocument
        

    def modifyLayerText(self, layerName, text):
        layer = self.document.ArtLayers[layerName]
        layer.TextItem.contents = text

    def addImageToLayer(self, layerName, imageFilePath):
        utils.resizeImageToA4(imageFilePath)
        selectedLayers = list(filter(
            lambda layer : layer.name == layerName, 
            self.document.ArtLayers))

        if len(selectedLayers) == 0:
            print("[ERRO] Layer not found")
            return

        print("[INFO] Layer found")
        selectedLayer = selectedLayers[0]
        self.psApp.Application.ActiveDocument.ActiveLayer = selectedLayer
        desc = win32com.client.Dispatch("Photoshop.ActionDescriptor")
        nullId = self.psApp.CharIDToTypeID("null")
        desc.PutPath(nullId, imageFilePath)
        eventId = self.psApp.StringIDToTypeID("placedLayerReplaceContents")
        self.psApp.ExecuteAction(eventId, desc)
        print(selectedLayer.Bounds)

    def saveAsPdf(self, destFilePath):
        # Configure options
        options = win32com.client.Dispatch('Photoshop.PDFSaveOptions')
        options.Encoding = 2
        options.Layers = False
        options.OptimizeForWeb = True
        options.JPEGQuality = 12

        # Save Photoshop as PDF
        self.document.SaveAs(SaveIn=destFilePath, Options=options, ExtensionType=2)