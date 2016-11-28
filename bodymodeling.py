import graphlab as gl
# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd
# from nltk.corpus import stopwords
# from nltk.stem.snowball import SnowballStemmer
# from sklearn.feature_extraction.text import TfidfVectorizer
# from string import punctuation

'''
1. Build a recommender system with a web app that contains:
    drop down of up to 3 current products using
    switcher of male/female
    drop down of height in feet, inches with switcher of ft/m
    drop down of weight in pounds with switcher of lb/kg
    toggler of price range, goal, if specific item recommend or stack

2. Output recommended nutrition products

3. To Do:
NMF
TF-IDF
Clustering

'''

class BBmodel(object):

    def __init__(self):
        self.df = pd.read_pickle('reviews.pkl')
        self.n_topics = 10


    def non_food_subset(self):
        '''
        Subset DataFrame to only include food products
        '''
        non_food_stopwords = ['accessories','backpack', 'bag', 'bottle', \
        'blenderbottle', 'tank', 'tee', ' cap', 'hat', 'tights', 'bra', \
        'pant', 'pants', 'plate', 'organizer', 'lock', 'log', 'glove', \
        'gloves', 'container', 'case', 'beanie', 'hoodie', 'weight set', \
        'kettlebell', 'short', 'shorts', 'tan', 'scale', 'cookbook', \
        'fitbook', 'wrap', 'wraps', 'schiek', 'suits', 'sling', 'tan', \
        'strap', 'straps', 'rope', 'wheel', 'station', 'roller', 'belt', \
        'belts', 'pad', 'headphone', 'headphones', 'grip', 'measure kit', \
        'tracker', 'cuff', 'mat', 'harness', 'rashguard', 'chalk', 't-shirt', \
        'massage', 'tools', 'shaker', 'shakers', 'shoe', 'shoes', 'ray', \
        'bodyfit', 'funnel', 'sportmixer', 'trunk', 'bands', 'headband', \
        'superband', 'knee', 'pull-up', 'attachment', 'loop', 'yoga', 'waist'\
        'denim', 'towel', 'powerblock', 'gripz', 'clothing', 'journals', \
        'body-solid', 'gymboss', 'prohands', 'rocktape', 'plastics', 'jbl', \
        'omron', 'coat', 'ball', 'wrist', 'exerciser']
        non_food_desc = []
        for name in self.df.name.unique():
            for stopword in non_food_stopwords:
                if stopword in name.lower().split():
                    non_food_desc.append(name)
        non_food_desc = list(set(non_food_desc))
        self.df = self.df[[name not in non_food_desc for name in self.df.name]]



    def graphlab_rec(self):
        pass

    def myvectorizer(self):
        '''
        feature extraction with corpus being all products' reviews and each doc
        being each particular product's reviews.
        '''
        corpus = []
        stemmer = SnowballStemmer('english')
        for prodId in self.df.productId.unique():
            docs = []
            for doc in self.df[self.df.productId == prodId].text:
                if doc:
                    doc = ' '.join(stemmer.stem(word.strip(punctuation).lower()) \
                                                    for word in doc.split())
                    docs.append(doc)
            corpus.append(' '.join(docs))
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf = self.tfidf_vectorizer.fit_transform(corpus)
        self.nmf = NMF(n_components = self.n_topics).fit(self.tfidf)
        n_topic_words = self.n_topics
        for topic_idx, topic in enumerate(self.nmf.components_):
            print 'Topic #{}:' .format(topic_idx)
            print ' '.join([self.tfidf_vectorizer.get_feature_names()[i] for i \
                                in topic.argsort()[:-n_topic_words -1:-1]])
            print()

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


if __name__ == '__main__':
    data = BBmodel()
    data.myvectorizer()
