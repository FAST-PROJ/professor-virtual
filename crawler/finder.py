#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 14:54:50 2020

@author: Vinicius Alves
"""

import nltk
import pymysql

class Finder:
    def __init__(self):
        self.conn = None
        
    '''
        Abre uma conexão com a base de dados
    '''
    def getDatabaseConnection(self):        
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
        self.conn.close()
        
    '''
        Procura palavras salvas na base de dados
    '''
    def findWords(self, clause):
        list_fields = 'w1.id_url'
        list_tables = ''
        list_clauses = ''
        words_id = []
        
        words = clause.split(' ')
        count_table = 1
        for word in words:
            id_word = self.getIdWord(word)
            if id_word > 0:
                words_id.append(id_word)
                if count_table > 1:
                    list_tables += ', '
                    list_clauses += ' and '
                    list_clauses += 'w%d.id_url = w%d.id_url and ' % (count_table - 1, count_table)
                list_fields += ', w%d.location_page' % count_table
                list_tables += ' word_location w%d' % count_table
                list_clauses += 'w%d.id_word = %d' % (count_table, id_word)
                count_table += 1
        query = 'select %s from %s where %s' % (list_fields, list_tables, list_clauses)
        
        cursor = self.getDatabaseConnection()
        cursor.execute(query)
        rows = [row for row in cursor]
        cursor.close()
        self.closeDatabaseConnection()
        return rows, words_id

    '''
        Retorna o id da palavra pesquisada
    '''
    def getIdWord(self, word):
        INDEX_STATE = -1 # palavra não indexada
        cursor = self.getDatabaseConnection()
        stemmer = nltk.stem.RSLPStemmer()
        cursor.execute('select id_word from words where word = %s', stemmer.stem(word).lower())
        if cursor.rowcount > 0:
            INDEX_STATE = cursor.fetchone()[0]
        cursor.close()
        self.closeDatabaseConnection()
        return INDEX_STATE

    '''
        Busca simples de palavra
    '''
    def findOneWord(self, word):
        id_word = self.getIdWord(word)
        cursor = self.getDatabaseConnection()
        cursor.execute(
            'SELECT urls.url FROM word_location wlc' +
            ' INNER JOIN urls on wlc.id_url = urls.id_url' +
            ' WHERE wlc.id_word = %s', id_word
        )
        
        pages = set()
        for url in cursor:
            pages.add(url[0])
            
        for url in pages:
            print(url)
            
        cursor.close()
        self.closeDatabaseConnection()
    
    
finder = Finder()
finder.findOneWord('python')

rows = finder.findWords('python programação')
print(rows)
            
