import flask
from flask_pymongo import PyMongo
import sys
import os

parent_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append("{}/database".format(parent_dir))
# A FAIRE
import db

client = db.client()

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
 return '''<h1>API LCTP</h1>
<p>Capture et Analise de trame</p>'''
# A route to return all of the available entries in our catalog.

@app.route('/api/v1/resources/trame/all', methods=['GET'])
def api_all():
    _,trame = db.get_db(client)
    flask.
    return flask.jsonify(trame)

app.run()