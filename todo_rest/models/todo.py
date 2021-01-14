from db import db


class TodoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo_desc = db.Column(db.String(500))
    is_completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user_model.id"))

    def __init__(self, todo_desc, user_id):
        self.todo_desc = todo_desc
        self.user_id = user_id

    def json(self):
        return {
            "id": self.id,
            "todo_desc": self.todo_desc,
            "is_completed": self.is_completed,
            "user_id": self.user_id,
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id_):
        return cls.query.filter_by(id=id_)

    @classmethod
    def get_todos_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id)
