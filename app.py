from flask import Flask
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager
from db import db
from resources.user import UserRegister, UserLogin, TokenRefresh
from resources.todo import TodoResource, UserTodo

app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["JWT_SECRET_KEY"] = "abhi"
app.secret_key = "abhilash"


@app.before_first_request
def create_tables():
    db.create_all()


# api.add_resource(UserResource, "/user/<int:id>")
# api.add_resource(TodoResource, "/todo/<int:id>")
api.add_resource(UserRegister, "/user", methods=["POST"])
api.add_resource(UserLogin, "/login", methods=["POST"])
api.add_resource(TodoResource, "/todo", methods=["POST"])
api.add_resource(UserTodo, "/todos", methods=["POST"])
api.add_resource(TokenRefresh, "/refresh")

if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True)
