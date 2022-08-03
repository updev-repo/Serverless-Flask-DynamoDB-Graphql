import graphene
from flask_graphql import GraphQLView
from app.query import UserQuery
from app.types.user import User
from app.mutations.user import UserMutations 

schema = graphene.Schema(query=UserQuery, types=[User], mutation=UserMutations)

graphview = GraphQLView.as_view("users", schema=schema, graphiql=True)

__all__ = ["graphview"]