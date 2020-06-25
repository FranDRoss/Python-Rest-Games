from flask import Flask, request
from flask_restful import Resource
from sqlalchemy import create_engine
from json import dumps
import json
from flask_jsonpify import jsonify

app = Flask(__name__)

with open('static/games.json') as json_file:
    db = json.load(json_file)

@app.route('/', methods=['GET']) 
def welcome():
    return app.send_static_file('index.html')

@app.route('/games', methods=['GET']) 
def getGames():
    return jsonify(db)

@app.route('/games/<id>', methods=['GET']) 
def getGame(id):
    id = int(id)
    length = len(db)
    data = ""

    if length <= id: 
        data = jsonify("No game with that id")
    elif length > id:
        data = jsonify(db[id])

    return data
    
@app.route('/games', methods=['POST']) 
def postGame():
    db.append(request.get_json())
    with open('static/games.json', "w") as json_file:
        json.dump(db, json_file)
    return jsonify(db)

@app.route('/games/<id>', methods=['PUT']) 
def updateGame(id):
    id = int(id)
    length = len(db)
    data = ""
    update = request.get_json()

    if length <= id: 
        data = jsonify("No game with that id")
    elif length > id:
        db[id] = update
        with open('static/games.json', "w") as json_file:
            json.dump(db, json_file)
        data = jsonify(db[id])
    return data



if __name__ == '__main__':
     app.run(port='5000')