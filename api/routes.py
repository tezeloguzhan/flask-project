from .todo import Task, Tasks

def initialize_routes(api):
    api.add_resource(Tasks, '/api/tasks/')
    api.add_resource(Task, '/api/tasks/<id>/')