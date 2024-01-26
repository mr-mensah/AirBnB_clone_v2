#!/usr/bin/python3
"""lists of the states"""
from models import storage
from flask import Flask, render_template
from models.state import State


app = Flask(__name__)


@app.teardown_appcontext
def remove_session(session):
    """closes session after every request"""
    storage.close()


@app.route("/cities_by_states", strict_slashes=False)
def states_list():
    """states router"""
    states = storage.all(State)
    sortedd = sorted(states.values(), key=lambda item: item.name)
    return render_template('8-cities_by_states.html', sorted_states=sortedd)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
