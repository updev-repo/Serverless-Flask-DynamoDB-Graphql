from graphene import ObjectType,relay
from app.user_model import UserModel

class User(ObjectType):
    class Meta:
        model = UserModel
        Interface = (relay.Node,)