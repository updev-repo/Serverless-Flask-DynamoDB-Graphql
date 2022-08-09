from graphene.test import Client
from dynamodb_handler import deleteTables
from main import schema
from db import User

# Delete existing tables and create one anew
deleteTables('Todo')
if not User.exists():
    User.create_table(wait=True)
    User(id=1, name="mahadi", password="password").save()
    User(id=1, name="test", password="test").save()

client = Client(schema)

def test_create_user():
    executed = client.execute('''
    mutation createUser {
        createUser(id:4, name:"dev",password:"dev"){
            user{
            name
            password
            }
        }   
    }
    
   ''' )
    assert executed == {
        "data": {
            "createUser": {
            "user": {
                "name": "dev",
                "password": "dev"
            }
            }
        }
        }

def test_fetch_user():
    executed = client.execute('''
        query GetUser {
            usersSingle(input:4) {
                id
                name
                }
            }
    ''')
    assert executed != {
  "errors": [
    {
      "message": "Invalid username",
      "locations": [
        {
          "line": 30,
          "column": 3
        }
      ],
      "path": [
        "usersSingle"
      ]
    }
  ],
  "data": {
    "usersSingle": None
  }
}
    assert executed == {
        "data": {
            "usersSingle": {
            "id": "VXNlclR5cGU6NA==",
            "name": "dev"
            }
            }
        }

# Pass User_Login test
def test_login_user_pass():
    executed = client.execute('''
        mutation loginAuth {
            auth(name: "test", password: "test") {
                accessToken
                refreshToken
            }
        }

    ''')

    assert executed != {
        "data": {
            "auth": None
        }
        }

#Fail user login test since This user does not exist
def test_login_user_fail():
    executed = client.execute('''
        mutation loginAuth {
            auth(name: "Username", password: "password") {
                accessToken
                refreshToken
            }
        }

    ''')
    print(executed)
    assert executed == {
        "data": {
            "auth": None
        }
        }

