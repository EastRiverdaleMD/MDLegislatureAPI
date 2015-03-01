from flask import Flask, jsonify, make_response, request, render_template
from flask.ext.sqlalchemy import SQLAlchemy

import os
import json

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import Legislator

@app.route('/')
def index():
    return render_template('index.html', data=Legislator.list())

@app.route('/legislator/<email>')
def contact(email):
    data = Legislator.details(email=email)
    if data:
        return render_template('contact.html', data=data)
    else:
        return render_template('404.html'), 404

@app.route('/api/assembly', methods=['GET'])
def get_legislators():
    return jsonify({'legislators':  Legislator.list()})

@app.route('/api/assembly/search', methods=['GET'])
def search_legislators():
    kwargs = {}
    for arg in request.args:
        kwargs[arg] = request.args.get(arg)
    return jsonify({'legislators': Legislator.search(**kwargs)})

@app.route('/api/legislator/<email>', methods=['GET'])
def get_legislator(email):
    return jsonify(Legislator.details(email=email))

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run()
