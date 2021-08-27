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
import os
import re

class Cleaner:
  def removeIsolatedNumbers(self, text):
    return re.sub(r"^\d+[^\w-]", "", text, flags=re.MULTILINE)
  
  def removeSpaces(self, text):
    return re.sub(r"(^ +)|( +$)", "", text, flags=re.MULTILINE)

  def removeBlankLines(self, text):
    return re.sub(r"^(?:[\t ]*(?:\r?[\n\r]))+", "", text, flags=re.MULTILINE)

  def removeSpecialCaracteres(self, text):
    special = re.sub(r'[ç]', 'c', text)
    a = re.sub(r'[áâãà]', 'a', special)
    e = re.sub(r'[éêè]', 'e', a)
    i = re.sub(r'[íîì]', 'i', e)
    o = re.sub(r'[óôõò]', 'o', i)
    u = re.sub(r'[úûù]', 'u', o)
    return re.sub(r'[\(\)]', '', u)

  def sentenceToList(self, text):
    return re.findall("[^\n]+", text, flags=re.M)

  def wordToList(self, text):
    return re.findall("\w+", text, flags=re.M)
