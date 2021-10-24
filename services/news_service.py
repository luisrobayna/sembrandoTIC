from datos.models import news_model
from datetime import datetime
from routes.auth import verify_token

def create_new(title, description,image):
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return news_model.create_new(title, description,date, image)


def get_new(id):
    return news_model.get_new(id)


def get_news():
    return news_model.get_news()


def update_new(id,title,description,image,token):
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    token_info = verify_token(token)#decode Token
    return news_model.update_new(id,title,description,image,date,token_info['user_name'])

def delete_new(id,token):
    token_info = verify_token(token)#decode Token
    return news_model.delete_new(id,token_info['user_name'])
