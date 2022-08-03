import os

from pynamodb.attributes import UnicodeAttribute
from pynamodb.models import Model


class UserModel(Model):
    class Meta:
        table_name = os.environ['USERS_TABLE'] 
        host = 'http://localhost:8000' 
        
    id = UnicodeAttribute(range_key=True)
    name = UnicodeAttribute(null=False)
    email = UnicodeAttribute(null=False)