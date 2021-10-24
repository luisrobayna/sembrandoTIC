from flask import Blueprint, request
from flask import json
from flask.json import jsonify
from werkzeug.wrappers import response
from services import forum_comment_service

routes_comment_forum = Blueprint("routes_comment_forum",__name__)

@routes_comment_forum.route('/foro/post/<int:id_post>/comment', methods=['POST'])
def create_comment_post(id_post):
    data = request.get_json()
    if 'description' not in data:
        return {"response": 'La descripcion es requerida para crear el comentario'}, 412
    if 'token' not in data:
        return {"response":'Necesitas logearte para poder comentar'},412

    response = forum_comment_service.create_comment(id_post,data['description'], data['token'])
    if type(response) is not str:
        return jsonify({"response":response}), 200
    else:
        return {"response":response},404


@routes_comment_forum.route('/foro/post/<int:id_post>/comment', methods=['GET'])
def get_comments_post(id_post):
    response = forum_comment_service.get_comments(id_post)
    if type(response) is not str:
        return jsonify({"response":response}), 200
    else:
        return {"response":response}, 404


@routes_comment_forum.route('/foro/post/<int:id_post>/comment/<string:id_comment>', methods=['PUT'])
def update_comment_post(id_post,id_comment):
    data = request.get_json()
    if 'description' not in data:
        return {"response":"Para modificar el comentario tienes que al menos modificar la descripcion"},412
    if 'token' not in data:
        return {"response":"Tienes que logearte para modificar tu comentario"},412

    response = forum_comment_service.update_comment(id_post,id_comment,data['description'],data['token'])
    if type(response) is not str:
        return jsonify({"response":response}),200
    else:
        return {"response":response},404



@routes_comment_forum.route('/foro/post/<int:id_post>/comment/<string:id_comment>', methods=['DELETE'])#bien//Modificar endpoint utilizando el token como identificador, sacar la aprte de usuario del endpoint
def delete_comment_post(id_post,id_comment):
    data = request.get_json()
    if 'token' not in data:
        return {"response":"Tienes que logearte para borrar tu comentario"},412
    response = forum_comment_service.delete_commment(id_post,id_comment,data['token'])

    if type(response) is not str:
        return jsonify({"response":response}), 200
    else:
        return {"response":response}, 404
        
    