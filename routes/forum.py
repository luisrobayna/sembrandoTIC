from flask import Blueprint, request
from flask.json import jsonify
from werkzeug.wrappers import response
from services import forum_service

routes_forum = Blueprint("routes_forum",__name__)

@routes_forum.route('/foro/post/crear', methods=['POST'])
def create_post():
    data = request.get_json()
    if 'title' not in data:
        return {"response":'El titulo es requerido para la creacion del post'}, 412
    if 'description' not in data:
        return {"response":'La descripcion es requerida para la creacion del post'}, 412
    if 'token' not in data:
        return {"response":'Tienes que estar logeado para crear un post en el foro'}, 412
    response = forum_service.create_post(data['title'], data['description'],data['token'])
    return jsonify({"response":response}), 200



@routes_forum.route('/foro', methods=['GET'])
def get_forum():
   response =  forum_service.get_forum()
   if type(response) is not str:
       return jsonify({"response":response}),200
   else:
       return {"response":response},404


@routes_forum.route('/foro/post/<int:id_post>', methods=['GET'])
def get_post(id_post):
    response = forum_service.get_post(id_post)
    if type(response) is not str:
        return jsonify({"response":response}),200
    else:
        return {"response":response},404


@routes_forum.route('/foro/post/<int:id_post>', methods=['PUT'])
def update_post(id_post):
    data = request.get_json()
    if 'title' not in data:
        return {"response":"Es necesario al menos cambiar el titulo"},412
    if 'description' not in data:
        return {"response":"Es necesario al menos cambiar la descripcion"},412
    if 'token' not in data:
        return {"response":"Tienes que estar logeado para poder modificar tu post"},412
    response = forum_service.update_post(id_post,data['title'],data['description'],data['token'])
    if type(response) is not str:
        return jsonify({"response":response}), 200
    else:
        return {"response":response}


@routes_forum.route('/foro/post/<int:id_post>', methods=['DELETE'])
def delete_post(id_post):
    data = request.get_json()
    if 'token' not in data:
        return {"response":"Tienes que estar logeado para poder modificar tu post"},412
    response = forum_service.delete_post(id_post,data['token'])
    if type(response) is not str:
        return jsonify({"response":response}),200
    else:
        return {"response":response},404