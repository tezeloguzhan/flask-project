from flask import Flask, jsonify, request,make_response,jsonify
from flask_mongoengine import MongoEngine
from database.models import User,Task
#Güvenlik
from api.constants import database_name,database_password

app = Flask(__name__)
DB_URL="mongodb+srv://oguzhan:{}@cluster0.nupmm.mongodb.net/{}?retryWrites=true&w=majority".format(database_password,database_password)
app.config['MONGODB_HOST'] = DB_URL

db=MongoEngine()
db.init_app(app)

#Database için örnek data
@app.route('/api/example_data',methods=["POST"])
def example_data():
    task1=Task(task_id=1,title="Konu 1",text="Açıklama 1",is_done="True")
    task2=Task(task_id=2,title="Konu 2",text="Açıklama 2",is_done="False")
    task3=Task(task_id=3,title="Konu 3",text="Açıklama 3",is_done="True")
    task1.save()
    task2.save()
    task3.save()
    return make_response('',201)

#task post ve get işlemleri
@app.route('/api/tasks',methods=["POST","GET"])
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
        tasks=[]
        for task in Task.objects:
            tasks.append(task)
            return make_response(jsonify(tasks),200)

#ID'ye göre güncelleme,silme ,görüntüleme işlemleri       
@app.route('/api/tasks/<task_id>',methods=["GET","PUT","DELETE"])
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
    elif request.method=="DELETE":
        each_task=Task.objects(task_id=task_id).first()
        each_task.delete()
        return make_response("",200)


if __name__ == "__main__":
    app.run(debug=True)