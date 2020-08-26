#!/usr/bin/env python
__author__     = "Vinicius Alves"
__copyright__  = "Copyright 2020, The FAST-PROJ Group"
__credits__    = ["Vinicius Alves"]
__license__    = "MIT"
__version__    = "1.0.0"
__maintainer__ = "FAST-PROJ"
__email__      = "#"
__status__     = "Development"

import urllib3
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import nltk
#nltk.download() - NLKT download wizard
import pymysql # conda install pymysql

# Crawler
class Crawler:
    def __init__(self, pages, max_depth=1):
        self.pages = pages
        self.max_depth = max_depth
        self.conn = None

    '''
        Abre uma conexão com a base de dados
    '''
    def getDatabaseConnection(self):
        # @todo Criar singleton para reutilizar o objeto de conexão
        #if self.conn == None:
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            passwd='root',
            db='crawler',
            autocommit=True
        )
        return self.conn.cursor()

    '''
        Fecha a conexão com a base de dados
    '''
    def closeDatabaseConnection(self):
        if self.conn != None:
            self.conn.close()

    '''
        Insere a palavra e sua localização na página na base de dados
    '''
    def insertWordLocationToDatabase(self, id_url, id_word, location):
        cursor = self.getDatabaseConnection()
        cursor.execute(
            'INSERT INTO word_location (id_url, id_word, location_page) VALUES(%s, %s, %s)',
            (id_url, id_word, location)
        )
        id_word_location = cursor.lastrowid
        cursor.close()
        self.closeDatabaseConnection()
        return id_word_location

    '''
        Insere a página indexada na base de dados
    '''
    def insertPageToDatabase(self, url):
        cursor = self.getDatabaseConnection()
        cursor.execute('INSERT INTO urls (url) VALUES(%s)', url)
        page_id = cursor.lastrowid
        cursor.close()
        self.closeDatabaseConnection()
        return page_id

    '''
        Verifica se a página já foi indexada pelo crawler
        Tipos de retorno da função
            -1 => A página ainda não indexada
            -2 A página foi indexada e possui palavras cadastras na base de dados
            id_url (número inteiro maior que 0) => Página indexa sem palavras cadastradas
    '''
    def isPageIndexed(self, url):
        INDEX_STATE = -1 # Página não indexada
        cursor = self.getDatabaseConnection()
        cursor.execute('select id_url from urls where url = %s', url)
        if cursor.rowcount > 0:
            id_url = cursor.fetchone()[0]
            cursor.execute('select id_url from word_location where id_url= %s', id_url)
            if cursor.rowcount > 0:
                INDEX_STATE = -2 # Página indexada com palavras cadastradas
            else:
                INDEX_STATE = id_url
        cursor.close()
        self.closeDatabaseConnection()

        return INDEX_STATE

    '''
        Indexa uma palavra na base de dados
    '''
    def insertWordToDatabase(self, word):
        cursor = self.getDatabaseConnection()
        cursor.execute('INSERT INTO words (word) VALUES(%s)', word)
        word_id = cursor.lastrowid
        cursor.close()
        self.closeDatabaseConnection()
        return word_id

    '''
        Verifica se uma palavra pertencente a uma página já foi indexada pelo crawler
        Tipos de retorno da função
            -1 => A palavra ainda não indexada
            id_word (número inteiro maior que 0) => A palavra foi já indexada pelo crawler
    '''
    def isWordIndexed(self, word):
        INDEX_STATE = -1 # palavra não indexada
        cursor = self.getDatabaseConnection()
        cursor.execute('select id_word from words where word = %s', word)

        if cursor.rowcount > 0:
            INDEX_STATE = cursor.fetchone()[0]

        cursor.close()
        self.closeDatabaseConnection()
        return INDEX_STATE # palavra não indexada

    '''
        Retorna os textos parseados - Selecionando o radical da palavra
    '''
    def splitWords(self, sentence):
        stopwords = nltk.corpus.stopwords.words('portuguese')
        stopwords.append('é')
        '''
            uso do NLTK para remover o radical das palavras
        '''
        stemmer = nltk.stem.RSLPStemmer()

        '''
            Criação de expressão regular para dividar a sentença palavra por palavra
        '''
        sppliter = re.compile("([\W][\W']*)")

        parsed_words = []
        doc_words = [word for word in sppliter.split(sentence) if word != '']
        for word in doc_words:
            word = word.strip()
            if (word.lower() not in stopwords and len(word) > 1):
                parsed_words.append(stemmer.stem(word).lower())

        return parsed_words

    '''
        Retorna o texto bruto - Removendo as tags HTML
    '''
    def getRawText(self, soup):
        for tags in soup(['script', 'style']):
            tags.decompose()
        return ' '.join(soup.stripped_strings)

    '''
        Faz a indexação das palavras e das páginas
    '''
    def indexer(self, url, soup):
        print('Indexing page: ' + str(url))
        indexed = self.isPageIndexed(url)
        if indexed == -2:
            print('Page indexed')
            return
        elif indexed == -1:
            id_new_page = self.insertPageToDatabase(url)
        elif indexed > 0:
            id_new_page = indexed

        text = self.getRawText(soup)
        words = self.splitWords(text)
        for position in range(len(words)):
            word = words[position]
            indexed = self.isWordIndexed(word)
            if indexed == -1:
                print('indexing word: ' + str(word))
                id_word = self.insertWordToDatabase(word)
            self.insertWordLocationToDatabase(id_new_page, id_word, position)

    '''
      Cria um pool http para parsear as paginas
      Itera até a profundidade máxima definida pelo usuário
      Itera por cada página na lista de páginas definida pelo usuário
      Chama o método parser dos links
    '''
    def run(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        for i in range(self.max_depth):
            for page in self.pages:
                http = urllib3.PoolManager()
                try:
                    searched_page = http.request('GET', page)
                    print('reading page: ' + str(page))
                    self.parsePageLinks(page, searched_page.data)
                except Exception as e:
                    print('Failed: '+ str(e))

    '''
      Faz o parser dos links existentes na página atual
      Adiciona a página parseada à lista de páginas a serem visitadas
      Executa o pré-processamento de limpeza os dados da URL da página
    '''
    def parsePageLinks(self, page, data):
        soup = BeautifulSoup(data, features="lxml")
        self.indexer(page, soup)

        links = soup.find_all('a')
        links_counter = 1
        # lista de páginas seguidas pelo crawler
        followed_pages = set()

        for link in links:
            print('parsing link: ' + str(link))
            if ('href' in link.attrs):
                # Juntando uma URL com caminh relativo à URL BASE da página
                url = urljoin(page, str(link.get('href')))

                # Ignora a URL caso possua uma apóstrofe
                if url.find("'") != -1:
                    continue

                '''
                  Se a URL for uma ancôra da própria página
                  Quebra a URL em um array e utilia apenas o primeiro elemento do array
                '''
                url = url.split('#')[0]

                # Verifição de protocolo http
                if url[0:4] == 'http':
                    print('Appending url: ' + str(url))
                    followed_pages.add(url)

                links_counter += 1

        self.pages = followed_pages

        print('página: ' + page)
        print('total de links: ' + str(links_counter))
        print(len(self.pages))

crawl = Crawler(
  [
    'https://pt.wikipedia.org/wiki/Linguagem_de_programa%C3%A7%C3%A3o'
  ],
  max_depth=2
)
crawl.run()

#crawl.isWordIndexed('linguagem')
#crawl.insertWordLocationToDatabase(1, 1, 50)
#crawl.insertWordToDatabase('linguagem')
#crawl.isPageIndexed('teste')
#crawl.insertPageToDatabase('https://pt.wikipedia.org/wiki/Linguagem_de_programa%C3%A7%C3%A3o')