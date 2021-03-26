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
        solutions = cls.query.filter_by(project_id=project_id).all()
        return cls.map_solution_to_solution_id(solutions)

    @classmethod
    def find_best_solution_of_project(cls, project_id):
        best_solution = cls.query.filter_by(project_id=project_id).filter(cls.test_mse != None).order_by(cls.test_mse.desc()).first()
        return best_solution

    def if_belongs_to(self, project_id):
        return self.project_id == project_id

    def analytics_filled(self):
        return self.train_mse != None

    def update_analytics(self, analytics):
        self.train_mse = analytics["train:mse"]
        self.test_mse = analytics["test:mse"]
        self.save()