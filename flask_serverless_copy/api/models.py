from email.policy import default
from main import db
from datetime import datetime

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    completed = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.Date, default=datetime.now())

    def serialize(self):
        return {
            "id": self.id,
            "completed": self.completed,
            "description": self.description,
            "due_date": str(self.due_date.strftime('%d-%m-%Y'))
        }


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), unique=True)
    password = db.Column(db.String(500))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password
        }
