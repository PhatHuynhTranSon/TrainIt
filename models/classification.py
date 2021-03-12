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

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()