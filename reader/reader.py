#!/usr/bin/env python
__author__     = "Mateus Ferreira"
__copyright__  = "Copyright 2020, The FAST-PROJ Group"
__credits__    = ["Mateus Ferreira"]
__license__    = "MIT"
__version__    = "1.0.0"
__maintainer__ = "FAST-PROJ"
__email__      = "#"
__status__     = "Development"

from pdfminer.high_level import extract_text
import os

class Reader:
  def __init__(self):
    self.sourcePath = Reader.setSourceDataPath()

  def setSourceDataPath():
    return os.path.join(os.getcwd(), "reader", "source")

  def getTextFromPdf(self, fileName):
    try:
      text = extract_text(f"{self.sourcePath}\{fileName}.pdf")
    except Exception as e:
      raise(str(e))
    return text

reader = Reader()
text = reader.getTextFromPdf('manual_ps5')

print(text)

