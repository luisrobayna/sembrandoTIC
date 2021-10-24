from datos.base_de_datos import BaseDeDatos

bd = BaseDeDatos()

def create_post(title,description,date,user_name):
    
    get_user_sql = f"""
    SELECT FOTO_PERFIL FROM USUARIOS WHERE NOMBRE_USUARIO = '{user_name}'
"""
    
    image_tupla = bd.ejecutar_sql(get_user_sql)
    if len(image_tupla) == 0 or image_tupla[0][0] == None:
        image = "user_default.png"
    else:
        image = image_tupla[0][0]
        


    create_post_sql = f"""
        INSERT INTO POSTS(TITULO_POST, DESCRIPCION, FECHA_HORA, NOMBRE_USUARIO,FOTO_PERFIL,VISTAS)
        VALUES ('{title}','{description}','{date}','{user_name}','{image}',0)
"""
    get_post_sql = f"""
        SELECT * FROM POSTS WHERE FECHA_HORA = '{date}'
"""
    bd.ejecutar_sql(create_post_sql)
    return {"newPost":
            {"id":register[0],
             "title":register[1],
             "description":register[2],
             "date":register[3],
             "user_name":register[4],
             "profile_image":register[5],
             "views:":register[6]}for register in bd.ejecutar_sql(get_post_sql)}



def get_forum():
    get_posts_sql = f"""
    SELECT POST_ID, TITULO_POST, DESCRIPCION, FECHA_HORA, NOMBRE_USUARIO, VISTAS FROM POSTS
"""

    forum = bd.ejecutar_sql(get_posts_sql)
    if forum:
        return {"posts":
                [{"id": register[0],
                "title": register[1],
                "description": register[2],
                "date": register[3],
                "user_name": register[4],
                "views":register[5]} for register in bd.ejecutar_sql(get_posts_sql)]
                }
    else:
        return "No hay ningun post en el foro aun"


def get_post(id):
    get_post_sql = f"""
    SELECT * FROM POSTS WHERE POST_ID = {id}
"""


    post = bd.ejecutar_sql(get_post_sql)
    if post:
        print(post[0],"ANTES DE SUMARLE 1")
        id_post,title,description,date_post,user_creator,image_profile,views = post[0]
        views = views + 1  #add +1 when the user visit the page.

        view_post_sql = f"""
        UPDATE POSTS SET VISTAS={views} WHERE POST_ID={id}
        """
        
        bd.ejecutar_sql(view_post_sql)
        print("El post quedaria",bd.ejecutar_sql(get_post_sql))
        return  {"post":
                    {"id": register[0],
                    "title": register[1],
                    "description": register[2],
                    "date": register[3],
                    "userCreator": register[4],
                    "image_profile": register[5],
                    "views":register[6]} for register in bd.ejecutar_sql(get_post_sql)
                    }
    else:
        return "No existe este post"


def update_post(id,title,description,date,user_name):
    update_post_sql = f"""
    UPDATE POSTS SET TITULO_POST='{title}',DESCRIPCION='{description}',FECHA_HORA='{date}' WHERE POST_ID={id}
"""
    get_post_sql = f"""
           SELECT * FROM POSTS WHERE POST_ID = {id}
"""
    get_post_id_sql = f"""
           SELECT POST_ID FROM POSTS WHERE POST_ID = {id}
"""
    id_post = bd.ejecutar_sql(get_post_id_sql)
    if id_post:
        post = bd.ejecutar_sql(get_post_sql)
        if post[0][4] == user_name:
            bd.ejecutar_sql(update_post_sql)
            return {"post":
                    {"id": register[0],
                    "title": register[1],
                    "description": register[2],
                    "date": register[3],
                    "userCreator": register[4],
                    "image_profile": register[5],
                    "views":register[6]} for register in bd.ejecutar_sql(get_post_sql)
                    } 
        else:
            return "Este post no es tuyo"
    else:
        return "No existe este post"



def delete_post(id,user_name):
    get_post_sql = f"""
               SELECT * FROM POSTS WHERE POST_ID = {id}
"""
    delete_post_sql = f"""
    DELETE FROM POSTS WHERE POST_ID = {id}
"""
    delete_post_comment_sql = f"""
    DELETE FROM COMENTARIOS_POST WHERE ID_POST = {id}
"""
    
    post = bd.ejecutar_sql(get_post_sql)
    if post:
        if user_name == "adminMaster02" or user_name == "adminMaster01":
            bd.ejecutar_sql(delete_post_sql)
            bd.ejecutar_sql(delete_post_comment_sql)
            return {"post":
                            {"id": register[0],
                            "title": register[1],
                            "description": register[2],
                            "date": register[3],
                            "userCreator": register[4],
                            "image_profile": register[5],
                            "views":register[6]} for register in post
                            },{"message":"Post eliminado por un admin"}
        else:
            if post[0][4] == user_name:
                bd.ejecutar_sql(delete_post_sql)
                bd.ejecutar_sql(delete_post_comment_sql)
                return {"post":
                            {"id": register[0],
                            "title": register[1],
                            "description": register[2],
                            "date": register[3],
                            "userCreator": register[4],
                            "image_profile": register[5],
                            "views":register[6]} for register in post
                            },{"message":"Post eliminado"}
            else:
                return "Este post no es tuyo" 
    else:
        return "No existe este post"