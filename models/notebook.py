from re import L
from database import database as db


class NotebookModel(db.Model):
    __tablename__ = "notebooks"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __init__(self, name, status, user_id):
        self.name = name
        self.status = status
        self.user_id = user_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.remove(self)
        db.session.commit()

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "user_id": self.user_id
        }

    def update_status(self, status):
        self.status = status
        self.save()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def is_in_terminal_state(self):
        return self.status in ["Failed", "InService", "Stopped"]