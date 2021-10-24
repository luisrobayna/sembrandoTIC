from flask import Blueprint, request
from flask.json import jsonify
from werkzeug.wrappers import response
from services import user_service

routes_user = Blueprint("routes_user",__name__)

@routes_user.route("/usuario/registro",methods=['Post'])
def create_user():
    user_info = request.get_json()
    rol_account = "normal"
    if 'user_name' not in user_info:
        return {"response":'El nombre de usuario es requerido para registrarse'}, 412
    if 'email' not in user_info:
        return {"response":'El correo es requerido para registrarse'}, 412
    if 'password' not in user_info:
        return {"response":'La clave es requerida para registrarse'}, 412
    if user_info['user_name'] == "adminMaster01" or user_info['user_name'] == "adminMaster02":
        rol_account = "admin"
    newUser = user_service.create_user(user_info['user_name'],user_info['email'],user_info['password'],rol_account)
    if type(newUser) is not str:
        return jsonify({"response":newUser,
                    "message":"Creacion de cuenta exitosa"}),200
    return {"response":newUser},412
    


@routes_user.route("/usuario/cerrar_sesion",methods=["DELETE"])
def log_out():
    data = request.get_json()
    response = user_service.log_out(data["token"])
    return {"response":response},200


@routes_user.route("/usuario/perfil/<string:user_name>",methods=["GET"])
def get_profile(user_name):
    profile = user_service.get_profile(user_name)
    if type(profile) is str:
        return {"response": profile},404
    else:
        return jsonify({"response": profile}),200



@routes_user.route("/usuario/perfil/<string:user_name>",methods=["PUT"])
def update_profile(user_name):
    data = request.get_json()
    response = user_service.update_profile(user_name,data['description'],data['full_name'],data['age'],data['profile_image'])
    if type(response) is str:
        return {"response": response},400
    else:
        return jsonify({"response":response}),200


@routes_user.route("/usuario/perfil/<string:user_name>",methods=["DELETE"])
def delete_account(user_name):
    data = request.get_json()
    if 'token' not in data:
        return {"response":"Tienes que estar logeado para borrar tu cuenta"},402
    response = user_service.delete_account(user_name,data["token"])
    if type(response) is str:
        return {"response":response},400
    else:
        return jsonify({"response":response,
                        "message":"Cuenta eliminada exitosamente"}),200
