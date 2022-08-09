from datetime import datetime, timezone
from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute,
    UnicodeSetAttribute, UTCDateTimeAttribute, BooleanAttribute
)


from dynamodb_handler import deleteTables


class Todo(Model):
    class Meta:
        table_name = "Todo"
        host = "http://localhost:8000"
        region="dummy"
        aws_access_key_id="dummy"
        aws_secret_access_key="dummy"
        write_capacity_units = 10
        read_capacity_units = 10

    id = UnicodeAttribute(hash_key=True)
    description = UnicodeAttribute(range_key=True, null=False)
    due_date = UTCDateTimeAttribute(default=datetime.now())
    completed = BooleanAttribute(default=False)

class User(Model):
    class Meta:
        table_name = "User"
        host = "http://localhost:8000"
        region="dummy"
        aws_access_key_id="dummy"
        aws_secret_access_key="dummy"
        write_capacity_units = 10
        read_capacity_units = 10


    id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute(range_key=True, null=False)
    password = UnicodeAttribute(null=False)
    deleteTables('User')
    
if not User.exists():
    User.create_table(wait=True)
    User(id=1, name="mahadi", password="password").save()
    User(id=1, name="test", password="test").save()

    deleteTables('Todo')
if not Todo.exists():
    Todo.create_table(wait=True)
    Todo(id=5, description='desc').save()
    Todo(id=4, description='desc').save()

