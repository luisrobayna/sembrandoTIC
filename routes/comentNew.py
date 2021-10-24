from flask import Blueprint, request
from flask.json import jsonify
from werkzeug.wrappers import response
from services import new_coment_service

routes_comment_news = Blueprint("routes_comment_news",__name__)

@routes_comment_news.route('/noticia/<int:id_new>/comment', methods=['POST'])
def crear_comentario_noticia(id_new):
    data = request.get_json()
    if 'description' not in data:
        return {"response":'La descripcion es requerida para crear el comentario'}, 412
    if 'token' not in data:
        return {"response":"Tienes que estar logeado para poder comentar"}
    response = new_coment_service.create_comment_new(id_new,data['description'],data['token'])
    if type(response) is str:
            return {"response":response},412
    else:
        return jsonify({"response": response}),200



@routes_comment_news.route('/noticia/<int:id_new>/comment', methods=['GET'])
def get_comments_new(id_new):
    response = new_coment_service.get_comments(id_new)
    if type(response) is str:
        return {"response": response}, 404
    else:
        return jsonify({"response": response}), 200



@routes_comment_news.route('/noticia/<int:id_new>/comment/<string:id_comment>', methods=['PUT'])
def update_comment_new(id_new,id_comment):
    data = request.get_json()
    if 'description' not in data:
        return {"response":"Necesitas almenos la descripcion del comentario"},412
    if 'token' not in data:
        return {"response":"Tienes que logearte para poder editar tu comentario"},412
    
    response = new_coment_service.update_comment(id_new,id_comment,data['description'],data['token'])
    if type(response) is str:
        return {"response":response}, 404
    else:
        return jsonify({"response":response}), 200



@routes_comment_news.route('/noticia/<int:id_new>/comment/<string:id_comment>', methods=['DELETE'])
def delete_comment_new(id_new,id_comment):
    data = request.get_json()
    if 'token' not in data:
        return {"response":"Tienes que logearte para poder borrar el comentario"}
    response = new_coment_service.delete_comment(id_new,id_comment,data['token'])

    if type(response) is str:
            return {"response":response}, 404
    else:
        return jsonify({"response": response}),200
       
