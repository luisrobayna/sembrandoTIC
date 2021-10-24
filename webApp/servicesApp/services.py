from werkzeug.wrappers import response
from servicesApp import api_rest
import requests

API = api_rest
req = requests

def create_news(title,description,image):
    body = {"title": title,
            "description": description,
            "image":image}
    response = requests.post(f'{api_rest.API_REST}/noticia/crear', json=body)
    print(response.json())
    return response.json()



def update_user(user,description="",full_name="",age="",image="user_default.png"):
    body = {"description": description,
            "full_name": full_name,
            "age":age,
            "profile_image":image}
    print(body)
    response = requests.put(f'{api_rest.API_REST}/usuario/perfil/{user}', json=body)
    print(response)
    return response.json()