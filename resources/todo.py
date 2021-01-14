from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.todo import TodoModel


class TodoResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "todo_desc", required=True, type=str, help="This field cannot be blank"
    )

    @jwt_required
    def post(self):
        data = TodoResource.parser.parse_args()

        user_id = get_jwt_identity()
        todo = TodoModel(data["todo_desc"], user_id)
        todo.save_to_db()

        return {"message": "Todo created successfully"}, 201


class UserTodo(Resource):
    @jwt_required
    def post(self):
        user_id = get_jwt_identity()

        if user_id:
            todos = TodoModel.get_todos_by_user_id(user_id)
            if todos:
                return {"todos": [todo.json() for todo in todos.all()]}
            return {"message": "Todo not found"}, 404

        return {"message": "Invalid credentials"}
