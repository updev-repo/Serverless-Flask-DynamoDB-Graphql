import graphene
from app.types.user import User
from app.user_model import UserModel

class UserMutations(graphene.Mutation):
   class Arguments:
       id = graphene.String(required=True)
       name = graphene.String(required=True)
       email = graphene.String(required=True)

   user = graphene.Field(lambda: User)

   def mutate(self, info, id, name, email):
       user = UserModel(id=id, name=name, email=email)
       user.save()
       
       return UserMutations(user=user)