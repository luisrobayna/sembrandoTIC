from datos.models import forum_model
from datetime import datetime
from routes.auth import verify_token

def create_post(title,description,token):
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    token_info = verify_token(token)#decode Token
    return forum_model.create_post(title,description,date,token_info['user_name'])


def get_forum():
    return forum_model.get_forum()


def get_post(id):
    return forum_model.get_post(id)


def update_post(id,title,description,token):
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    token_info = verify_token(token)#decode Token
    return forum_model.update_post(id,title,description,date,token_info['user_name'])


def delete_post(id,token):
    token_info = verify_token(token)#decode Token
    return forum_model.delete_post(id,token_info['user_name'])