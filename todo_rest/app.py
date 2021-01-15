from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager
from db import db
from resources.user import UserRegister, UserLogin, UserLogout, TokenRefresh
from resources.todo import TodoResource, UserTodo
from blacklist import BLACKLIST

app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["JWT_SECRET_KEY"] = "abhi"
app.secret_key = "abhilash"
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]


@app.before_first_request
def create_tables():
    db.create_all()


# When a token is expired this is what will be returned
@jwt.expired_token_loader
def expired_token_loader():
    return (
        jsonify({"description": "The token has expired", "error": "token_expired"}),
        401,
    )


# Marks the jwt to be invalid, a way to logout an user
@jwt.revoked_token_loader
def logout():
    return (
        jsonify({"description": "The token has been revoked", "error": "token_revoked"})
    ), 401


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


# api.add_resource(UserResource, "/user/<int:id>")
# api.add_resource(TodoResource, "/todo/<int:id>")
api.add_resource(UserRegister, "/user", methods=["POST"])
api.add_resource(UserLogin, "/login", methods=["POST"])
api.add_resource(UserLogout, "/logout", methods=["POST"])
api.add_resource(TodoResource, "/todo", methods=["POST"])
api.add_resource(UserTodo, "/todos", methods=["POST"])
api.add_resource(TokenRefresh, "/refresh")

if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True)
