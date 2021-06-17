import os, re
import heapq
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer

configFile  = 'RelevantWordsConfig.txt'
STOPProp  = 'STOP_det'

class RelevantWordsTask:
    
    enabled = False
    configDir = None
    
    def isEnabled(self):
        return True
        
    def init(self, confProps, configFolder):
        
        from java.io import File
        from dpf.sp.gpinf.indexer.util import UTF8Properties
        extraProps = UTF8Properties()
        extraProps.load(File(configFolder, configFile))
        STOP_det = extraProps.getProperty(STOPProp)      
        global STOP
        
        def Convert(string):
           li = list(string.split(" "))
           return li
           
        if STOP_det is not None:
           STOP = Convert(str(STOP_det)) 
        return 
    
    def finish(self):      
        return 
        
    def process(self, item):
        
        categories = item.getCategorySet().toString()
        if not ("Chats" in categories or "Emails" in categories):
           return 
        
        text = str(item.getParsedTextCache()).lower()
        #Retirando números
        text = re.sub(r'\d+','',text)
        #Tokenização
        tokenizer = RegexpTokenizer(r'\w+')
        Text_separed_from_words = tokenizer.tokenize(text)   
        #Importando as stopwords do arquivo txt
        All_stopwords = STOP
        
        def remove_stopwords(words, stopwords):
           #Retirando as stop words
           words_without_stopwords = []
           for item in words:
              if item not in stopwords:
                 words_without_stopwords.append(item)
           #Retirando palavras com menos de 3 letras
           for item in words_without_stopwords:
              if len(item) < 3:
                 words_without_stopwords.remove(item)
           #Retirando risadas "kkk" 
           for item in words_without_stopwords:
              characters_word = item.split()
              for i in characters_word:
                contLetra = i.count('k')
                if contLetra >= 2:
                   words_without_stopwords.remove(item)                 
           return words_without_stopwords
         
        def Create_bag_of_words(words):
           wordfreq ={}
           for item in words:
              if item not in wordfreq.keys():
                 wordfreq[item] = 1
              else:
                 wordfreq[item] += 1     
           return wordfreq
           
        words_without_stopwords = remove_stopwords(Text_separed_from_words, All_stopwords)
        
        def stemming(words):
            stem = PorterStemmer()
            for item in words:
               item = stem.stem(item)
            return words
        #Stemmização das palavras -- Não tenho certeza se está fazendo muita diferença, mas é uma função do NLTK
        words_without_stopwords = stemming(words_without_stopwords)
        
        Bag_of_words = Create_bag_of_words(words_without_stopwords)
        #Seleção das 10 palavras com maiores frequências
        most_freq = heapq.nlargest(10, Bag_of_words, key=Bag_of_words.get) 
        item.setExtraAttribute('RelevantWords', most_freq)  