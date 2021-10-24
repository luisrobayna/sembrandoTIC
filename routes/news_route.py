from flask import Blueprint, request,Flask
from flask.json import jsonify
from werkzeug.wrappers import response
import os
from werkzeug.utils import secure_filename
from services import news_service

app = Flask(__name__)
routes_news = Blueprint("routes_news",__name__)


@routes_news.route('/noticia/crear',methods=['POST'])
def createNew():
     data = request.get_json()
     print(data,"LO QUE NOS LLEGAAAAAAAAAAAAAAA")
     image = ""
     if 'title' not in data:
         return {"response":'El titulo es requerido para la creacion de la noticia'}, 412
     if 'description' not in data:
         return {"response":'La descripcion es requerida para la creacion de la noticia'}, 412
     if 'image'  in data:
          image = data['image']
          print(image)

     info_new = news_service.create_new(data['title'], data['description'], image)
     return jsonify({"response":info_new}), 200



@routes_news.route('/noticia/<int:id_new>', methods=['GET'])
def get_news(id_new):
    info_new = news_service.get_new(id_new)
    if info_new:
        return jsonify(info_new), 200
    else:
        return {"response":"Ups no existe la noticia que quieres acceder!!"},404



@routes_news.route('/noticias', methods=['GET'])
def get_all_news():
    news = news_service.get_news()
    if news:
        return jsonify(news),200
    else:
        return {"response":"No existe ninguna noticia para mostrar"}, 200



@routes_news.route('/noticia/<int:id_new>', methods=['PUT'])
def actualizar_noticia(id_new):
     data = request.get_json()
     if 'token' not in data:
          return {"response":"Tienes que estar logeado para modificar la noticia"},400
     if 'image' in data:
          image = data['image']
     info_new = news_service.update_new(id_new, data['title'], data['description'], image,data['token'])
     if type(info_new) is str:
         return info_new,400
     else:
          return jsonify({"response":info_new}), 200


@routes_news.route('/noticia/<int:id_new>', methods=['DELETE'])
def borra_noticia(id_new):
     data = request.get_json()
     if 'token' not in data:
          return {"response":"Tienes que estar logeado para modificar la noticia"},400
     new_deleted = news_service.delete_new(id_new,data['token'])
     if type(new_deleted) is str:
        return {"response":
                    {"message":new_deleted}},404
     else:
        return jsonify({"response":{"article_deleted": new_deleted,
                                    "message":"Noticia borrada exitosamente"}}),404
