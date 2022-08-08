from flask import Flask
from flask_graphql import GraphQLView
import graphene
from app.query import UserQuery
from app.mutations import UserMutations

# graphview = GraphQLView.as_view("graphql", schema=schema, type=[UserType] , graphiql=True)
schema = graphene.Schema(query=UserQuery, mutation=UserMutations)


class Config:
    SECRET_KEY = 'Test Secret Key'


def create_app(**kwargs):
    app = Flask(__name__)
    app.debug = True
    app.config.from_object(Config)
    app.add_url_rule(
        '/graphql', view_func=GraphQLView.as_view("graphql", schema=schema, **kwargs)
    )
    return app


app = create_app(graphiql=True)

__all__ = ("app",)