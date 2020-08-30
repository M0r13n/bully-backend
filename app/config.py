import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

dotenv_path = os.path.join(os.path.dirname(__file__), '../../.local_env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

ENV = os.getenv("FLASK_ENV")
DEBUG = ENV == "development"
SECRET_KEY = os.getenv("SECRET_KEY", 'my-precious')

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///database.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False
