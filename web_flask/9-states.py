#!/usr/bin/python3
"""Flask web application listening on 0.0.0.0, port 5000"""
from models import storage
from models.state import State
from flask import Flask
from flask import render_template
from os import getenv

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def states():
    """Return list of states"""
    states = storage.all(State).values()
    return render_template("7-states_list.html", states=states)


@app.route('/states/<id>', strict_slashes=False)
def state_id(id):
    """Return the state with the id passed as arg and their related cities"""
    states = storage.all(State).values()
    if id in states:
        for state in states:
            if state.id == id:
                return render_template(
                        "9-states.html",
                        state=state,
                        storage_type=getenv("HBNB_TYPE_STORAGE"))
    else:
        return render_template("9-states.html")


@app.teardown_appcontext
def teardown(_):
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
