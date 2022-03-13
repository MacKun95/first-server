
from flask import Flask, url_for, abort
from flask import jsonify
from flask import request

app = Flask(__name__)

testListe = []
index_id = 0

users = [{'name': 'Mac', 'user_id': 1},
         {'name': 'Tai', 'user_id': 2},
         {'name': 'Guy', 'user_id': 3},
         {'name': 'Jack', 'user_id': 4}]

todoListen = [{'list_id': 1, 'name': 'Einkauf'},
              {'list_id': 2, 'name': 'Notwendiges'},
              {'list_id': 3, 'name': 'Lager'},
              {'list_id': 4, 'name': 'Bestellung'}]

listenEintraege = [{'id': 1, 'name': 'Kaese', 'description': 'Milch Produkt', 'list_id': 1, 'user_id': 1},
                   {'id': 2, 'name': 'Jogurt', 'description': 'Milch Produkt', 'list_id': 1, 'user_id': 1},
                   {'id': 1, 'name': 'Tastatusr', 'description': 'Mac', 'list_id': 3, 'user_id': 1}]


@app.after_request
def apply_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/list/<int:list_id>', methods=['GET', 'DELETE'])
def list(list_id):
    list_object = None
    for entry in todoListen:
        if entry['list_id'] == list_id:
            list_object = entry
            break
    if not list_object:
        return "Es existiert keine Liste mit dieser ID!"
    if request.method == 'GET':
            return jsonify([i for i in listenEintraege if i['list_id'] == list_id])
    else:
        todoListen.remove(list_object)
        return "Liste wurde geloescht"

@app.route("/list", methods=['POST'])
def add_new_list():
    new_list = request.get_json(force=True)
    print('neue Liste: {}'.format(new_list))
    list_object = None
    for entry in todoListen:
        if entry['list_id'] == new_list['list_id']:
            list_object = entry
            break
    if not list_object:
        todoListen.append(new_list)
        return jsonify(todoListen), 200
    else:
        return "es existiert bereits eine Liste mit dierser ID!"

@app.route('/list/<int:list_id>/entry', methods=['POST'])
def add_new_entry(list_id):
    new_entry = request.get_json(force=True)
    list_object = None
    for entry in todoListen:
        if entry['list_id'] == list_id:
            list_object = entry
            break
    if not list_object:
        return "Es existiert keine Liste mit dieser ID!", 500
    else:
        listenEintraege.append(new_entry)
        return jsonify(new_entry), 200

@app.route('/list/<int:list_id>/entry/<int:entry_id>', methods=['POST', 'DELETE'])
def update_entry(list_id, entry_id):
    list_object = None
    entry_objekt = None
    index = 0
    for entry in todoListen:
        if entry['list_id'] == list_id:
            list_object = entry
            break
    for entry in listenEintraege:
        if entry['id'] == entry_id:
            entry_object = entry
            break
    if not list_object:
        return "Es existiert keine Liste mit dieser ID!", 500
    if request.method == 'POST':
        updatet_entry = request.get_json(force=True)
        for element in listenEintraege:
            if element['id'] == updatet_entry['id']:
                listenEintraege[index] = updatet_entry
                break
        return 'Erfolg', 200
    else:
        listenEintraege.remove(entry_object)
        return 'loesche', 200

@app.route("/users", methods=['GET'])
def get_user():
    return jsonify([i for i in users])


@app.route("/user", methods=['POST'])
def user():
    new_user = request.get_json(force=True)
    users.append(new_user)
    return new_user

@app.route("/user/<int:user_id>", methods=['DELETE'])
def delete_user(user_id):
    user_object = None
    for entry in users:
        if entry['user_id'] == user_id:
            user_object = entry
            break
    if not user_object:
        return "kein User mit dieser ID", 500
    else:
        users.remove(user_object)
        return "User geloescht", 200


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
