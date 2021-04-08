import jwt
from notebook import NoteBookCreator, NoteBookStatus, NoteBookUrlCreator

from models.notebook import NotebookModel
from models.user import UserModel

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity


class NotebookListResource(Resource):
    def __init__(self):
        self.create_argument_parser()
    
    def create_argument_parser(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "name",
            type=str,
            required=True,
            help="Notebook name should not be empty"
        )

    def parse_args(self):
        return self.parser.parse_args()

    @jwt_required()
    def get(self):
        # Get user id
        user_id = get_jwt_identity()

        # Get all notebooks belonging to user
        notebooks = NotebookModel.find_by_user_id(user_id)

        # Return user id
        return {
            "notebook_ids": [notebook.id for notebook in notebooks]
        }


    @jwt_required()
    def post(self):
        # Get user id
        user_id = get_jwt_identity()

        # Get notebook name
        arguments = self.parse_args()
        notebook_name = arguments["name"]

        # Check for duplicated name
        if NotebookModel.find_by_name(notebook_name):
            return {
                "message": "A notebook with the same name already exists"
            }, 400

        # Create a notebook
        notebook_creator = NoteBookCreator(notebook_name)
        notebook_creator.create()

        # Save into database -> The initial state is Pending
        notebook_model = NotebookModel(notebook_name, "Pending", user_id)
        notebook_model.save()

        # Reduce tokens
        user = UserModel.find_user_with_id(user_id)
        user.increase_tokens(-1)

        # Return notebook
        return notebook_model.json(), 201


class NotebookResource(Resource):
    @jwt_required()
    def get(self, notebook_id):
        # Get user
        user_id = get_jwt_identity()

        # Get notebook
        notebook = NotebookModel.find_by_id(notebook_id)

        # Check if notebook belongs to user
        if notebook.user_id != user_id:
            return {
                "message": "Notebook does not exist"
            }, 400

            # Get status and update -> Return
        status_getter = NoteBookStatus(notebook.name)
        status = status_getter.get_status()

        if status != notebook.status:
            notebook.update_status(status)

        return notebook.json()


class NotebookStartResource(Resource):
    @jwt_required()
    def post(self, notebook_id):
        # Get user
        user_id = get_jwt_identity()

        # Get notebook
        notebook = NotebookModel.find_by_id(notebook_id)

        # Check if notebook belongs to user
        if notebook.user_id != user_id:
            return {
                "message": "Notebook does not exist"
            }, 400

        # Stop and delete notebook instance
        notebook_creator = NoteBookCreator(notebook.name)
        notebook_creator.start()

        # Success message
        return {
            "message": "Notebook have been successfully started"
        }, 200


class NotebookStopResource(Resource):
    @jwt_required()
    def post(self, notebook_id):
        # Get user
        user_id = get_jwt_identity()

        # Get notebook
        notebook = NotebookModel.find_by_id(notebook_id)

        # Check if notebook belongs to user
        if notebook.user_id != user_id:
            return {
                "message": "Notebook does not exist"
            }, 400

        # Stop and delete notebook instance
        notebook_creator = NoteBookCreator(notebook.name)
        notebook_creator.stop()

        # Success message
        return {
            "message": "Notebook have been successfully stopped"
        }, 200


class NotebookUrlResource(Resource):
    @jwt_required()
    def get(self, notebook_id):
        # Get user
        user_id = get_jwt_identity()

        # Get notebook
        notebook = NotebookModel.find_by_id(notebook_id)

        # Check if notebook belongs to user
        if notebook.user_id != user_id:
            return {
                "message": "Notebook does not exist"
            }, 400

        # Get url
        url_getter = NoteBookUrlCreator(notebook.name)
        url = url_getter.create()

        # Response
        return {
            "url": url
        }, 200
        
