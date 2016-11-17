import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from string import punctuation

'''
1. Build a recommender system with a web app that contains:
    drop down of up to 3 current products using
    switcher of male/female
    drop down of height in feet, inches with switcher of ft/m
    drop down of weight in pounds with switcher of lb/kg
    toggler of price range, goal, if specific item recommend or stack

2. Output recommended nutrition products

3. To Do:
Learn selenium
NMF
TF-IDF
Clustering

'''

class BBmodel(object):

    def __init__(self):

    def my_tokenizer(self, x):
        stop = set(stopwords.words('english'))
        tokens = BeautifulSoup(x, 'html.parser').getText().lower().split()
        tokens = [token.strip(punctuation) for token in tokens if token not in stop]
        stemmer = SnowballStemmer("english")
        tokens = [stemmer.stem(token) for token in tokens if token]
        return ' '.join(tokens)

#https://github.com/zipfian/DSI_Lectures/blob/master/recommendation-systems/giovanna_thron/notes.md

    '''
    distance metric want to use is pearson correlation because it helps measure
    similarity of two users without sensitivity to a user who consistently rates
    low or high. For example, say user 1 rates three items: 5, 5, 3 and user 2
    rates three items: 3, 3, 1. The similarity of these two users will be 1
    (totally similar).
    '''

    '''
    Jaccard Similarity may be of interest: is a measure of the similarity of
    two sets. In this case, we would like to measure if two items have been
    rated by the same users. The Jaccard Similarity is useful when we don't
    have ratings, just a boolean value. For example, whether or not the user
    watched the movie, bought the product, etc.
    '''
