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

    def parse_food_prods(self):
        non_food_stopwords = ['backpack', 'bag', 'bottle', 'tank', 'tee', \
        ' cap', 'hat', 'tights', 'bra', 'pant', 'pants', 'plate', 'organizer', \
        'lock', 'log', 'glove', 'gloves', 'container', 'case', 'beanie', \
        'hoodie', 'weight set', 'kettlebell', 'short', 'shorts', 'tan', \
        'scale', 'cookbook', 'fitbook', 'wrap', 'wraps', 'denim', 'towel', \
        'strap', 'straps', 'rope', 'wheel', 'station', 'roller', 'belt', \
        'belts', 'pad', 'headphone', 'grip', 'measure kit', 'ball', 'wrist', \
        'tracker', 'cuff', 'mat', 'harness', 'rashguard', 'chalk', 't-shirt', \
        'massage', 'tools', 'shaker', 'shakers', 'shoe', 'shoes', 'ray', \
        'bodyfit', 'funnel', 'sportmixer', 'trunk', 'bands', 'headband', \
        'superband', 'knee', 'pull-up', 'attachment', 'loop', 'yoga', 'waist']
        non_food_desc = []
        for name in self.df.name.unique():
            for stopword in non_food_stopwords:
                if stopword in name.lower().split():
                    non_food_desc.append(name)
        non_food_desc = list(set(non_food_desc))
        self.df = self.df[[name not in non_food_desc for name in df.name]]

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

    '''
    https://turi.com/learn/userguide/recommender/choosing-a-model.html
    Side information for users, items, and observations
In many cases, additional information about the users or items can
improve the quality of the recommendations. For example, including information
about the genre and year of a movie can be useful information in recommending
movies. We call this type of information user side data or item side data
depending on whether it goes with the user or the item.
Including side data is easy with the user_data or item_data parameters to
the recommender.create() function. These arguments are SFrames and must have
a user or item column that corresponds to the user_id and item_id columns in
the observation data. Internally, the data is joined to the particular user
or item when training the model, the data is saved with the model and also used
to make recommendations.
In particular, the FactorizationRecommender and the
RankingFactorizationRecommender both incorporate the side data into the
prediction through additional interaction terms between the user, the item,
and the side feature. For the actual formula, see the API docs for the
FactorizationRecommender. Both of these models also allow you to obtain the
parameters that have been learned for each of the side features via the
m['coefficients'] argument.
    '''

if __name__ == '__main__':
    data = BBclean()
    data.expand_columns()
    data.parse_food_prods()
    data.check_useless()
    data.del_columns()
