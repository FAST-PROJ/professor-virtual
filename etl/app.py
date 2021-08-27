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
from reader import Reader
from cleaner import Cleaner
from mysql import dbConnection
import pandas as pd

# Inicia a classe de conexão com o banco
connection = dbConnection()
# Inicia a classe de leitura do arquivo
reader = Reader()
# Inicia a classe de limpeza
cleaner = Cleaner()


def rawText(id):

  # Preenche o parametro de fileId
  reader.setFileId(id)

  # Coleta as informações do banco de dados a partir do id do arquivo
  file = connection.getFile(reader.getFileId())

  # Leitura do arquivo da pasta source
  reader.setTextFromPdf(f"{file['name']}")

  text = reader.getTextFromPdf

  #Cria um dicionario com as informações do arquivo
  rawText = {
              "id": [reader.getFileId()], 
              "text":[text]
  }

  #Efetua o insert na camada bronze
  connection.insertRawText(pd.DataFrame(data=rawText))

def refinedText():
  
  numbersClean = cleaner.removeIsolatedNumbers(reader.getTextFromPdf())
  spaceClean = cleaner.removeSpaces(numbersClean)
  blankClean = cleaner.removeBlankLines(spaceClean)
  cleanText = cleaner.removeSpecialCaracteres(blankClean)

  #Cria um dicionario com as informações do arquivo
  refinedText = {
              "id": [reader.getFileId()],
              "text":[cleanText]
  }

  #Efetua o insert na camada bronze
  connection.insertRefinedText(pd.DataFrame(data=refinedText))

rawText(1)
refinedText()

# sentences = cleaner.sentenceToList(cleanText)
# words = cleaner.wordToList(cleanText)
