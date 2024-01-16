from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_babelex import Babel
from flask_login import LoginManager
app = Flask(__name__)
app.secret_key='wjfkkw81910491@1'
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:%s@localhost/private_clinics' % quote('123456')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app=app)
babel = Babel(app=app)
login_manager=LoginManager(app=app)
app.config['CART_KEY'] = 'cart'
@babel.localeselector
def get_locale():
    return "vi"