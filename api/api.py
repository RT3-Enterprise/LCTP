import flask
from bson.json_util import dumps
import db

client = db.client()

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
 return '''<h1>API LCTP</h1>
<p>Capture et Analise de trame</p>'''
# A route to return all of the available entries in our catalog.

@app.route('/api/v1/resources/packet/all', methods=['GET'])
def api_get_packet():
    raw,trame = db.get_db(client)
    L = [raw,trame]
    return flask.jsonify(L)

@app.route('/api/v1/resources/packet', methods=['GET'])
def api_get_packet_id():
    raw,trame = db.get_db(client)
    if 'id' in flask.request.args:
        id = flask.request.args['id']
    else:
        return "Error: No id field provided. Please specify an id."
    results = []
    for ra in raw:
        if ra['_id'] == id:
            results.append(ra)
    for tr in trame:
        if tr['_id'] == id:
            results.append(tr)
    return flask.jsonify(results)

@app.route('/api/v1/resources/packet', methods=['POST'])
def api_post_packet():
    content = flask.request.json
    packet = db.json_to_packet(content)
    db.insert_packet(client, packet)
    return 'OK'

@app.route('/api/v1/resources/packet', methods=['DELETE'])
def api_delete_packet():
    content = flask.request.json
    packet = db.json_to_packet(content)
    db.delete_packet(client, packet)
    return 'OK'

@app.route('/api/v1/resources/packet', methods=['PUT'])
def api_put_packet():
    content_json = flask.request.json
    content = json.loads(content_json)
    packet = db.json_to_packet(content['json'])
    new_packet = db.json_to_packet(content['json_new'])
    db.change_packet(client, packet, new_packet)
    return 'OK'

@app.route('/api/v1/resources/trame/all', methods=['GET'])
def api_all_trame():
    _,trame = db.get_db(client)
    return flask.jsonify(trame)

@app.route('/api/v1/resources/trame', methods=['GET'])
def api_filter():
    _,trame = db.get_db(client)
    args = flask.request.args
    results = []
    for tr in trame:
        flag = False
        only = True
        for key in args:
            if key in tr:
                if tr[key] == args[key]:
                    flag = True
                else: 
                    only = False
        if 'only' in args:
            results.append(tr) if only else None
        else:
            results.append(tr) if flag else None
                        
    return flask.jsonify(results)

@app.route('/api/v1/resources/raw/all', methods=['GET'])
def api_all_raw():
    raw,_ = db.get_db(client)
    return flask.jsonify(raw)

@app.route('/api/v1/resources/raw', methods=['GET'])
def api_id_raw():
    raw,_ = db.get_db(client)
    if 'id' in flask.request.args:
        id = flask.request.args['id']
    else:
        return "Error: No id field provided. Please specify an id."
    results = []
    for ra in raw:
        if ra['_id'] == id:
            results.append(ra)
    return flask.jsonify(results)

@app.route('/api/v1/resources/baux/all', methods=['GET'])
def api_all_baux():
    baux = db.get_baux(client)
    return flask.jsonify(baux)

@app.route('/api/v1/resources/baux', methods=['GET'])
def api_baux_filter():
    baux = db.get_baux(client)
    args = flask.request.args
    results = []
    for bail in baux:
        flag = False
        only = True
        for key in args:
            if key in ba:
                if ba[key] == args[key]:
                    flag = True
                else: 
                    only = False
        if 'only' in args:
            results.append(ba) if only else None
        else:
            results.append(ba) if flag else None
                        
    return flask.jsonify(results)

def api_post_baux():
    content = flask.request.json
    baux = db.json_to_baux(content)
    db.insert_baux(client, baux)
    return 'OK'

def api_delete_baux():
    content = flask.request.json
    baux = db.json_to_baux(content)
    db.delete_baux(client, baux)
    return 'OK'

def api_put_baux():
    content_json = flask.request.json
    content = json.loads(content_json)
    baux = db.json_to_baux(content['json'])
    new_baux = db.json_to_baux(content['json_new'])
    db.change_baux(client, baux, new_baux)
    return 'OK'

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)