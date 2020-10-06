import site
site.addsitedir("/pdftron/PDFNetWrappers/PDFNetC/Lib")
from PDFNetPython import *
import sys

PDFNet.Initialize()


def compress_pdf(input_fp, output_fp):
    doc = PDFDoc(input_fp)
    doc.InitSecurityHandler()
    image_settings = ImageSettings()
    
    # low quality jpeg compression
    image_settings.SetCompressionMode(ImageSettings.e_jpeg)
    image_settings.SetQuality(1)
    
    # Set the output dpi to be standard screen resolution
    image_settings.SetImageDPI(144,96)
    
    # this option will recompress images not compressed with
    # jpeg compression and use the result if the new image
    # is smaller.
    image_settings.ForceRecompression(True)
    
    # this option is not commonly used since it can 
    # potentially lead to larger files.  It should be enabled
    # only if the output compression specified should be applied
    # to every image of a given type regardless of the output image size
    #image_settings.ForceChanges(True)

    opt_settings = OptimizerSettings()
    opt_settings.SetColorImageSettings(image_settings)
    opt_settings.SetGrayscaleImageSettings(image_settings)

    # use the same settings for both color and grayscale images
    Optimizer.Optimize(doc, opt_settings)
    
    doc.Save(output_fp, SDFDoc.e_linearized)
    doc.Close()
