from datos.base_de_datos import BaseDeDatos

bd = BaseDeDatos()

def create_comment_new(id_new,date,decription,id_comment,user_name):
    get_user_sql = f"""
    SELECT FOTO_PERFIL FROM USUARIOS WHERE NOMBRE_USUARIO = '{user_name}'
"""
    image_tupla = bd.ejecutar_sql(get_user_sql)
    if len(image_tupla) == 0 or image_tupla[0][0] == None:
        image = "image_default.png"
    else:
        image = image_tupla[0][0]

    get_comment_new_sql = f"""
    INSERT INTO COMENTARIOS_NOTICIA(COMENTARIO_ID,NOMBRE_USUARIO, FECHA_HORA, DESCRIPCION_COMENTARIO, FOTO_PERFIL,ID_NOTICIA)
        VALUES ('{id_comment}','{user_name}','{date}','{decription}','{image}',{id_new})
"""
    get_new_comment_sql = f"""
        SELECT * FROM COMENTARIOS_NOTICIA WHERE COMENTARIO_ID = '{id_comment}'
    """
    compare_id_tables_sql = f"""
    SELECT NOTICIA_ID FROM NOTICIAS WHERE NOTICIA_ID = {id_new}
"""
  
    compared = bd.ejecutar_sql(compare_id_tables_sql)
    if compared:
        bd.ejecutar_sql(get_comment_new_sql)
        return [{"idComment": register[0],
                 "user_name": register[1],
                 "date": register[2],
                 "description": register[3],
                 "imageProfile":register[4],
                 "idNew":register[5]}for register in bd.ejecutar_sql(get_new_comment_sql)]
    else:
        return "Error al comentar, no existe la noticia"



def get_comments(id_new):
    get_comments_sql = f"""
    SELECT * FROM COMENTARIOS_NOTICIA WHERE ID_NOTICIA = '{id_new}' 
"""
    comments = bd.ejecutar_sql(get_comments_sql)
    if comments:
        return {"commentNew":
                    [{"idComment": register[0],
                    "user": register[1],
                    "date": register[2],
                    "description": register[3],
                    "pictureProfile":register[4],
                    "idNew":register[5]}for register in bd.ejecutar_sql(get_comments_sql)]}
    else:
        return "Estas intentando ver los comentarios de una noticia que no existe"



def update_comment(id_new,comment_id,description,date,user_name):
    update_comment_sql =  f"""
               UPDATE COMENTARIOS_NOTICIA SET DESCRIPCION_COMENTARIO='{description}',FECHA_HORA='{date}' WHERE COMENTARIO_ID='{comment_id}'
    """
    get_new_comment_sql = f"""
               SELECT * FROM COMENTARIOS_NOTICIA WHERE COMENTARIO_ID = '{comment_id}'
    """
    get_new_sql = f"""
                SELECT ID_NOTICIA FROM COMENTARIOS_NOTICIA WHERE COMENTARIO_ID = '{comment_id}' AND ID_NOTICIA = '{id_new}'
    """
    info_new = bd.ejecutar_sql(get_new_sql)
    if info_new:
        comment = bd.ejecutar_sql(get_new_comment_sql)
        id_comment,user,date_comment,description_comment,image,new_id = comment[0]
        if user == user_name:
            bd.ejecutar_sql(update_comment_sql)
            if comment:
                return {"update_comment":{
                        "idComment": register[0],
                        "user": register[1],
                        "date": register[2],
                        "description": register[3],
                        "imageProfile":register[4],
                        "idNew":register[5]}for register in bd.ejecutar_sql(get_new_comment_sql)}
        else:
            return "Este comentario no es tuyo"
             
    else:
        return "No existe el comentario"



def delete_comment(id_new,id_comment,user_name):
    delete_comment_sql = f"""
    DELETE FROM COMENTARIOS_NOTICIA WHERE COMENTARIO_ID ='{id_comment}'
"""
    get_comment_new_sql = f"""
           SELECT * FROM COMENTARIOS_NOTICIA WHERE COMENTARIO_ID = '{id_comment}'
"""
    get_new_sql = f"""
            SELECT ID_NOTICIA FROM COMENTARIOS_NOTICIA WHERE COMENTARIO_ID = '{id_comment}' AND ID_NOTICIA = '{id_new}'
"""
    if user_name == "adminMaster02" or user_name == "adminMaster01":
        is_comment = bd.ejecutar_sql(get_new_sql)
        if is_comment:
            comment = bd.ejecutar_sql(get_comment_new_sql)
            bd.ejecutar_sql(delete_comment_sql)
            return [{"deleted_comment":{
                        "idComment": register[0],
                        "user": register[1],
                        "date": register[2],
                        "description": register[3],
                        "imageProfile":register[4],
                        "idNew":register[5],
                        "message":"Comentario eliminado por el Admin"}for register in comment}]
        else:
            return "No existe el comentario"
    else:
        is_comment = bd.ejecutar_sql(get_new_sql)
        if is_comment:
            comment = bd.ejecutar_sql(get_comment_new_sql)
            comment_id,user,date_comment,description_comment,image,new_id = comment[0]
            if user == user_name:
                bd.ejecutar_sql(delete_comment_sql)
                return [{"deleted_comment":{
                        "idComment": register[0],
                        "user": register[1],
                        "date": register[2],
                        "description": register[3],
                        "imageProfile":register[4],
                        "idNew":register[5]}for register in comment}]
            else:
                return "Este comentario no te pertenece"

        else:
            return "No existe el comentario"

        
