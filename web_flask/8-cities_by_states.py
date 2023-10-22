#!/usr/bin/python3
"""Flask web application listening on 0.0.0.0, port 5000"""
from models import storage
from models.state import State
from flask import Flask
from flask import render_template
from os import getenv

app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """Return list of states and their related cities"""
    states = storage.all(State).values()
    return render_template(
            "8-cities_by_states.html",
            states=states)


@app.teardown_appcontext
def teardown(_):
    """Remove the current SQLAlchemy Session after each request"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
