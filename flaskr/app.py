from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/recommendation')
def recommendation():
    return render_template('recommendation.html')

@app.route('/workflow')
def workflow():
    return render_template('workflow.html')

@app.route('/post', methods = ['POST'])
def post():
    return render_template('post.html')


if __name__ == "__main__":
    app.run()
