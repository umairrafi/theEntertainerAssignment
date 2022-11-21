from flask import Flask
from flask_marshmallow import Marshmallow
from flask_restful import reqparse, abort, Api, Resource
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from encryption import real_encrypt

app = Flask(__name__)
api = Api(app)
ma = Marshmallow(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

# basic auth used static username and password credentials
auth = HTTPBasicAuth()
USER_DATA = {
    "admin": "theEntertainer"
}


@auth.verify_password
def verify(username, password):
    """
    Basic Authentication function
    check user and password are valid
    """
    if not (username and password):
        return False
    return USER_DATA.get(username) == password


class TodoSchema(ma.Schema):
    """
    A class to convert complex datatype , object to and from python datatypes.
    """

    class Meta:
        fields = ('id', 'task', 'description', 'status')


todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)


# sqlite database model
class TodoModel(db.Model):
    """
    A class to represent a TodoModel.

    Attributes:
    -------
    id : integer,
    task : string,
    description : string,
    status : string
    """
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(200), nullable=False)


with app.app_context():
    db.create_all()

todo_put_args = reqparse.RequestParser()
todo_put_args.add_argument("task", type=str,
                           help="Name of the task is required",
                           required=True)
todo_put_args.add_argument("description", type=str,
                           help="Description of the task",
                           required=True)
todo_put_args.add_argument("status", type=str,
                           help="Status of the task",
                           required=True)

todo_update_args = reqparse.RequestParser()
todo_update_args.add_argument("task", type=str,
                              help="Name of the task is required")
todo_update_args.add_argument("description", type=str,
                              help="Description of the task")
todo_update_args.add_argument("status", type=str,
                              help="Status of the task")


# shows a singletodo item, update,delete and post atodo item
class Todo(Resource):
    """
    A class to represent atodo and contain its method.

    Methods
    -------
    get, post, put and delete:
        perform complete crud functionality
    """

    @auth.login_required
    def get(self, todo_id):
        """
        function to perform get call
        require(int) : task id
        return encrypted string
        """
        result = TodoModel.query.filter_by(id=todo_id).first()
        if not result:
            abort(404, message=f"Could not find task with id {todo_id}")
        result = todo_schema.dump(result)
        enc_to = real_encrypt(result)
        return enc_to

    @auth.login_required
    def delete(self, todo_id):
        """
        function to perform delete call
        require(int) : task id
        return acknowledgement string
        """
        todo = TodoModel.query.filter_by(id=todo_id).first()
        if not todo:
            abort(404, message=f"Could not find task with id {todo_id}")
        db.session.delete(todo)
        db.session.commit()
        return '', 204

    @auth.login_required
    def put(self, todo_id):
        """
        function to perform update call
        require(int) : task id
        require(str) : body contain any or all of(task, description, status)
        return encrypted string
        """
        args = todo_update_args.parse_args()
        result = TodoModel.query.filter_by(id=todo_id).first()
        if not result:
            abort(
                404, message=f"Can't update,Task with id {todo_id} does not exist")
        if args['task']:
            result.task = args['task']
        if args['description']:
            result.description = args['description']
        if args['status']:
            result.status = args['status']
        db.session.commit()
        result = todo_schema.dump(result)
        enc_to = real_encrypt(result)
        return enc_to

    @auth.login_required
    def post(self, todo_id):
        """
        function to perform post call
        require(int) : task id
        require : body contain all of(task, description, status)
        return encrypted string
        """
        args = todo_put_args.parse_args()
        result = TodoModel.query.filter_by(id=todo_id).first()
        if result:
            abort(409, message=f"Task id {todo_id} already taken")
        todo = TodoModel(
            id=todo_id,
            task=args['task'],
            description=args['description'],
            status=args['status'])
        db.session.add(todo)
        db.session.commit()
        result = todo_schema.dump(todo)
        enc_to = real_encrypt(result)
        return enc_to, 201


# shows a list of all todos
class TodoList(Resource):
    """
    A class to represent a todolist and contain its method.

    Methods
    -------
    get:
        performs query on database table and return encrypted data
    """

    @auth.login_required
    def get(self):
        """
        function to get list of tasks
        return encrypted string
        """
        tasks = TodoModel.query.order_by(TodoModel.id).all()
        if not tasks:
            abort(404, message=f"Currently, No task exists.")
        todos = todos_schema.dump(tasks)
        enc_to = real_encrypt(todos)
        return enc_to


# Actually set up the Api resource routing here
api.add_resource(TodoList, '/todos', '/')
api.add_resource(Todo, '/todos/<todo_id>')

if __name__ == '__main__':
    app.run(debug=True)
