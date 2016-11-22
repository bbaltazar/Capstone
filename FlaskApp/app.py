from flask import Flask, render_template
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


if __name__ == "__main__":
    app.run()
