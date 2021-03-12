from database import database as db


class RegressionProblem(db.Model):
    _tablename_ = "regressions"

    id = db.Column(db.Integer, primary_key=True)
    job_name = db.Column(db.String(255))
    algorithm_name = db.Column(db.String(255))

    train_mse = db.Column(db.Float)
    test_mse = db.Column(db.Float)

    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    project = db.relationship("Project")

    def __init__(self, job_name, algorithm_name, project_id):
        self.job_name = job_name
        self.algorithm_name = algorithm_name
        self.project_id = project_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {
            "id": self.id,
            "job_name": self.job_name,
            "algorithm_name": self.algorithm_name,
            "train_mse": self.train_mse,
            "test_mse": self.test_mse,
            "project_id": self.project_id
        }