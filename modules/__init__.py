import os

import dotenv
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

dotenv.load_dotenv()

db_host = os.getenv("host")
db_user = os.getenv("user")
db_pass = os.getenv("passwd")
db_name = os.getenv("db")

secret_key = os.getenv("secret_key")

app.config['SECRET_KEY'] = secret_key

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{db_user}:{db_pass}@{db_host}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager()
login_manager.init_app(app)

db = SQLAlchemy(app)
