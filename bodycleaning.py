from bodyscraping import BBcom
import json
import numpy as np
import pandas as pd


class BBclean(object):

    def __init__(self):
        self.df = pd.read_csv('products.csv')
        self.del_cols = []
        self.new_cols = []

    def add_columns(self):
        self.df.productReviews = \
        self.df.productReviews.apply(lambda x: json.loads(x)[0]) #changes str to dict
        for col in self.df.productReviews[0].keys():
            self.df[col] = [self.df.productReviews[i][col] \
            for i in xrange(self.df.shape[0])]
            self.new_cols.append(col)
        self.del_cols.append('productReviews')
        for new_col in self.new_cols:
            if type(self.df[new_col][0]) == dict:
                self.del_cols.append(new_col)
                for sub_col in self.df[new_col][0].keys():
                    column_list = []
                    for i in xrange(self.df.shape[0]):
                        try:
                            column_list.append(model.df[new_col][i][sub_col])
                        except TypeError:
                            column_list.append(None)
                    self.df[sub_col] = column_list

    def check_useless(self):
        for col in self.df.columns:
            try:
                if len(self.df[col].unique()) ==1:
                    self.del_cols.append(col)
            except TypeError:
                pass

    def del_columns(self):
        self.df.drop(self.del_cols, axis=1, inplace=True)

if __name__ == '__main__':
    model = BBclean()
    # model.add_columns()
    # model.check_useless()
    # model.del_columns()
