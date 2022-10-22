# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, render_template

app = Flask(__name__)


# @app.route('/')
# def hello_world():
#     return '''<h1>Wordle bot</h1>

#     <p>"Make guess (1), use utility (2), or quit (q): "</p>
#     <button>(1)</button><button>(2)</button><button>(q)</button>'''

@app.route('/')
def my_form():
    return render_template('my-form.html')


@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    return processed_text
