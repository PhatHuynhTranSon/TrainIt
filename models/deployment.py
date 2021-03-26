from database import database as db


class DeploymentModel(db.Model):
    __tablename__ = "deployments"
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    endpoint_name = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(255), default="Creating")

    def __init__(self, project_id, endpoint_name):
        self.project_id = project_id
        self.endpoint_name = endpoint_name
        self.status = "Creating"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "endpoint_name": self.endpoint_name,
            "status": self.status
        }

    def update_status(self, status):
        self.status = status
        self.save()

    @classmethod
    def find_by_project_id(cls, project_id):
        return cls.query.filter_by(project_id=project_id).first()

    @classmethod
    def if_a_deployment_exist(cls, project_id):
        return cls.query.filter_by(project_id=project_id).first() != None

    