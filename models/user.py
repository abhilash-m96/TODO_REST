from db import db


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(70), unique=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(64))
    is_deleted = db.Column(db.Boolean, default=False)
    todos = db.relationship("TodoModel", backref="user", lazy="dynamic")

    def __init__(self, email, username, password):
        self.email = email
        self.password = password
        self.username = username

    def json(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "todos": [todo.json() for todo in self.todos.all()],
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
