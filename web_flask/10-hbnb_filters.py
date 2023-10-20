#!/usr/bin/python3
"""Flask web application listening on 0.0.0.0, port 5000"""
from models import storage
from models.state import State
from models.amenity import Amenity
from flask import Flask
from flask import render_template
from os import getenv

app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def state():
    """Return the state with the id passed as arg and their related cities"""
    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    return render_template(
            "10-hbnb_filters.html",
            states=states,
            amenities=amenities,
            storage_type=getenv("HBNB_TYPE_STORAGE"))


@app.teardown_appcontext
def teardown(_):
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
