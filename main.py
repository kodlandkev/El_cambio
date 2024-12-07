from flask import Flask, render_template, request
from res import get_class

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result')
def result():
    
app.run(debug=True)
