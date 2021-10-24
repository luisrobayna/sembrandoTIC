from flask import Blueprint, request
from flask.json import jsonify
from function_jwt import write_token, validate_token
from function_jwt import write_token
from jwt import encode

from datos.models import user_model as User

routes_auth = Blueprint("routes_auth",__name__)

@routes_auth.route("/usuario/login",methods=["POST"])
def login():
    data = request.get_json()
    if 'email' not in data:
        return 'El correo es requerido para logarse', 412
    if 'password' not in data:
        return 'La clave es requerida para logearse', 412
    check_user = User.get_user(data['email'],data['password'])
    if check_user == None:
        response = jsonify({"message":"Usuario o contraseña equivocada"})
        response.status_code = 404
        return response
    else:
        #token = write_token(data=request.get_json())
        data['user_name'] = check_user[0]['user_name']
        del data['password']
        token = write_token(data=data)
        token = User.login_user(data['email'],token)

        return jsonify({"response": token,
                        "message":"Logeo existoso!!!"})


@routes_auth.route("/verify/token")
def verify():
    print(request.headers['Authorization'])
    token = request.headers['Authorization'].split(" ")[1]
    return validate_token(token, output=True)



def verify_token(token):
    #print(request.headers['Authorization'])
    #token = request.headers['Authorization'].split(" ")[1]
    return validate_token(token, output=True)
