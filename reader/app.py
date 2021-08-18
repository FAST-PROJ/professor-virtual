#!/usr/bin/env python
__author__     = "Mateus Ferreira"
__copyright__  = "Copyright 2020, The FAST-PROJ Group"
__credits__    = ["Mateus Ferreira"]
__license__    = "MIT"
__version__    = "1.0.0"
__maintainer__ = "FAST-PROJ"
__email__      = "#"
__status__     = "Development"

from pdfminer.high_level import extract_text # pip install pdfminer.six
from reader import Reader, Cleaner
from mysql import dbConnection
import pandas as pd

connection = dbConnection()
reader = Reader()

for file in connection.getFiles():
  text = reader.getTextFromPdf(f"{file['name']}")
  cleaner = Cleaner(text)
  numbersClean = cleaner.removeIsolatedNumbers(text)
  spaceClean = cleaner.removeSpaces(numbersClean)
  blankClean = cleaner.removeBlankLines(spaceClean)
  cleanText = cleaner.removeSpecialCaracteres(blankClean)
  sentences = cleaner.sentenceToList(cleanText)
  words = cleaner.wordToList(cleanText)


  insertList = {
                  "id": [file['id']], 
                  "text":[text], 
                  "clean":[cleanText], 
                  "sentence": [', '.join(sentences)], 
                  "word":[', '.join(words)]
  }

  connection.insertFileText(pd.DataFrame(data=insertList))
