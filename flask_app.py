# A very simple Flask Hello World app for you to get started with...

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return '<h1>Hello from Flask! -- Wordle bot</h1><button>test button</button>'
