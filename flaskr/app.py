from flask import Flask, render_template, request, redirect
from graphlab.toolkits.recommender import factorization_recommender
import pandas as pd

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/recommendation')
def recommendation():
    # df = pd.read_pickle('../nutrition.pkl')
    return render_template('recommendation.html')

@app.route('/workflow')
def workflow():
    columns = df.columns
    return render_template('workflow.html', columns=columns)

@app.route('/result', methods = ['POST'])
def result():
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
    return render_template('result.html', fname=fname, height=height, \
                            height_input=height_input, weight=weight, \
                            weight_input=weight_input)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
    df = pd.read_pickle('../nutrition.pkl')
#after bodyfat in recommendation.html
# <p align='left'>
#     Rate a product:
# </p>
#     <select name="product">
#       {%for brandName in df.brandName.unique()%}
#         <option value={{ brandName }}>{{brandName}}</option> '''add more options if necessary'''
#         {% endfor %}
#     </select>
