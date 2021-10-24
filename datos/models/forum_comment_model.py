from datos.base_de_datos import BaseDeDatos

bd = BaseDeDatos()

def create_comment_post(id_post,description,date,id_comment,user_name):
    get_user_sql = f"""
    SELECT FOTO_PERFIL FROM USUARIOS WHERE NOMBRE_USUARIO = '{user_name}'
"""
    image_tupla = bd.ejecutar_sql(get_user_sql)
    if len(image_tupla) == 0 or image_tupla[0][0] == None:
        image = "image_default.png"
    else:
        image = image_tupla[0][0]

    comment_post_sql = f"""
        INSERT INTO COMENTARIOS_POST(COMENTARIO_POST_ID,NOMBRE_USUARIO, DESCRIPCION_COMENTARIO, FECHA_HORA, FOTO_PERFIL,ID_POST)
            VALUES ('{id_comment}','{user_name}','{description}','{date}','{image}',{id_post})
    """
    get_post_coment_sql = f"""
            SELECT * FROM COMENTARIOS_POST WHERE COMENTARIO_POST_ID = '{id_comment}'
        """
    get_post_id_sql = f"""
        SELECT POST_ID FROM POSTS WHERE POST_ID = {id_post}
    """
    compared = bd.ejecutar_sql(get_post_id_sql)

    if compared:
        bd.ejecutar_sql(comment_post_sql)
        return {"newPostComment":
                {"idComment":register[0],
                 "userName":register[1],
                 "description":register[2],
                 "date":register[3],
                 "imageProfile":register[4],
                 "idPost":register[5]}for register in bd.ejecutar_sql(get_post_coment_sql)},{
                  "message":"Comentario creado exitosamente"
                 }
    else:
        return "No existe el post"


def get_comments(id_post):
    get_comments_sql = f"""
    SELECT * FROM COMENTARIOS_POST WHERE ID_POST = '{id_post}' 
"""
    get_post_id_sql = f"""
        SELECT POST_ID FROM POSTS WHERE POST_ID = {id_post}
    """
    compared = bd.ejecutar_sql(get_post_id_sql)
    if compared:
        comments = bd.ejecutar_sql(get_comments_sql)
        if comments:
            return {"postComments":[
                    {"idComment":register[0],
                    "user_name":register[1],
                    "description":register[2],
                    "date":register[3],
                    "pictureProfile":register[4],
                    "idPost":register[5]}for register in bd.ejecutar_sql(get_comments_sql)]}
        else:
            return "No hay comentarios aun"
    else:
        return "No existe este post"



def update_comment(id_post,id_comment,description,date,user_name):
    update_comment_sql =  f"""
    UPDATE COMENTARIOS_POST SET DESCRIPCION_COMENTARIO='{description}',FECHA_HORA='{date}' WHERE COMENTARIO_POST_ID='{id_comment}'
"""
    get_post_coment_sql = f"""
               SELECT * FROM COMENTARIOS_POST WHERE COMENTARIO_POST_ID = '{id_comment}'
    """
    get_post_sql = f"""
                   SELECT * FROM POSTS WHERE POST_ID = '{id_post}'
        """
    post = bd.ejecutar_sql(get_post_sql)
    if post:
        comment = bd.ejecutar_sql(get_post_coment_sql)
        comment_id,user,description_comment,date_comment,image,post_id = comment[0]
        if post_id == id_post:
            if user == user_name:
                bd.ejecutar_sql(update_comment_sql)
                comentario = bd.ejecutar_sql(get_post_coment_sql)
                return {"postComment":{
                            "idComment":register[0],
                            "user_name":register[1],
                            "description":register[2],
                            "date":register[3],
                            "pictureProfile":register[4],
                            "idPost":register[5]}for register in bd.ejecutar_sql(get_post_coment_sql)
                        },{"message":"Comentario modificado!!"}
            else:
                return "No puedes modificar el comentario"
        else:
            return "No existe el comentario en este post"
    else:
        return "No existe el comentario"


def delete_comment(id_post,id_comment, user_name):
    delete_comment_sql = f"""
    DELETE FROM COMENTARIOS_POST WHERE COMENTARIO_POST_ID ='{id_comment}'
"""
    get_post_coment_sql = f"""
           SELECT * FROM COMENTARIOS_POST WHERE COMENTARIO_POST_ID = '{id_comment}'
"""
    get_post_id_sql = f"""
            SELECT ID_POST FROM COMENTARIOS_POST WHERE COMENTARIO_POST_ID = '{id_comment}' AND ID_POST= '{id_post}'
"""
    if user_name == "adminMaster02" or user_name == "adminMaster01":
        is_comment = bd.ejecutar_sql(get_post_id_sql)
        if is_comment:
            comment = bd.ejecutar_sql(get_post_coment_sql)
            bd.ejecutar_sql(delete_comment_sql)
            return {"commentRemoved":{
                            "idComment":register[0],
                            "user_name":register[1],
                            "description":register[2],
                            "date":register[3],
                            "pictureProfile":register[4],
                            "idPost":register[5]}for register in comment
                        },{"message":"Comentario borrado por un admin"} 
        else:
            return "No existe este comentario"
    else:
        is_comment = bd.ejecutar_sql(get_post_id_sql)
        if is_comment:
            comment = bd.ejecutar_sql(get_post_coment_sql)
            comment_id,user,date_comment,description_comment,image,post_id = comment[0]
            if user == user_name:
                bd.ejecutar_sql(delete_comment_sql)
                return {"commentRemoved":{
                            "idComment":register[0],
                            "user_name":register[1],
                            "description":register[2],
                            "date":register[3],
                            "pictureProfile":register[4],
                            "idPost":register[5]}for register in comment
                        },{"message":"Comentario borrado"}
            else:
                return "Este comentario no te pertenece"
        else:
            return "No existe el comentario"