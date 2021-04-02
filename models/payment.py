from database import database as db


class PaymentModel(db.Model):
    __tablename__ = "payments"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Integer, nullable=False)

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()