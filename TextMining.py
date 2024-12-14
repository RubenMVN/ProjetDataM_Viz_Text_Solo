from unidecode import unidecode
from nltk.stem import SnowballStemmer



document = []
with open("/ProjetDataM_Viz_Text_Solo/corpus.txt","r") as f:
    document.append(f.read())
document = document[0]

from FonctionMining import stopWords
stopWords = [unidecode(sw) for sw in stopWords]

stemmer = SnowballStemmer('french')


from FonctionMining import *
Texte = stem_cleaner(document,stemmer,stopWords)






