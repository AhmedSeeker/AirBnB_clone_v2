#!/usr/bin/python3
"""Flask web application listening on 0.0.0.0, port 5000"""
from models import storage
from models.state import State
from models.amenity import Amenity
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """Return list of states with related cities and a list of amenities"""
    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    return render_template(
            "10-hbnb_filters.html", states=states, amenities=amenities)


@app.teardown_appcontext
def teardown(_):
    """Remove the current SQLAlchemy Session after each request"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
