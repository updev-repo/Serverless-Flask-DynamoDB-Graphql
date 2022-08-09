from flask import Flask
from flask_graphql import GraphQL
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask (__name__)
app.secret_key = "default"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.getcwd()}/todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
