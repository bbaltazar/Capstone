from pymongo import MongoClient
from IPython.core.display import HTML
from bs4 import BeautifulSoup
import pandas as pd
import StringIO
import requests

class BBcom(object):

    def __init__(self, client):
        self.client = client
        self.load_data()
        self.brand_urls = None
        self.brand_num_list = []

    def load_data(self):
        self.db = self.client['bodyscrape']
        self.coll = self.db['products']

    def brand_list(self):
        z = requests.get('http://reviews.bodybuilding.com/view-reviews')
        soup = BeautifulSoup(z.content, 'html.parser')
        self.brand_urls = [soup.findAll(id='brandName')[i]['href'] for i in
        xrange(len(soup.findAll(id='brandName')))]
        #return self.brand_urls

    def brand_numbers(self):
        for url in self.brand_urls:
            z = requests.get(url)
            soup = BeautifulSoup(z.content, 'html.parser')
            tags = soup.findAll(attrs={'class':'product-image'})
            for i in xrange(0, len(tags), 2):
                product_num = \
                tags[i].find('img')['src'].split('image/prod_')[1].split('/')[0]
                self.brand_num_list.append(product_num)

    def insert_product(self):
        '''
        Inserts JSON dictionary entries into db.products collection
        '''
        params = {\
             'page':0,
          'reviewType':'verified',
          'size':'1'} # foo.json()['totalItems'] gives total size but cannot call until foo.json initiated
        headers = {\
                   'Accept':'application/json',
        'Accept-Encoding':'gzip, deflate, sdch, br',
        'Accept-Language':'en-US,en;q=0.8',
        'BB-App':'product-detail-app, 5.1.3',
        'Connection':'keep-alive',
        'Host':'catalog.bodybuilding.com',
        'Origin':'http://www.bodybuilding.com',
        'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36}'
                  }
        for num in self.brand_num_list:
            url = 'https://catalog.bodybuilding.com/products/'+str(num)+'/reviews'
            r = requests.get(url, headers=headers, params=params)
            if r.json()['productReviews']:
                for i in xrange(r.json()['totalItems']):
                    params = {\
                            'page':i,
                      'reviewType':'verified',
                            'size':'1'}
                    z = requests.get(url, headers=headers, params=params)
                    z_json = z.json()
                    self.coll.insert_one(z_json)


if __name__ == '__main__':

    client = MongoClient()
    script = BBcom(client)
    script.brand_list()
    script.brand_numbers()
    # script.insert_product()
    client.close()
'''
In terminal: export MongoDB collection to CSV excluding '<>':
<mongoexport --db bodyscrape --collection products --type csv --out products.csv\
 --fields 'totalItems','productReviews'>
'''
