from os import access
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token

from models.user import UserModel

class UserSignupResource(Resource):
    def __init__(self):
        self.create_argument_parser()

    def create_argument_parser(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "username",
            type=str,
            required=True,
            help="Username must be provided"
        )
        self.parser.add_argument(
            "email",
            type=str,
            required=True,
            help="Email must be provided"
        )
        self.parser.add_argument(
            "password",
            type=str,
            required=True,
            help="Password must be provided"
        )

    def post(self):
        username, email, password = self.parse_arguments()

        # Check if user has not already registered
        if UserModel.find_user_with_email(email):
            return {
                "message": "Email already existed"
            }, 400

        # Create user
        user = UserModel(username=username, email=email, password=password)
        user.save()

        # Repond with successful message
        return {
            "message": "User created successfuly"
        }, 201

    def parse_arguments(self):
        args = self.parser.parse_args()
        return args["username"], args["email"], args["password"]


class UserSigninResource(Resource):
    def __init__(self):
        self.create_argument_parser()

    def create_argument_parser(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "email",
            type=str,
            required=True,
            help="Email must be provided"
        )
        self.parser.add_argument(
            "password",
            type=str,
            required=True,
            help="Password must be provided"
        )

    def post(self):
        email, password = self.parse_arguments()

        # Find user with same email
        user_with_same_email = UserModel.find_user_with_email(email)
        if not user_with_same_email or not user_with_same_email.check_password(password):
            return {
                "message": "Invalid email/password combination"
            }, 400

        # Get the token
        access_token = create_access_token(identity=user_with_same_email.id)
        refresh_token = create_refresh_token(identity=user_with_same_email.id)

        # Repond with 'successfully' message
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }, 200

    def parse_arguments(self):
        args = self.parser.parse_args()
        return args["email"], args["password"]
