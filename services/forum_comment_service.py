from datos.models import forum_comment_model
from datetime import datetime
from routes.auth import verify_token

def create_comment(id_post,description,token):
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    token_info = verify_token(token)#decode Token
    user_coment = token_info['user_name']
    id_comment = format(id(user_coment), 'x')
    return forum_comment_model.create_comment_post(id_post,description,date,id_comment,token_info['user_name'])


def get_comments(id_post):
    return forum_comment_model.get_comments(id_post)


def update_comment(id_post,id_comment,description,token):
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    token_info = verify_token(token)#decode Token
    return forum_comment_model.update_comment(id_post,id_comment,description,date,token_info['user_name'])


def delete_commment(id_post,id_comment,token):
    token_info = verify_token(token)#decode Token
    return forum_comment_model.delete_comment(id_post,id_comment,token_info['user_name'])