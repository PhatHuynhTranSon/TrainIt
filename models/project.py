from database import database as db
from uuid import uuid4


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    location_name = db.Column(db.String(255)) # This denotes the project location name in s3 bucket
    description = db.Column(db.String(255))
    type = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __init__(self, name, description, type, user_id):
        self.name = name
        self.description = description
        self.type = type
        self.user_id = user_id
        self.generate_location_name()

    def generate_location_name(self):
        # Generate a unique uuid string
        self.location_name = uuid4().hex

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def belongs_to_user(self, user_id):
        return self.user_id == user_id

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "location_name": self.location_name,
            "description": self.description,
            "type": self.type
        }

    @classmethod
    def find_project_with_id(cls, project_id):
        return cls.query.filter_by(id=project_id).first()

    @classmethod 
    def find_project_from_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    def is_classification_problem(self):
        return self.type == "classification"

    def is_regression_problem(self):
        return self.type == "regression"