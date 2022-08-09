from graphene.test import Client
from dynamodb_handler import deleteTables
from main import schema

from db import Todo
client = Client(schema)

# Delete existing tables and create one anew
deleteTables('Todo')
if not Todo.exists():
    Todo.create_table(wait=True)
    Todo(id=5, description='desc').save()
    Todo(id=4, description='desc').save()


def test_todo_query():
    executed = client.execute('''
        query GetTodo {
            todoSingle(input:5) {
                description
                completed
        }
        }
    ''')
    assert executed != {
  "errors": [
    {
      "message": "This Todo item does not exist.",
      "locations": [
        {
          "line": 20,
          "column": 3
        }
      ],
      "path": [
        "todoSingle"
      ]
    }
  ],
  "data": {
    "todoSingle": None
  }
}


    assert executed == {
  "data": {
    "todoSingle": {
      "description": "desc",
      "completed": False
    }
  }
}

def test_todo_update():
    executed = client.execute('''
        mutation updateTodo {
            updateTodo(id:5, description:"desc",completed:true){
                todo{
                description
                completed
                }
            }   
        }
    ''')

    assert executed == {
  "data": {
    "updateTodo": {
      "todo": {
        "description": "desc",
        "completed": True
      }
    }
  }
}

def test_todo_delete():
    executed = client.execute('''

        mutation deleteTodo {
            deleteTodo(id:5){
            todo{
            id
            }
        }
        }

    ''')
    assert executed == {
        "data": {
            "deleteTodo": {
            "todo": None
            }
        }
        }


def test_todo_create():
    executed = client.execute('''
    mutation createTodo {
        createTodo(id:5, description:"A new name",completed:true){
        todo{
        description
        completed
        }
    }   
    }
''')

    assert executed == {
        "data": {
            "createTodo": {
            "todo": {
                "description": "A new name",
                "completed": True
            }
            }
        }
        }
