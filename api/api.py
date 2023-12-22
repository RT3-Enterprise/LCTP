import flask
import os
import sys

parent_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append("{}/database".format(parent_dir))
# A FAIRE
import db


client = db.client()
print(client)

(RAW,TRAME) = db.get_db(client)

print(RAW,TRAME)

""""
app = flask.Flask(__name__)
app.config["DEBUG"] = True

trame = [
 {'id': 0,
 'title': 'A Fire Upon the Deep',
 'author': 'Vernor Vinge',
 'first_sentence': 'The coldsleep itself was dreamless.',
 'year_published': '1992'},
 {'id': 1,
 'title': 'The Ones Who Walk Away From Omelas',
 'author': 'Ursula K. Le Guin',
 'first_sentence': "With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.",
 'published': '1973'},
 {'id': 2,
 'title': 'Dhalgren',
 'author': 'Samuel R. Delany',
 'first_sentence': 'to wound the autumnal city.',
 'published': '1975'}
]

@app.route('/', methods=['GET'])
def home():
 return '''<h1>API LCTP</h1>
<p>Capture et Analise de trame</p>'''
# A route to return all of the available entries in our catalog.

@app.route('/api/v1/resources/trame/all', methods=['GET'])
def api_all():
 return flask.jsonify(trame)

@app.route('/api/v1/resources/trame', methods=['GET'])
def api_id():
 # Check if an ID was provided as part of the URL.
 # If ID is provided, assign it to a variable.
 # If no ID is provided, display an error in the browser.
    if 'id' in flask.request.args:
        id = int(flask.request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."
 # Create an empty list for our results
    results = []
 # Loop through the data and match results that fit the requested ID.
 # IDs are unique, but other fields might return many results
    for e in trame:
        if e['id'] == id:
            results.append(e)
 # Use the jsonify function from Flask to convert our list of
 # Python dictionaries to the JSON format.
    return flask.jsonify(results)

app.run()"""