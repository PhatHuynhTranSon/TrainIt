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

    @classmethod
    def map_solution_to_solution_id(cls, solutions):
        return [
            solution.id for solution in solutions
        ]

    @classmethod
    def find_solution_with_id(cls, solution_id):
        return cls.query.filter_by(id=solution_id).first()

    @classmethod
    def find_solutions_of_project(cls, project_id):
        solutions = cls.query.filter_by(project_id=project_id).order_by(ClassficationProblem.id.desc()).all()
        return cls.map_solution_to_solution_id(solutions)

    @classmethod
    def find_best_solution_of_project(cls, project_id):
        best_solution = cls.query.filter_by(project_id=project_id).filter(cls.test_accuracy != None).order_by(cls.test_accuracy.desc()).first()
        return best_solution

    def if_belongs_to(self, project_id):
        return self.project_id == project_id

    def analytics_filled(self):
        return self.train_accuracy != None

    def update_analytics(self, analytics):
        self.train_accuracy = analytics["train:accuracy"]
        self.test_accuracy = analytics["test:accuracy"]
        self.train_f1 = analytics["train:f1"]
        self.test_f1 = analytics["test:f1"]
        self.save()