import flask
from bson.json_util import dumps
import db

client = db.client()

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET']) # route de la page d'accueil
def home(): # fonction de la page d'accueil
 return '''<h1>API LCTP</h1>
<p>Capture et Analise de trame</p>'''

@app.route('/api/v1/resources/packet/all', methods=['GET']) # route pour récupérer tous les packets
def api_get_packet():   # fonction pour récupérer tous les packets
    raw,trame = db.get_db(client)
    L = [raw,trame]
    return flask.jsonify(L)

@app.route('/api/v1/resources/packet/last', methods=['GET']) # route pour récupérer tous les packets
def api_get_last_packet(): # fonction pour récupérer le dernier packet
    _,trame = db.get_db(client) # on récupère les packets
    return flask.jsonify(trame[-1]) if len(trame) > 0 else flask.jsonify([])

@app.route('/api/v1/resources/packet/first', methods=['GET']) # route pour récupérer tous les packets
def api_get_first_packet():
    _,trame = db.get_db(client)
    return flask.jsonify(trame[0]) if len(trame) > 0 else flask.jsonify([])

@app.route('/api/v1/resources/packet', methods=['GET']) # route pour récupérer un packet en fonction de son id
def api_get_packet_id(): # fonction pour récupérer un packet
    raw,trame = db.get_db(client) # on récupère les packets
    if 'id' in flask.request.args: # Vérification de id dans les arguments
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

@app.route('/api/v1/resources/packet', methods=['POST']) # route pour poster un packet
def api_post_packet(): # fonction pour poster un packet
    content = flask.request.json # on récupère le contenu de la requête
    packet = db.json_to_packet(content) # on transforme le contenu en packet
    db.insert_packet(client, packet) # on insère le packet dans la base de donnée
    return 'OK'

@app.route('/api/v1/resources/packet', methods=['DELETE']) # route pour supprimer un packet
def api_delete_packet(): # fonction pour supprimer un packet
    content = flask.request.json # on récupère le contenu de la requête
    packet = db.json_to_packet(content) # on transforme le contenu en packet
    db.delete_packet(client, packet)    # on supprime le packet dans la base de donnée
    return 'OK'

@app.route('/api/v1/resources/packet', methods=['PUT']) # route pour modifier un packet
def api_put_packet(): # fonction pour modifier un packet
    content_json = flask.request.json # on récupère le contenu de la requête
    content = json.loads(content_json) # on transforme le contenu en json
    packet = db.json_to_packet(content['json']) # on transforme le json en packet
    new_packet = db.json_to_packet(content['json_new']) # on transforme le json en packet
    db.change_packet(client, packet, new_packet) # on modifie le packet dans la base de donnée
    return 'OK'

@app.route('/api/v1/resources/trame/all', methods=['GET']) # route pour récupérer toutes les trames
def api_all_trame(): # fonction pour récupérer toutes les trames
    _,trame = db.get_db(client) # on récupère les trames
    return flask.jsonify(trame) # on retourne les trames

@app.route('/api/v1/resources/trame/last', methods=['GET']) # route pour récupérer toutes les trames
def api_last_trame():
    _,trame = db.get_db(client)
    return flask.jsonify(trame[-1])

@app.route('/api/v1/resources/trame/first', methods=['GET']) # route pour récupérer tous les packets
def api_first_trame():
    _,trame = db.get_db(client)
    return flask.jsonify(trame[0])

@app.route('/api/v1/resources/trame', methods=['GET']) # route pour récupérer une trame en fonction de son id
def api_filter(): # fonction pour récupérer une trame
    _,trame = db.get_db(client) # on récupère les trames
    args = flask.request.args # on récupère les arguments de la requête
    results = []
    for tr in trame: # on parcours les trames
        flag = False
        only = True
        for key in args: # on parcours les arguments
            if key in tr: # on vérifie si l'argument est dans la trame
                if tr[key] == args[key]: # on vérifie si la valeur de l'argument est égale à la valeur de la trame
                    flag = True
                else: 
                    only = False 
        if 'only' in args:
            results.append(tr) if only else None # on ajoute la trame si only est vrai sinon on ajoute rien
        else:
            results.append(tr) if flag else None # on ajoute la trame si flag est vrai sinon on ajoute rien
                        
    return flask.jsonify(results) # on retourne les trames

@app.route('/api/v1/resources/raw/all', methods=['GET']) # route pour récupérer tous les raw
def api_all_raw(): # fonction pour récupérer tous les raw
    raw,_ = db.get_db(client) # on récupère les raw
    return flask.jsonify(raw) # on retourne les raw

@app.route('/api/v1/resources/raw', methods=['GET']) # route pour récupérer un raw en fonction de son id
def api_id_raw(): # fonction pour récupérer un raw
    raw,_ = db.get_db(client) # on récupère les raw
    if 'id' in flask.request.args: # on vérifie si id est dans les arguments
        id = flask.request.args['id']
    else:
        return "Error: No id field provided. Please specify an id."
    results = []
    for ra in raw:
        if ra['_id'] == id:
            results.append(ra)
    return flask.jsonify(results) # on retourne les raw

@app.route('/api/v1/resources/baux/all', methods=['GET']) # route pour récupérer tous les baux
def api_all_baux(): # fonction pour récupérer tous les baux
    baux = db.get_baux(client) # on récupère les baux
    return flask.jsonify(baux) # on retourne les baux

@app.route('/api/v1/resources/baux', methods=['GET']) # route pour récupérer un baux en fonction de son id
def api_baux_filter(): # fonction pour récupérer un baux
    baux = db.get_baux(client) # on récupère les baux
    args = flask.request.args # on récupère les arguments de la requête
    results = []
    for bail in baux: # on parcours les baux
        flag = False
        only = True
        for key in args: # on parcours les arguments
            if key in ba: # on vérifie si l'argument est dans le baux
                if ba[key] == args[key]: # on vérifie si la valeur de l'argument est égale à la valeur du baux
                    flag = True
                else: 
                    only = False
        if 'only' in args:
            results.append(ba) if only else None # on ajoute le baux si only est vrai sinon on ajoute rien
        else:
            results.append(ba) if flag else None # on ajoute le baux si flag est vrai sinon on ajoute rien
                        
    return flask.jsonify(results) # on retourne les baux

def api_post_baux(): # fonction pour poster un baux
    content = flask.request.json # on récupère le contenu de la requête
    baux = db.json_to_baux(content) # on transforme le contenu en baux
    db.insert_baux(client, baux) # on insère le baux dans la base de donnée
    return 'OK'

def api_delete_baux(): # fonction pour supprimer un baux
    content = flask.request.json # on récupère le contenu de la requête
    baux = db.json_to_baux(content) # on transforme le contenu en baux
    db.delete_baux(client, baux) # on supprime le baux dans la base de donnée
    return 'OK'

def api_put_baux():
    content_json = flask.request.json # on récupère le contenu de la requête
    content = json.loads(content_json) # on transforme le contenu en json 
    baux = db.json_to_baux(content['json']) # on transforme le json en baux
    new_baux = db.json_to_baux(content['json_new']) # on transforme le json en baux
    db.change_baux(client, baux, new_baux) # on modifie le baux dans la base de donnée
    return 'OK'

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)