from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = "bvwnniusv"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///final_3"

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from shop import routes
from app import app
from routes import register, login, logout, add_item, items, user_items

