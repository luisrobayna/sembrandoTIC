from datos.base_de_datos import BaseDeDatos
import secrets
from flask import request
from flask.json import jsonify
from function_jwt import write_token, validate_token
from jwt import decode


bd = BaseDeDatos()

def create_user(user_name, email_user, password,rol_account):
    create_user_sql = f"""
            INSERT INTO USUARIOS(NOMBRE_USUARIO, CORREO, CONTRASEÑA,DESCRIPCION_USUARIO,NOMBRE_COMPLETO,EDAD,FOTO_PERFIL,ROL)
            VALUES ('{user_name}','{email_user}','{password}','','','','user_default.png','{rol_account}')
        """
    search_user_sql = f"""
    SELECT NOMBRE_USUARIO,CORREO,ROL FROM USUARIOS WHERE NOMBRE_USUARIO = '{user_name}' OR CORREO = '{email_user}'
"""

    search_user = bd.ejecutar_sql(search_user_sql)
    if search_user:
        user = search_user[0]
        nick, email, password = user
        if nick == user_name:
            message = f"{user_name} ya esta en uso,intenta otro nombre de usuario"
            return message
        elif email == email_user:
            message = f"{email_user} ya esta en uso, intenta otro correo"
            return message
    else:
        bd.ejecutar_sql(create_user_sql)
        return [{"username": register[0],
                 "email": register[1],
                 "rol": register[2]}for register in bd.ejecutar_sql(search_user_sql)]



def get_user(email,password):
    get_user_sql = f"""
    SELECT NOMBRE_USUARIO,CORREO,CONTRASEÑA FROM USUARIOS WHERE CORREO = '{email}'
""" 
    check_user = bd.ejecutar_sql(get_user_sql)
    if len(check_user) != 0:
        user_name,email_user , pass_user = check_user[0]
        if password == pass_user and email == email_user:
            return [{"user_name": register[0],
                    "email": register[1],
                    "password":register[2]} for register in bd.ejecutar_sql(get_user_sql)]
    else:
        return None


def verify():
    token = request.headers['Authorization'].split(" ")[1]
    return validate_token(token, output=True)



def login_user(email,token):
    get_user_sql = f"""
    SELECT NOMBRE_USUARIO FROM USUARIOS WHERE CORREO = '{email}'
""" 
    user_name = bd.ejecutar_sql(get_user_sql)
    token_str = str(token).split("'")[1]
    insert_token_sql = f"""
        INSERT INTO USUARIOS_TOKENS(NOMBRE_USUARIO,CORREO,TOKEN_SECRET)
        VALUES ('{user_name[0][0]}','{email}','{token_str}')
        """
    bd.ejecutar_sql(insert_token_sql)
    return token_str
    


def log_out(email):
    delete_token_sql = f"""
    DELETE FROM USUARIOS_TOKENS WHERE CORREO = '{email}'
"""
    get_user_sql = f"""
        SELECT NOMBRE_USUARIO FROM USUARIOS_TOKENS WHERE CORREO = '{email}'
    """
    user = bd.ejecutar_sql(get_user_sql)
    bd.ejecutar_sql(delete_token_sql)
    if user:
        return {"message":"Se ha cerrado sesion correctamente"}
    else:
        return {"message":"No puedes cerrar sesion de un usuario que no esta logeado"}



def get_profile(user_name):
    get_profile_sql= f"""
    SELECT NOMBRE_USUARIO,DESCRIPCION_USUARIO,NOMBRE_COMPLETO,EDAD,FOTO_PERFIL FROM USUARIOS WHERE NOMBRE_USUARIO = '{user_name}'
"""
    perfil = bd.ejecutar_sql(get_profile_sql)
    if perfil:
        return [{"user_name":register[0],
                "description":register[1],
                "full_name":register[2],
                "age":register[3],
                "profile_image":register[4]}for register in bd.ejecutar_sql(get_profile_sql)]
    else:
        return "No existe este perfil"



def update_profile(user_name,description,name,age,profile_image):
    profile_user_sql = f"""
    UPDATE USUARIOS SET DESCRIPCION_USUARIO='{description}',NOMBRE_COMPLETO='{name}',EDAD='{age}',FOTO_PERFIL='{profile_image}' WHERE NOMBRE_USUARIO='{user_name}' 
"""
    get_user_sql = f"""
    SELECT NOMBRE_USUARIO,CORREO,DESCRIPCION_USUARIO,NOMBRE_COMPLETO,EDAD,FOTO_PERFIL FROM USUARIOS WHERE NOMBRE_USUARIO = '{user_name}'
"""
    update_comment_new_sql = f"""
    UPDATE COMENTARIOS_NOTICIA SET FOTO_PERFIL= '{profile_image}' WHERE NOMBRE_USUARIO='{user_name}' 
"""
    update_comment_post_sql = f"""
    UPDATE COMENTARIOS_POST SET FOTO_PERFIL= '{profile_image}' WHERE NOMBRE_USUARIO='{user_name}' 
"""
    update_post_sql = f"""
    UPDATE POSTS SET FOTO_PERFIL= '{profile_image}' WHERE NOMBRE_USUARIO='{user_name}' 
"""

 
    bd.ejecutar_sql(profile_user_sql)
    bd.ejecutar_sql(update_comment_new_sql)#Modificamos la foto del comentario
    bd.ejecutar_sql(update_comment_post_sql)#cuando cambiamos foto de perfil
    bd.ejecutar_sql(update_post_sql)#Tambien post, todo donde este el usuario
    print(bd.ejecutar_sql(get_user_sql))
    return [{"user_name":register[0],
            "email":register[1],
            "description":register[2],
            "full_name":register[3],
            "age":register[4],
            "profile_image":register[5]}for register in bd.ejecutar_sql(get_user_sql)]


   


def delete_account(user_name,token):
    intento_email = token
    delete_user_sql = f"""
    DELETE FROM USUARIOS WHERE CORREO= '{token}'
"""
    delete_token_sql = f"""
        DELETE FROM USUARIOS_TOKENS WHERE CORREO = '{token}'
    """
 
    get_userName_sql = f"""
        SELECT * FROM USUARIOS WHERE CORREO = '{intento_email}'
    """

    admin_permision_sql = f"""
        DELETE FROM USUARIOS WHERE NOMBRE_USUARIO = '{user_name}'
"""

    admin_permision_token_sql = f"""
        DELETE FROM USUARIOS_TOKENS WHERE NOMBRE_USUARIO = '{user_name}'
    """
    get_eliminate_account_sql =  get_user_sql = f"""
        SELECT * FROM USUARIOS WHERE NOMBRE_USUARIO = '{user_name}'
"""
    delete_comment_news_sql = f"""
    DELETE FROM COMENTARIOS_NOTICIA WHERE NOMBRE_USUARIO ='{user_name}'
"""
    delete_comment_posts_sql = f"""
    DELETE FROM COMENTARIOS_POST WHERE NOMBRE_USUARIO ='{user_name}'
"""
    delete_post_sql = f"""
    DELETE FROM POSTS WHERE NOMBRE_USUARIO = '{user_name}'
"""
    user = bd.ejecutar_sql(get_userName_sql)
    if len(user) != 0:
        nick_name,email,password,description,full_name,age,image_profile,rol = user[0]
        if rol == "admin":
            admin_accion = bd.ejecutar_sql(get_eliminate_account_sql)
            bd.ejecutar_sql(delete_comment_posts_sql)#borramos comentarios post
            bd.ejecutar_sql(delete_post_sql)#borramos post
            bd.ejecutar_sql(delete_comment_news_sql)#borramos comentarios noticia
            bd.ejecutar_sql(admin_permision_sql)#borramos usuario
            bd.ejecutar_sql(admin_permision_token_sql)#borramos token
            return [{"user_name":register[0],
                "email":register[1],
                "password":register[2],
                "description":register[3],
                "full_name":register[4],
                "age":register[5],
                "profile_image":register[6],
                "rol": register[7],
                "messageAdmin":"Cuenta Baneada"}for register in admin_accion]
        else:
            if nick_name == user_name:
                print("ELIMINASTE LA CUENTAAAAAAAAAAAAAAAAAA")
                bd.ejecutar_sql(delete_comment_posts_sql)#borramos comentarios post
                bd.ejecutar_sql(delete_post_sql)#borramos post
                bd.ejecutar_sql(delete_comment_news_sql)#borramos comentarios noticia
                bd.ejecutar_sql(delete_user_sql)#borramos usuario
                bd.ejecutar_sql(delete_token_sql)#borramos token
                return [{"user_name":register[0],
                    "email":register[1],
                    "password":register[2],
                    "description":register[3],
                    "full_name":register[4],
                    "age":register[5],
                    "profile_image":register[6]}for register in user]
            else:
                return "No puedes eliminar una cuenta que no te pertenece"
    else:
        return "No puedes eliminar esta cuenta porque no existe"
     
