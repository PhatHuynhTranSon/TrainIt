from database import database as db


class ClassficationProblem(db.Model):
    _tablename_ = "classifications"

    id = db.Column(db.Integer, primary_key=True)
    job_name = db.Column(db.String(255))
    algorithm_name = db.Column(db.String(255))

    train_accuracy = db.Column(db.Float)
    test_accuracy = db.Column(db.Float)
    train_f1 = db.Column(db.Float)
    test_f1 = db.Column(db.Float)

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
            "train_accuracy": self.train_accuracy,
            "test_accuracy": self.test_accuracy,
            "train_f1": self.train_f1,
            "test_f1": self.test_f1,
            "project_id": self.project_id
        }