import graphene
from graphene import relay
from app.user_model import UserModel
from app.types.user import User

class UserQuery(graphene.ObjectType):
   node = relay.Node.Field()

   users = graphene.List(lambda: UserModel, id=graphene.String())

   def resolve_users(self, info, id=None):
       if id:
           return UserModel.get(id=id)
       return list(UserModel.scan())