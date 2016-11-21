from bodyscraping import BBcom
import json
import numpy as np
import pandas as pd


class BBclean(object):

    def __init__(self):
        self.df = pd.read_csv('../products.csv')
        self.del_cols = []
        self.new_cols = []

    def expand_columns(self):
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
                            column_list.append(data.df[new_col][i][sub_col])
                        except TypeError:
                            column_list.append(None)
                    self.df[sub_col] = column_list
        self.df['rating'] = [self.df.userRating[i]['overallRating'] for i in xrange(self.df.shape[0])]


    def check_useless(self):
        for col in self.df.columns:
            try:
                if len(self.df[col].unique()) ==1:
                    self.del_cols.append(col)
            except TypeError:
                pass

    def del_columns(self):
        self.df.drop(self.del_cols, axis=1, inplace=True)

    '''
    Graphlab
    User Rating by Brand
    sf_1 = gl.SFrame(data.df[['userId', 'brandId', 'rating']])
    model_1_brand = gl.toolkits.recommender.create(sf_1, \
    user_id = 'userId', item_id='brandId', target='rating')
    Final objective value: 1.78124
    Final training RMSE: 0.940268
    '''

    '''
    Graphlab
    User Rating by Product
    sf_2 = gl.SFrame(data.df[['userId', 'productId', 'rating']])
    model_2_product = gl.toolkits.recommender.create(sf_2, \
    user_id = 'userId', item_id='productId', target='rating')
    Final objective value: 1.01031
    Final training RMSE: 0.504773
    '''

    '''
    Graphlab
    User Rating in General
    sf_3 = gl.SFrame(data.df[['userId', '_id', 'rating']])
    model_3_purchase = gl.toolkits.recommender.create(sf_3, \
    user_id = 'userId', item_id='_id', target='rating')
    Final objective value: 2.52944
    Final training RMSE: 0.512273
    '''

if __name__ == '__main__':
    data = BBclean()
    data.expand_columns()
    data.check_useless()
    data.del_columns()
