from unittest import result

import pymongo as pymongo
from flask import Flask, jsonify, abort, make_response, request
app = Flask(__name__)
import random
from bson import json_util, ObjectId


# Create connection
conex = pymongo.MongoClient(host=['localhost:27017'])


db = conex.Artesanos

artesanos_collection = db.artesanos
obras_collection = db.obras



'''
643dcc80677ee55519d0c25e
36760512
{
  "artesano": {
    "nombre_completo": "Sebastian González",
    "email": "Sebastian.gonzalez@email.com",
    "telefono": "555-9876",
    "direccion": "Calle Secundaria 456, San José",
    "categorias": ["pintura", "escultura"]
  }
}
{
    "artesano": {    
        "nombre_completo": "Dorian Uma",
        "email": "Dorian.Uma@email.com",
        "telefono": "999-9876",
        "direccion": "Calle santa fe 456, San jose",
        "categorias": [
            "pintura"
        ]
    }
}

artesano = [
    {
    "id": 1,
    "nombre_completo": "Juan Pérez",
    "email": "juan.perez@email.com",
    "telefono": "555-1234",
    "direccion": "Calle Principal 123, Puntarenas",
    "categorias": ["cerámica", "tejidos"]
},
    {
    "id": 2,
    "nombre_completo": "Sebastian SoloYi",
    "email": "Sebastian.Yi@email.com",
    "telefono": "8977-8790",
    "direccion": "Invu Frente al marco 123, Donde huela a Yi",
    "categorias": ["Mariguano", "Administrador en gerencia"]
}

] '''


def generate_id():
    return str(random.randint(10000000, 99999999))

def generate_idOb():
    return str(random.randint(10000000, 99999999))


@app.route('/artesano/<string:art_id>', methods=['GET'])
def get_artesano(art_id):
    art = artesanos_collection.find_one({'custom_id': art_id})
    if art is None:
        abort(404)
    return json_util.dumps({'artesano': art})


@app.route('/artesano', methods=['GET'])
def get_artesanos():
    arts = list(artesanos_collection.find())
    return json_util.dumps({'artesano': arts})



@app.route('/artesano', methods=['POST'])
def create_artesano():
    if not request.json or not 'artesano' in request.json or not 'nombre_completo' in request.json['artesano']:
        abort(400)

    art_data = request.json['artesano']
    token = generate_id()

    art = {
        '_id': ObjectId(),
        'custom_id': art_data['custom_id'],
        'nombre_completo': art_data['nombre_completo'],
        'email': art_data['email'],
        'telefono': art_data['telefono'],
        'direccion': art_data['direccion'],
        'categorias': art_data['categorias']
    }

    artesanos_collection.insert_one(art)

    return json_util.dumps({'artesano': art}), 201



@app.route('/artesano/<string:art_id>', methods=['PUT'])
def update_artesano(art_id):
    art = artesanos_collection.find_one({'custom_id': art_id})
    if art is None:
        abort(404)
    if not request.json:
        abort(400)
    if 'nombre_completo' in request.json and request.json['nombre_completo'] == '':
        abort(400)
    if 'email' in request.json and request.json['email'] == '':
        abort(400)
    if 'telefono' in request.json and request.json['telefono'] == '':
        abort(400)
    if 'direccion' in request.json and request.json['direccion'] == '':
        abort(400)
    if 'categorias' in request.json and request.json['categorias'] == '':
        abort(400)

    updated_art = {
        'nombre_completo': request.json.get('nombre_completo', art['nombre_completo']),
        'email': request.json.get('email', art['email']),
        'telefono': request.json.get('telefono', art['telefono']),
        'direccion': request.json.get('direccion', art['direccion']),
        'categorias': request.json.get('categorias', art['categorias'])
    }

    result = artesanos_collection.update_one({'custom_id': art_id}, {'$set': updated_art})
    art = artesanos_collection.find_one({'custom_id': art_id})

    return json_util.dumps({'artesano': art}), 200


@app.route('/artesano/<string:art_id>', methods=['DELETE'])
def delete_artesano(art_id):
    art = artesanos_collection.find_one({'custom_id': art_id})
    if art is None:
        abort(404)

    obras_collection.delete_many({'artesano_id': art_id})
    artesanos_collection.delete_one({'custom_id': art_id})

    return jsonify({'result': True})


@app.route('/artesano/<string:art_id>/obra', methods=['POST'])
def create_obra(art_id):
    art = artesanos_collection.find_one({'custom_id': art_id})
    if art is None:
        abort(404)

    if not request.json or not 'obra' in request.json or not 'titulo' in request.json['obra']:
        abort(400)

    obra_data = request.json['obra']
    token = generate_id()
    obra = {
        '_id': ObjectId(),
        'obra_id': token,
        'artesano_id': art_id,
        'titulo': obra_data['titulo'],
        'descripcion': obra_data.get('descripcion', ''),
        'categoria': obra_data.get('categoria', ''),
        'url_imagen': obra_data.get('url_imagen', '')
    }

    obras_collection.insert_one(obra)
    return json_util.dumps({'obra': obra}), 201

@app.route('/obra/<string:obra_id>', methods=['GET'])
def get_obra(obra_id):
    obra = obras_collection.find_one({'obra_id': obra_id})
    if obra is None:
        abort(404)
    return json_util.dumps({'obra': obra})


@app.route('/obra', methods=['GET'])
def get_obras():
    obra = list(obras_collection.find())
    return json_util.dumps({'obra': obra})


@app.route('/obra/<string:obra_id>', methods=['PUT'])
def update_obra(obra_id):
    obra = obras_collection.find_one({'obra_id': obra_id})
    if obra is None:
        abort(404)
    if not request.json:
        abort(400)
    if 'titulo' in request.json and request.json['titulo'] == '':
        abort(400)
    if 'descripcion' in request.json and request.json['descripcion'] == '':
        abort(400)
    if 'categoria' in request.json and request.json['categoria'] == '':
        abort(400)
    if 'url_imagen' in request.json and request.json['url_imagen'] == '':
        abort(400)

    updated_obra = {
        'titulo': request.json.get('titulo', obra['titulo']),
        'descripcion': request.json.get('descripcion', obra['descripcion']),
        'categoria': request.json.get('categoria', obra['categoria']),

        'url_imagen': request.json.get('url_imagen', obra['url_imagen'])
    }

    result = obras_collection.update_one({'obra_id': obra_id}, {'$set': updated_obra})
    obra = obras_collection.find_one({'obra_id': obra_id})

    return json_util.dumps({'obra': obra}), 200


@app.route('/artesano/<string:art_id>/obras', methods=['GET'])
def get_obras_by_artesano(art_id):
    art = artesanos_collection.find_one({'custom_id': art_id})
    if art is None:
        abort(404)

    obras = list(obras_collection.find({'artesano_id': art_id}))
    return json_util.dumps({'obras': obras})


@app.route('/obras/categoria/<string:categoria>', methods=['GET'])
def get_obras_by_categoria(categoria):
    obras = list(obras_collection.find({'categoria': categoria}, {'_id': 0, 'obra_id': 1, 'titulo': 1, 'url_imagen': 1}))
    return json_util.dumps({'obras': obras})


@app.route('/obra/<string:obra_id>/detalles', methods=['GET'])
def get_obra_and_artesano(obra_id):
    obra = obras_collection.find_one({'obra_id': obra_id})
    if obra is None:
        abort(404)

    artesano = artesanos_collection.find_one({'custom_id': obra['artesano_id']})
    if artesano is None:
        abort(404)

    return json_util.dumps({'obra': obra, 'artesano': artesano})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

