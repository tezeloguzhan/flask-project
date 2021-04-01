#Database Alanları
from mongoengine import (Document,
                         EmbeddedDocument,
                         EmbeddedDocumentField,
                         StringField,
                         EmailField,
                         BooleanField,
                         IntField)
                         
#Şifre Güvenlik
from flask_bcrypt import generate_password_hash, check_password_hash

#Kullanıcı Rolleri 
class Access(EmbeddedDocument):
    user = BooleanField(default=True)
    admin = BooleanField(default=False)
#Kullanıcı   
class Users(Document):
    name = StringField(unique=False)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True, min_length=6, regex=None)
    access = EmbeddedDocumentField(Access, default=Access(user=True, admin=False))

    #Şifre Hash
    def generate_pw_hash(self):
        self.password = generate_password_hash(password=self.password).decode('utf-8')
    generate_pw_hash.__doc__ = generate_password_hash.__doc__

    def check_pw_hash(self, password: str) -> bool:
        return check_password_hash(pw_hash=self.password, password=password)
    check_pw_hash.__doc__ = check_password_hash.__doc__

    #Kaydetmeden önce hashle
    def save(self, *args, **kwargs):
        if self._created:
            self.generate_pw_hash()
        super(Users, self).save(*args, **kwargs)
    
#Task
class Task(Document):
    task_id=IntField(primary_key=True)
    title=StringField(max_length=60)
    text =StringField(max_length=150)
    is_done =BooleanField(default=False)

    def to_json(self):
        return{
            "task_id":self.task_id,
            "title":self.title,
            "text":self.text,
            "is_done":self.is_done
        }
    
    
