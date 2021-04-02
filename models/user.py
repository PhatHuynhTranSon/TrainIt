from database import database as db
from sqlalchemy.ext.hybrid import hybrid_property
from hashing import bcrypt


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    tokens = db.Column(db.Integer, default=0)
    _password = db.Column(db.String(255), nullable=False)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext).decode('utf-8')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def increase_tokens(self, tokens):
        self.tokens += tokens;
        self.save()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def check_password(self, plaintext):
        return bcrypt.check_password_hash(self._password, plaintext)

    def json(self):
        return {
            "email": self.email,
            "username": self.username,
            "tokens": self.tokens
        }

    @classmethod
    def find_user_with_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()

    @classmethod
    def find_user_with_email(cls, email):
        return cls.query.filter_by(email=email).first()