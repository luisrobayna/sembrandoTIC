from flask import Flask

from routes.auth import routes_auth
from routes.user_route import routes_user
from routes.news_route import routes_news
from routes.comentNew import routes_comment_news
from routes.forum import routes_forum
from routes.comentForum import routes_comment_forum
from flask_cors import CORS

from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

app.register_blueprint(routes_auth, url_prefix="/api")
app.register_blueprint(routes_user, url_prefix="/api")
app.register_blueprint(routes_news, url_prefix="/api")
app.register_blueprint(routes_comment_news, url_prefix="/api")
app.register_blueprint(routes_forum, url_prefix="/api")
app.register_blueprint(routes_comment_forum, url_prefix="/api")


if __name__=='__main__':
    load_dotenv()
    app.run(debug=True, port="5001")