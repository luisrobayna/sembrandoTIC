import sqlite3

sql_tabla_roles = '''
CREATE TABLE ROLES(
VISITANTE_ID INTEGER PRIMARY KEY, 
TIPO_ROL TEXT NOT NULL
)
'''

sql_tabla_usuarios = '''
CREATE TABLE USUARIOS(
NOMBRE_USUARIO TEXT PRIMARY KEY, 
CORREO TEXT,
CONTRASEÑA TEXT,
DESCRIPCION_USUARIO TEXT, 
NOMBRE_COMPLETO TEXT, 
EDAD INTEGER, 
FOTO_PERFIL TEXT,
ROL TEXT
)
'''

sql_tabla_usuarios_token = '''
CREATE TABLE USUARIOS_TOKENS(
NOMBRE_USUARIO TEXT PRIMARY KEY,
CORREO TEXT,
TOKEN_SECRET TEXT
)
'''

sql_tabla_noticias = '''
CREATE TABLE NOTICIAS(
NOTICIA_ID INTEGER PRIMARY KEY AUTOINCREMENT, 
TITULO TEXT NOT NULL, 
DESCRIPCION TEXT NOT NULL, 
IMAGEN TEXT, 
FECHA_HORA TEXT NOT NULL
)
'''

sql_tabla_comentarios_noticia = '''
CREATE TABLE COMENTARIOS_NOTICIA(
COMENTARIO_ID TEXT PRIMARY KEY, 
NOMBRE_USUARIO TEXT NOT NULL, 
FECHA_HORA TEXT NOT NULL, 
DESCRIPCION_COMENTARIO TEXT NOT NULL, 
FOTO_PERFIL TEXT NOT NULL,
ID_NOTICIA INTEGER NOT NULL,
FOREIGN KEY(ID_NOTICIA) REFERENCES NOTICIAS(NOTICIA_ID)
)
'''

sql_tabla_posts = '''
CREATE TABLE POSTS(
POST_ID INTEGER PRIMARY KEY AUTOINCREMENT, 
TITULO_POST TEXT NOT NULL, 
DESCRIPCION TEXT NOT NULL,
FECHA_HORA TEXT NOT NULL,
NOMBRE_USUARIO TEXT NOT NULL,
FOTO_PERFIL TEXT,
VISTAS INTEGER
)
'''

sql_tabla_comentarios_post = '''
CREATE TABLE COMENTARIOS_POST(
COMENTARIO_POST_ID TEXT PRIMARY KEY, 
NOMBRE_USUARIO TEXT NOT NULL, 
DESCRIPCION_COMENTARIO TEXT NOT NULL, 
FECHA_HORA TEXT NOT NULL, 
FOTO_PERFIL TEXT,
ID_POST INTEGER NOT NULL
)
'''

sql_tabla_roles_list = '''
CREATE TABLE ROLES_LIST(
ID INTEGER, NICK TEXT, 
FOREIGN KEY(ID) REFERENCES ROLES(VISITANTE_ID), 
FOREIGN KEY(NICK) REFERENCES USUARIOS(NOMBRE_USUARIO)
)
'''

sql_tabla_users_coments_noticias = '''
CREATE TABLE USERS_COMENTS_NOTICIAS(
LISTA_USER TEXT, 
NUMERO_NOTICIA INTEGER, 
NUMERO_COMENT INTEGER, 
FOREIGN KEY(LISTA_USER) REFERENCES USUARIOS(NOMBRE_USUARIO), 
FOREIGN KEY(NUMERO_NOTICIA) REFERENCES NOTICIAS(NOTICIA_ID), 
FOREIGN KEY(NUMERO_COMENT) REFERENCES COMENTARIOS_NOTICIA(COMENTARIO_ID)
)
'''

sql_tabla_users_coments_posts = '''
CREATE TABLE USERS_COMENTS_POSTS(
LISTA_USER TEXT, 
NUMERO_POST INTEGER, 
NUMERO_COMENT INTEGER, 
FOREIGN KEY(LISTA_USER) REFERENCES USUARIO(NOMBRE_USUARIO), 
FOREIGN KEY(NUMERO_POST) REFERENCES POST(POST_ID), 
FOREIGN KEY(NUMERO_COMENT) REFERENCES COMENTARIOS_POST(COMENTARIO_POST_ID)
)
'''

if __name__ == '__main__':
    try:
        print('Creando Base de datos..')
        conexion = sqlite3.connect('plataforma.db')

        print('Creando Tablas..')
        conexion.execute(sql_tabla_roles)
        conexion.execute(sql_tabla_usuarios)
        conexion.execute(sql_tabla_usuarios_token)
        conexion.execute(sql_tabla_noticias)
        conexion.execute(sql_tabla_comentarios_noticia)
        conexion.execute(sql_tabla_posts)
        conexion.execute(sql_tabla_comentarios_post)
        conexion.execute(sql_tabla_roles_list)
        conexion.execute(sql_tabla_users_coments_noticias)
        conexion.execute(sql_tabla_users_coments_posts)

        conexion.close()
        print('Creacion Finalizada.')
    except Exception as e:
        print(f'Error creando base de datos: {e}', e)
