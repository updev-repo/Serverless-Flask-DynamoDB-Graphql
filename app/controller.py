from app.user_model import UserModel
from flask import jsonify
import json

def create_user(user_id, name, email): 
    if not user_id or not name or not email:
        return jsonify({'error': 'Please provide a vaule of all fields'}), 400
    try:
        a_user = UserModel(user_id=user_id, name=name, email=email)
        a_user.save()
        return {'statusCode': 201, 'message': 'success'}
    except Exception as inst: 
        return(inst)

def get_user(user_id): 
    if not user_id:
        return jsonify({'error': 'Please provide a user_id'}), 400
    try:
        user_item = UserModel.get(user_id)
        return json.dumps(user_item)
    except Exception as inst: 
        print(inst)
        
def all_user_list():
    user_item = UserModel().scan()
    print(user_item)