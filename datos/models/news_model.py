from datos.base_de_datos import BaseDeDatos
bd = BaseDeDatos()

def create_new(title, description, date, image):
    create_new_sql = f"""
        INSERT INTO NOTICIAS(TITULO, DESCRIPCION, IMAGEN, FECHA_HORA)
        VALUES ('{title}','{description}','{image}','{date}')
    """
    get_new_sql = f"""
        SELECT * FROM NOTICIAS WHERE FECHA_HORA = '{date}'
    """
   
    bd.ejecutar_sql(create_new_sql)
    return {"newArticle":
                {"id":register[0],
                "title":register[1],
                "description":register[2],
                "image":register[3],
                "date":register[4]} for register in bd.ejecutar_sql(get_new_sql)} 



def get_new(id):
    get_new_sql = f"""
    SELECT * FROM NOTICIAS WHERE NOTICIA_ID = {id}
"""
    return {"article":
                {"id":register[0],
                  "title":register[1],
                  "description":register[2],
                  "image":register[3],
                  "date":register[4]} for register in bd.ejecutar_sql(get_new_sql)}



def get_news():
    get_news_sql = f"""
    SELECT * FROM NOTICIAS
"""
    return {"articles":
                [{"id":register[0],
                  "title":register[1],
                  "description":register[2],
                  "image":register[3],
                  "date":register[4]} for register in bd.ejecutar_sql(get_news_sql)]}



def update_new(id,title,description,image,date,user_name):
    update_new_sql = f"""
    UPDATE NOTICIAS SET TITULO='{title}',DESCRIPCION='{description}',IMAGEN='{image}',FECHA_HORA='{date}' WHERE NOTICIA_ID={id}
"""
    get_new_sql = f"""
        SELECT * FROM NOTICIAS WHERE NOTICIA_ID = {id}
"""
    if user_name == "adminMaster02" or user_name == "adminMaster01":
        bd.ejecutar_sql(update_new_sql)
        return {"article":
                    {"id":register[0],
                    "title":register[1],
                    "description":register[2],
                    "image":register[3],
                    "date":register[4]} for register in bd.ejecutar_sql(get_new_sql)}
    else:
        return {"response":"No tiene los permisos para crear noticias"}


def delete_new(id,user_name):
    delete_new_sql= f"""
    DELETE FROM NOTICIAS WHERE NOTICIA_ID = {id}
"""
    get_new_sql = f"""
        SELECT * FROM NOTICIAS WHERE NOTICIA_ID = {id}
"""

    delete_comment_sql =f"""
        DELETE FROM COMENTARIOS_NOTICIA  WHERE ID_NOTICIA = {id}
    """
    if user_name == "adminMaster02" or user_name == "adminMaster01":
        info_new = bd.ejecutar_sql(get_new_sql)
        if info_new:
            bd.ejecutar_sql(delete_new_sql)#borramos noticia
            bd.ejecutar_sql(delete_comment_sql)#borramos comentarios de esa noticia
            return [{"id":register[0],
                    "title":register[1],
                    "description":register[2],
                    "image":register[3],
                    "date":register[4]} for register in info_new]
        else:
            return "No existe esta noticia"
    else:
        return "No tiene los permisos necesarios"