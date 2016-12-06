from flask import Flask, render_template, request, redirect
from graphlab.toolkits.recommender import factorization_recommender, popularity_recommender
import graphlab as gl
import pandas as pd
import random

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/recommendation')
def recommendation():
    df = pd.read_pickle('rateaproduct.pkl')
    return render_template('recommendation.html', df=df)

@app.route('/workflow')
def workflow():
    return render_template('workflow.html')

@app.route('/result', methods = ['POST'])
def result():
    df = pd.read_pickle('rateaproduct.pkl')
    name = request.form['name']
    user = random.randint(1,1000000000)
    fname = name.split()[0]

    height_input = request.form['height']
    if request.form['height_toggle'] == "cm":
        height = round(float(height_input)/2.54, 2)
    else:
        height = round(float(height_input), 2)

    weight_input = request.form['weight']
    if request.form['weight_toggle'] == "kg":
        weight = round(float(weight_input)*2.205, 2)
    else:
        weight = round(float(weight_input), 2)

    form_input = {'userId':[], \
               'productId':[], \
                  'rating':[], \
                'username':[], \
                  'height':[], \
                  'weight':[], \
                 'bodyfat':[]}

    df2 = pd.read_pickle('nutrition.pkl')
    bodyfat = df2[df2.bodyfat > 0].bodyfat.mean()
    if request.form['bodyfat']:
        bodyfat = int(request.form['bodyfat'])

    if request.form['product'] != "0" and request.form['rating'] != "0":
        form_input['userId'].append(user)
        product = request.form['product']
        prodnum = df[df.drop_down ==product].values[0][0]
        form_input['productId'].append(prodnum)
        rating = request.form['rating']
        form_input['rating'].append(int(rating))
        form_input['username'].append(name)
        form_input['height'].append(float(height))
        form_input['weight'].append(float(weight))
        form_input['bodyfat'].append(bodyfat)


    if request.form['product2'] != "0" and request.form['rating2'] != "0":
        form_input['userId'].append(user)
        product2 = request.form['product2']
        prodnum2 = df[df.drop_down ==product2].values[0][0]
        form_input['productId'].append(prodnum2)
        rating2 = request.form['rating2']
        form_input['rating'].append(int(rating2))
        form_input['username'].append(name)
        form_input['height'].append(float(height))
        form_input['weight'].append(float(weight))
        form_input['bodyfat'].append(bodyfat)

    if request.form['product3'] != "0" and request.form['rating3'] != "0":
        form_input['userId'].append(user)
        product3 = request.form['product3']
        prodnum3 = df[df.drop_down ==product3].values[0][0]
        form_input['productId'].append(prodnum3)
        rating3 = request.form['rating3']
        form_input['rating'].append(int(rating3))
        form_input['username'].append(name)
        form_input['height'].append(float(height))
        form_input['weight'].append(float(weight))
        form_input['bodyfat'].append(bodyfat)

    if request.form['product4'] != "0" and request.form['rating4'] != "0":
        form_input['userId'].append(user)
        product4 = request.form['product4']
        prodnum4 = df[df.drop_down ==product4].values[0][0]
        form_input['productId'].append(prodnum4)
        rating4 = request.form['rating4']
        form_input['rating'].append(int(rating4))
        form_input['username'].append(name)
        form_input['height'].append(float(height))
        form_input['weight'].append(float(weight))
        form_input['bodyfat'].append(bodyfat)

    if request.form['product5'] != "0" and request.form['rating5'] != "0":
        form_input['userId'].append(user)
        product5 = request.form['product5']
        prodnum5 = df[df.drop_down ==product5].values[0][0]
        form_input['productId'].append(prodnum5)
        rating5 = request.form['rating5']
        form_input['rating'].append(int(rating5))
        form_input['username'].append(name)
        form_input['height'].append(float(height))
        form_input['weight'].append(float(weight))
        form_input['bodyfat'].append(bodyfat)


    sf = gl.SFrame(df2[['userId', 'productId', 'rating']])
    user_info = gl.SFrame(df2[['userId', 'height', 'weight', 'bodyfat']])
    item_info = gl.SFrame(df2[['brandName', 'name', 'brandId', 'productId', 'description']])
    user_info = user_info.fillna('weight', df2[df2.weight > 0].weight.mean())
    user_info = user_info.fillna('height', df2[df2.height > 0].height.mean())
    user_info = user_info.fillna('bodyfat', df2[df2.bodyfat > 0].bodyfat.mean())

    if request.form['product'] != "0" and request.form['rating'] != "0":
        m = factorization_recommender.create(sf, user_id='userId', num_factors=13,\
                                    item_id='productId', target='rating',\
                                        user_data=user_info, item_data=item_info)
    else:
        m = popularity_recommender.create(sf, user_id='userId', \
                                item_id='productId', target='rating',\
                                        user_data=user_info, item_data=item_info)

    recent_data = gl.SFrame(form_input)
    recs = m.recommend(users=[user], new_observation_data=recent_data)
    top = []
    for prod in recs['productId']:
        top.append(df[df.productId == prod].values[0][1])


    return render_template('result.html', fname=fname, height=height, \
                            height_input=height_input, weight=weight, \
                            weight_input=weight_input,  \
                            bodyfat=bodyfat,\
                            recs=recs, top=top)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
