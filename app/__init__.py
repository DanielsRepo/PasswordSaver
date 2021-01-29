from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config["DEBUG"] = os.environ["DEBUG"]
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
#     os.path.abspath(os.path.dirname(__file__)), "app.db"
# )

user = os.environ["POSTGRES_USER"]
pwd = os.environ["POSTGRES_PASSWORD"]
db_name = os.environ["POSTGRES_DB"]
host = os.environ["POSTGRES_HOST"]
port = os.environ["POSTGRES_PORT"]

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db_name}"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = "login"

from . import routes
