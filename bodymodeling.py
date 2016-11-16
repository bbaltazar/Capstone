from bodyscraping import BBcom
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class BBmodel(object):

    def __init__(self):
        self.df = pd.read_csv('products.csv')
        self.dup_cols = ['productReviews']
        self.new_cols = []
#works but causes Nonetype error and does not run methods in if __name__
    def add_columns(self):
        self.df.productReviews = \
        self.df.productReviews.apply(lambda x: json.loads(x)[0]) #changes str to dict
        for col in self.df.productReviews[0].keys():
            self.df[col] = [self.df.productReviews[i][col] \
            for i in xrange(self.df.shape[0])]
            self.new_cols.append(col)
        for new_col in self.new_cols:
            if type(self.df[new_col][0]) == dict:
                self.dup_cols.append(new_col)
                for sub_col in self.df[new_col][0].keys():
                    self.df[sub_col] = [self.df[new_col][j][sub_col] \
                    for j in xrange(self.df.shape[0])]
#works when method called in terminal

    def del_columns(self):
        self.df.drop(self.dup_cols, axis=1, inplace=True)
#works but throws TypeError: unhashable type: 'dict', and run manually in term

    def check_useless(self):
        for col in self.df.columns:
            if len(self.df[col].unique()) ==1:
                self.df.drop(col, axis=1, inplace=True)

if __name__ == '__main__':
    model = BBmodel()
    model.add_columns()
    model.del_columns()
    model.check_useless()
