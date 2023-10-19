#!/usr/bin/python3
"""Flask web application listening on 0.0.0.0, port 5000"""
from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def home():
    """Home page"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """HBNB page"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_is_fun(text):
    """Return C text"""
    text = text.replace('_', ' ')
    return "C {}".format(text)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
