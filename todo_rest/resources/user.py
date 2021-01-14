from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_refresh_token_required,
)
from werkzeug.security import safe_str_cmp


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("email", required=True, help="This field cannot be blank")
    parser.add_argument("password", required=True, help="This field cannot be blank")
    parser.add_argument("username", required=True, help="This field cannot be blank")

    def get(self, id):
        user = UserModel.find_by_id(id)
        if user:
            return user.json()
        return {"message": "User not found"}, 404

    def post(self):
        data = UserRegister.parser.parse_args()

        user = UserModel(data["email"], data["username"], data["password"])
        user.save_to_db()

        return {"message": "User successfuly created"}, 201


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", required=True, help="This field cannot be blank")
    parser.add_argument("password", required=True, help="This field cannot be blank")

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()

        user = UserModel.find_by_username(data["username"])
        if user and safe_str_cmp(user.password, data["password"]):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return {"message": "Invalid credentials"}, 401


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
