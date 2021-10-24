from flask import Flask, request, redirect, url_for
from flask import render_template, flash
from werkzeug.datastructures import ContentSecurityPolicy
from werkzeug.wrappers import response 
from werkzeug.utils import secure_filename
import os

from servicesApp import services



UPLOAD_FOLDER = './static/img/img_web'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS





@app.route('/noticia/image',methods=["POST"])
def image_new():
    print(request.url)
    #print(request.form.to_dict())
    info = request.form.to_dict()
    if request.method == "POST":
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            if info['title'] == "" or info['description'] == "" or filename == "":
                return redirect(url_for('create_new'))
            else:
                res = services.create_news(info['title'],info['description'],filename)
                id = res['response']['newArticle']['id']
                return redirect(url_for('get_new',id=id))
        else:
            return redirect(url_for('create_new'))



@app.route('/actualizar/perfil',methods=["POST"])
def profile_update():
    print(request.method)
    print(request.form.to_dict())
    info = request.form.to_dict()
    if request.method == "POST":
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            if info['description'] == "" or info['full_name'] == "" or info['age'] == "":
                return redirect(url_for("profile",user_name=info['user_name']))
            else:
                res = services.update_user(info['user_name'],info['description'],info['full_name'],info['age'],filename)
                return redirect(url_for("profile",user_name=info['user_name']))
        else:
            res = services.update_user(info['user_name'],info['description'],info['full_name'],info['age'],"user_default.png")
            return redirect(url_for("profile",user_name=info['user_name']))
            
            



@app.route('/',methods=["GET"])
def home_page():
    return render_template('index.html')

@app.route('/home',methods=["GET"])
def home():
    return render_template('index.html')


@app.route('/usuario/registro',methods=["GET"])
def registro():
    return render_template('registro_user.html')

@app.route('/usuario/login',methods=["GET"])
def login():
    return render_template('login.html')


@app.route('/usuario/perfil/<string:user_name>',methods=["GET"])
def profile(user_name):
    return render_template('profile.html',user=user_name)


@app.route('/noticias',methods=["GET"])
def get_news():
    return render_template('news.html')



@app.route('/noticia/crear',methods=["GET"])
def create_new():
    return render_template('create_new.html')





@app.route('/noticia/<int:id>',methods=["GET"])
def get_new(id):
    return render_template('new.html',id_new= id)

@app.route('/foro',methods=["GET"])
def forum():
    return render_template('forum.html')


@app.route('/foro/post/crear',methods=["GET"])
def create_post():
    return render_template('create_post.html')



@app.route('/foro/post/<int:id>',methods=["GET"])
def get_post(id):
    return render_template('post.html',id_post= id)




if __name__ == '__main__':
    app.run(debug=True, port="5002")