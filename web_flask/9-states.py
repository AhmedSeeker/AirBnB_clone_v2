#!/usr/bin/python3
"""Flask web application listening on 0.0.0.0, port 5000"""
from models import storage
from models.state import State
from flask import Flask
from flask import render_template
from os import getenv

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states(id=None):
    """Return the state with the id passed as arg and their related cities"""
    states = storage.all(State).values()
    if id:
        for state in states:
            if state.id == id:
                return render_template("9-states.html", state=state, id=id)
        return render_template("9-states.html", state=None, id=id)
    else:
        return render_template("9-states.html", states=states)


@app.teardown_appcontext
def teardown(_):
    """Remove the current SQLAlchemy Session after each request"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
