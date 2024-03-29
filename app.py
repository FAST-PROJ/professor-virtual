#!/usr/bin/env python
__author__     = "Mateus Ferreira"
__copyright__  = "Copyright 2020, The FAST-PROJ Group"
__credits__    = ["Mateus Ferreira"]
__license__    = "MIT"
__version__    = "1.0.0"
__maintainer__ = "FAST-PROJ"
__email__      = "#"
__status__     = "Development"

from flask import Flask, request
from etl.mysql import dbConnection
from etl.reader import Reader
from etl.cleaner import Cleaner
from etl.feature import Feature
import pandas as pd

app = Flask(__name__)

# Inicia a classe de conexão com o banco
connection = dbConnection()
# Inicia a classe de leitura do arquivo
reader = Reader()
# Inicia a classe de limpeza
cleaner = Cleaner()
# Inicia a classe de features
feature = Feature()

@app.route('/insertFiles', methods=['POST'])
def insertFiles():
    input_json = request.get_json(force=True)
    print(input_json)
    connection.insertFile(input_json['file_name'])
    return '200'

@app.route('/processFiles', methods=['POST'])
def processFiles():
    input_json = request.get_json(force=True)
    rawText(input_json['id'])
    refinedText()
    featureText()
    return '200'

def rawText(id):

  # Preenche o parametro de fileId
  reader.setFileId(id)

  # Coleta as informações do banco de dados a partir do id do arquivo
  file = connection.getFile(reader.getFileId())

  # Leitura do arquivo da pasta source
  reader.setTextFromPdf(f"{file['name']}")

  # Cria um dicionario com as informações do arquivo
  rawText = {
              "id": [reader.getFileId()], 
              "text":[reader.getTextFromPdf()]
  }

  # Efetua o insert na camada bronze
  connection.insertRawText(pd.DataFrame(data=rawText))

def refinedText():
  
  numbersClean = cleaner.removeIsolatedNumbers(reader.getTextFromPdf())
  spaceClean = cleaner.removeSpaces(numbersClean)
  blankClean = cleaner.removeBlankLines(spaceClean)
  cleanText = cleaner.removeSpecialCaracteres(blankClean)
  cleaner.setCleanText(cleanText)

  # Cria um dicionario com as informações do arquivo
  refinedText = {
              "id": [reader.getFileId()],
              "text":[cleaner.getCleanText()]
  }

  # Efetua o insert na camada silver
  connection.insertRefinedText(pd.DataFrame(data=refinedText))

def featureText():

  feature.setSentenceToList(cleaner.getCleanText())
  feature.setWordToList(cleaner.getCleanText())

  # Cria um dicionario com as informações do arquivo
  featureText = {
              "id": [reader.getFileId()],
              "word":[str(feature.getWordToList())],
              "sentence":[str(feature.getSentenceToList())]
  }

  # Efetua o insert na camada gold
  connection.insertFeatureText(pd.DataFrame(data=featureText))
