import os
import re

from app.controller import create_user, get_user, all_user_list
from flask_graphql import GraphQLView
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

# @app.route("/users", methods=["POST"])
# def post_user():
#     user_id = request.json.get('userId')
#     name = request.json.get('name')
#     email = request.json.get('email')
#     res = create_user(user_id, name, email)
#     return res

# @app.route("/users", methods=["GET"])
# def list_user():
#     res = all_user_list()
#     return res

# @app.route("/users/<string:user_id>")
# def get_user_item(user_id):
#     item = get_user(user_id)
#     if not item:
#         return jsonify({'error': 'User does not exist'}), 404
#     return item

if __name__ == '__main__':
   app.run(debug = True)