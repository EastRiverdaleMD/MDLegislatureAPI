from flask import Flask, jsonify, make_response, request
from flask.ext.sqlalchemy import SQLAlchemy

import os
import json

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import Legislator

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/api/legislators', methods=['GET'])
def get_legislators():
    data = Legislator.query.all()
    data = [person.display() for person in data]
    return jsonify({'legislators': data})

@app.route('/api/legislators/search', methods=['GET'])
def search_legislators():
    kwargs = {}
    for arg in request.args:
        kwargs[arg] = request.args.get(arg)
    data = Legislator.query.filter_by(**kwargs)
    data = [person.display() for person in data]
    return jsonify({'legislators': data})

@app.route('/api/legislator/<email>', methods=['GET'])
def get_legislator(email):
    person = Legislator.query.filter_by(email=email).first()
    return jsonify(person.display_details())


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run()
