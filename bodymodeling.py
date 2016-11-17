import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from string import punctuation


class BBmodel(object):

    def __init__(self):

    def my_tokenizer(self,x):
       stop = set(stopwords.words('english'))
       tokens = BeautifulSoup(x, 'html.parser').getText().lower().split()
       tokens = [token.strip(punctuation) for token in tokens if token not in stop]
       stemmer = SnowballStemmer("english")
       tokens = [stemmer.stem(token) for token in tokens if token]
       return ' '.join(tokens)
