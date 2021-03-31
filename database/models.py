from .database import db
from passlib.apps import custom_app_context as pwd_context

class User(db.Document):
    id=db.IntField(primary_key=True)
    username=db.StringField(max_length=30)
    password=db.StringField(max_length=30)
    email=db.StringField(max_length=30)
    user_role=db.StringField()

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

class Task(db.Document):
    id=db.IntField(primary_key=True)
    title=db.StringField(max_length=60)
    text = db.StringField(max_length=150)
    is_done = db.BooleanField(default=False)

