from database import database as db


class RegressionProblem(db.Model):
    _tablename_ = "regressions"

    id = db.Column(db.Integer, primary_key=True)
    job_name = db.Column(db.String(255))
    algorithm_name = db.Column(db.String(255))

    train_mse = db.Column(db.Float)
    test_mse = db.Column(db.Float)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()