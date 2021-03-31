from flask import Flask, jsonify, request
from flask_mongoengine import MongoEngine
from database.database import initialize_db
from database.models import User,Task
from flask_restful import Api
from api.routes import initialize_routes

app = Flask(__name__)
api = Api(app)

app.config['MONGODB_SETTINGS'] = {
    'db': 'todo',
    'host': 'mongodb://localhost/todo',
    'port': 27017
}

initialize_db(app)
initialize_routes(api)

if __name__ == "__main__":
    app.run(debug=True)