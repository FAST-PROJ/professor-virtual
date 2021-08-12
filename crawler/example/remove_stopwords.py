import re
import nltk

'''
    uso do NLTK para remover as stopwords
'''
stopwords = nltk.corpus.stopwords.words('portuguese')
stopwords.append('é')
nltk.download('stopwords')
'''
    uso do NLTK para remover o radical das palavras
'''
stemmer = nltk.stem.RSLPStemmer()

'''
    Criação de expressão regular para dividar a sentença palavra por palavra
'''
sppliter = re.compile("([\W][\W']*)")

parsed_words = []
doc_words = [word for word in sppliter.split('Este lugar é apavorante demais a b c') if word != '']
for word in doc_words:
    word = word.strip()    
    if (word.lower() not in stopwords and len(word) > 1):
        parsed_words.append(stemmer.stem(word).lower())


print(parsed_words)