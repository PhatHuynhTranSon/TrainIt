from database import database as db


class DeploymentModel(db.Model):
    __tablename__ = "deployments"
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    endpoint_name = db.Column(db.String, nullable=False)
    status = db.Column(db.String, default="Creating")

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_project_id(cls, project_id):
        return cls.query.filter_by(project_id=project_id).first()