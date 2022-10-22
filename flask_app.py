# A very simple Flask Hello World app for you to get started with...

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return '''<h1>Wordle bot</h1>

    <p>"Make guess (1), use utility (2), or quit (q): "</p>
    <button>(1)</button>(2)<button></button>(q)<button></button>'''
