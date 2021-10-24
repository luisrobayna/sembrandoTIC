from datos.models import new_comment_model
from datetime import datetime
from routes.auth import verify_token


def create_comment_new(id_new,decription,token):
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    token_info = verify_token(token)#decode Token
    user_coment = token_info['user_name']
    id_comment = format(id(user_coment), 'x')
    return new_comment_model.create_comment_new(id_new,date,decription,id_comment,token_info['user_name'])


def get_comments(id_new):
    return new_comment_model.get_comments(id_new)


def update_comment(id_new,comment_id,description,token):
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    token_info = verify_token(token)#decode Token
    return new_comment_model.update_comment(id_new,comment_id,description,date,token_info['user_name'])


def delete_comment(id_new,id_comment,token):
    token_info = verify_token(token)#decode Token
    return new_comment_model.delete_comment(id_new,id_comment,token_info['user_name'])


