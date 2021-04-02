from models.user import UserModel
from models.payment import PaymentModel
from paypal import create_paypal_handler
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity


class PaymentResource(Resource):
    def __init__(self):
        self.create_argument_parser()
        self.create_paypal_handler()

    def create_argument_parser(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "orderId",
            type=str,
            required=True,
            help="Order id is required"
        )

    def create_paypal_handler(self):
        self.paypal_handler = create_paypal_handler()

    def parse_args(self):
        return self.parser.parse_args()

    @jwt_required()
    def get(self):
        # Get user id
        user_id = get_jwt_identity()
        user = UserModel.find_user_with_id(user_id)

        return {
            "tokens": user.tokens
        }

    @jwt_required()
    def post(self):
        # Get user id
        user_id = get_jwt_identity()
        user = UserModel.find_user_with_id(user_id)

        # Get the order id from request
        arguments = self.parse_args()
        order_id = arguments["orderId"]

        # Capture the order
        response = self.paypal_handler.capture_order(order_id)
        token_id = response["reference_id"]

        # Check if status is completed
        if self.paypal_handler.is_completed(response):
            # Get the token pack with id
            token_pack = PaymentModel.find_by_id(token_id)
            # Increase user's token
            tokens = token_pack.amount
            user.increase_tokens(tokens)
        else:
            return {
                "message": "Purchase is not completed"
            }, 500

        # Respond with captured data
        return {
            "message": "Successfully purchased more tokens"
        }
