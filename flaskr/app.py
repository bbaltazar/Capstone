from flask import Flask, render_template, request, redirect
import graphlab as gl
# from graphlab.toolkits.recommender import factorization_recommender
import pandas as pd


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

    if request.form['product'] != "0" and request.form['rating'] != "0":
        product = request.form['product']
        prodnum = df[df.drop_down ==product].values[0][0]
        rating = request.form['rating']
    else:
        product = None
        rating = None


    if request.form['product2'] != "0":
        product2 = request.form['product2']
        prodnum = df[df.drop_down ==product2].values[0][0]
        rating2 = request.form['rating2']
    else:
        product2 = None
        rating2 = None

    if request.form['product3'] != "0":
        product3 = request.form['product3']
        prodnum = df[df.drop_down ==product3].values[0][0]
        rating3 = request.form['rating3']
    else:
        product3 = None
        rating3 = None

    return render_template('result.html', fname=fname, height=height, \
                            height_input=height_input, weight=weight, \
                            weight_input=weight_input, product=product, \
                            product2=product2, product3=product3, \
                            rating = rating, rating2=rating2, rating3=rating3, \
                            prodnum=prodnum, df=df)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)

#after bodyfat in recommendation.html
# <p align='left'>
#     Rate a product:
# </p>
#     <select name="product">
#       {%for brandName in df.brandName.unique()%}
#         <option value={{ brandName }}>{{brandName}}</option> '''add more options if necessary'''
#         {% endfor %}
#     </select>
