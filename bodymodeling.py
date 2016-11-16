from bodyscraping import BBcom
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class BBmodel(object):

    def __init__(self):
        self.df = None

    def load_data(self):
        self.df = pd.read_csv('products.csv')

    def add_columns(self):
        for col in p.productReviews[0].keys():
            p[col] = [p.productReviews[i][col] for i in xrange(p.shape[0])]

    def clean_data(self):
        self.df.productReviews = \
        self.df.productReviews.apply(lambda x: json.loads(x)[0]) #changes str to dict


if __name__ == '__main__':
    model = BBmodel()
    model.load_data()
