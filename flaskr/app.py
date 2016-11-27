from flask import Flask, render_template, request, redirect
import jinja2

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/recommendation')#, methods=['GET', 'POST'])
def recommendation():
    return render_template('recommendation.html')

@app.route('/workflow')
def workflow():
    return render_template('workflow.html')

@app.route('/result', methods = ['POST'])
def result():
    name = request.form['name']
    fname = name.split()[0]
    return render_template('result.html', fname=fname)


if __name__ == "__main__":
    app.run()
