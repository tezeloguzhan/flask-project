#Genel İşlemler
from flask import Flask, jsonify,request,make_response
from flask_mongoengine import MongoEngine
from database.models import Users,Task
#Özel Error
from api.errors import unauthorized
#Güvenlik
from constants import database_name,database_password
import datetime
#JWT İŞLEMLERİ
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


app = Flask(__name__)
DB_URL="mongodb+srv://oguzhan:{}@cluster0.nupmm.mongodb.net/{}?retryWrites=true&w=majority".format(database_password,database_name)#constants.py dosyası açıp bilgilerinizi giriniz
app.config['MONGODB_HOST'] = DB_URL

db=MongoEngine()
db.init_app(app)

app.config["JWT_SECRET_KEY"] = "super-secret"  #Test için default değer , ürüne çıkıldığında özel key üretiniz. 
jwt = JWTManager(app)

#Database için örnek data
@app.route('/api/example_data',methods=["POST"])
def example_data():
    task1=Task(task_id=1,title="Konu 1",text="Açıklama 1",is_done="True")
    task2=Task(task_id=2,title="Konu 2",text="Açıklama 2",is_done="False")
    task3=Task(task_id=3,title="Konu 3",text="Açıklama 3",is_done="True")
    new_user = Users(name="oguzhan",email="tezeloguzhann@gmail.com", password="123456", access={"admin": True})
    new_user.save()
    task1.save()
    task2.save()
    task3.save()
    return make_response('',201)

#####################################
########CRUD İŞLEMLERİ###############
#####################################

#task post ve get işlemleri
@app.route('/api/tasks',methods=["POST","GET"])
@jwt_required()
def tasks():
    if request.method=="POST":
        
        task=Task(
            task_id=request.json['task_id'],
            title=request.json['title'],
            text=request.json['text'],
            is_done=request.json['is_done']
        )
        task.save()
        return make_response('',201) #Created Response 
        
    elif request.method=="GET":
        datas=Task.objects()
        return make_response(jsonify(datas),200)

#ID'ye göre güncelleme,silme ,görüntüleme işlemleri       
@app.route('/api/tasks/<task_id>',methods=["GET","PUT"])
@jwt_required()
def single_task(task_id):
    if request.method=="GET":
        each_task=Task.objects(task_id=task_id).first()
        if each_task:
            return make_response(jsonify(each_task),200)
        else:
            return make_response("",404)
    elif request.method=="PUT":
        each_task=Task.objects(task_id=task_id).first()
        each_task.update(
            title=request.json['title'],
            text=request.json['text'],
            is_done=request.json['is_done'])
        return make_response("",204)
   
#Sadece Admin Silebilir.
@app.route('/api/tasks/<task_id>',methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    authorized: bool = Users.objects.get(id=get_jwt_identity()).access.admin
    if authorized:
        each_task=Task.objects(task_id=task_id).first()
        each_task.delete()
        return make_response("Task Silindi.",200)

    else:
        return make_response("Sadece Adminler Silebilir.",404)



#####################################
########Kullanıcı İşlemleri##########
#####################################

@app.route('/api/signup',methods=["POST"])
def signup():
    
    user=Users(
            name=request.json['name'],
            email=request.json['email'],
            password=request.json['password'],
            access=request.json['access']
            )
    user.save()

    output = {'id': str(user.id)}
    return jsonify({'result': output})

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    user = Users.objects.get(email=data.get('email'))
    auth_success = user.check_pw_hash(data.get('password'))
    
    if not auth_success:
            return unauthorized()
    else:
            expiry = datetime.timedelta(days=5)
            access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
            refresh_token = create_refresh_token(identity=str(user.id))
            return jsonify({'result': {'access_token': access_token,
                                       'refresh_token': refresh_token,
                                       'logged_in_as': f"{user.email}"}})


if __name__ == "__main__":
    app.run(debug=True)