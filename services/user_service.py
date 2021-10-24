from datos.models import user_model
from routes.auth import verify_token

def create_user(user_name,email,password,rol_account):
    return user_model.create_user(user_name,email,password,rol_account)


def login_user(email, token):
    return user_model.login_user(email,token)


def log_out(token):
    token_info = verify_token(token)#decode Token
    #print(token_info['email'])
    return user_model.log_out(token_info['email'])


def get_profile(user_name):
    return user_model.get_profile(user_name)


def update_profile(user_name,description,name,age,profile_image):
    return user_model.update_profile(user_name,description,name,age,profile_image)


def delete_account(user_name,token):
    token_info = verify_token(token)#decode Token
    return user_model.delete_account(user_name,token_info['email'])