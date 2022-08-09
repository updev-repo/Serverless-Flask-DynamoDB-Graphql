from datetime import datetime
import graphene
import sqlalchemy
from flask import session
from flask_graphql_auth import (AuthInfoField, GraphQLAuth,
                                create_access_token, create_refresh_token,
                                get_jwt_identity,
                                mutation_jwt_refresh_token_required,
                                mutation_jwt_required,
                                query_header_jwt_required)
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from graphql import GraphQLError
from werkzeug.security import check_password_hash, generate_password_hash

from api import app, db
from api.models import Todo as TodoModel
from api.models import User as UserModel

auth = GraphQLAuth(app)

from graphene_pynamodb import PynamoObjectType
from db import Todo, User
import dynamodb_handler as ddh
class UserType(PynamoObjectType):
    class Meta:
        model = User
        interfaces = (relay.Node, )


class TodoType(PynamoObjectType):
    class Meta:
        model = Todo
        interfaces = (relay.Node, )

class Query(graphene.ObjectType):
    node = relay.Node.Field()
    
    # Get all Db users and todo
    all_users = graphene.List(UserType)
    all_todo = graphene.List(TodoType)

    
    def resolve_all_users(self, context, **kwargs):
        return list(User.scan())    

    def resolve_all_todo(self, context, **kwargs):
        if list(Todo.scan()):
        
            return list(Todo.scan())



    # Get Users and todo by query and then resolve
    users_single = graphene.Field(UserType, input=graphene.Int())
    todo_single = graphene.Field(TodoType, input=graphene.Int())

    def resolve_users_single(root, info, input):
        for item in User.scan(User.id == (input)):
                if item: 
                    return item
            
        return GraphQLError("Invalid username")

    def resolve_todo_single(root, info, input):
        for item in Todo.scan(Todo.id == (input)):
            if item: 
                return item
         
        return GraphQLError("This Todo item does not exist.")


class TodoMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        description = graphene.String(required=True)
        completed = graphene.Boolean()
        due_date = graphene.DateTime(default_value=datetime.now())

    todo = graphene.Field(TodoType)

    @classmethod
    def mutate(cls, root, info, id, description, completed, due_date):
        todo = Todo(id=id, description=description, completed=completed, due_date=due_date)
        todo.save()
        return TodoMutation(todo=todo)


class UpdateTodoMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        description = graphene.String(required=True)
        completed = graphene.Boolean()
        due_date = graphene.DateTime(default_value=datetime.now())

    todo = graphene.Field(TodoType)


    @classmethod
    def mutate(cls, root, info, id, description, completed, due_date):
        todo =  None
        for item in Todo.scan(Todo.id == id):
            if item: 
                todo = item
                print(todo)
        print(todo)
        todo.id = id
        todo.description = description
        todo.completed = completed
        todo.due_date = due_date
        todo.save()

        return UpdateTodoMutation(todo=todo)
        
class DeleteTodoMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
    todo = graphene.Field(TodoType)


    @classmethod
    def mutate(cls, root, info, id):
        for item in Todo.scan(Todo.id == id):
            if item: 
                return item.delete()
            print(item)    
        return GraphQLError("This Todo item does not exist.")


class UserMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(default_value=1)
        name = graphene.String()
        password = graphene.String()
        
    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, id, name, password):
        hashed_password = generate_password_hash(password) 
        try:    
            user = User(id=id, name=name, password=password, )
            user.save()
        except sqlalchemy.exc.IntegrityError:
            return GraphQLError("Name not available")

        return UserMutation(user=user)

class AuthMutation(graphene.Mutation):
    access_token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        name = graphene.String()
        password = graphene.String()
    
    def mutate(self, info , name, password):
        hashed_password = check_password_hash(password,password)
        for user in User.scan(User.name==name):
            if not user.name:
                return GraphQLError('Authenication Failure : User is not registered')
            else: 
                print(user.name, user.password)
                print(name, password)
                session['name'] = name
                session['id'] = user.id
                # return GraphQLError('Authenication Failure : User is not registered')
                return AuthMutation(
                    access_token = create_access_token(name),
                    refresh_token = create_refresh_token(name)
                )
                
class Mutation(graphene.ObjectType):
    create_todo = TodoMutation.Field()
    update_todo = UpdateTodoMutation.Field()
    delete_todo = DeleteTodoMutation.Field()
    create_user = UserMutation.Field()
    auth = AuthMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)


