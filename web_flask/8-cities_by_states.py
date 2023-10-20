#!/usr/bin/python3
"""Flask web application listening on 0.0.0.0, port 5000"""
from models import storage
from models.state import State
from flask import Flask
from flask import render_template
from os import getenv

app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def states():
    """Return list of states"""
    states = storage.all(State).values()
    return render_template("8-cities_by_states.html", states=states,
            storage_type=getenv("HBNB_TYPE_STORAGE"))


@app.teardown_appcontext
def teardown(_):
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
