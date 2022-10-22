# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, render_template

app = Flask(__name__)


anchor = '<!-- output anchor -->'


@app.route('/')
def my_form():
    return render_template('my-form.html')


@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    response_text = f'<p>{processed_text}</p>'

    return render_template('my-form.html').replace(anchor, response_text)
