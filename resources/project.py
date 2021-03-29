from flask_jwt_extended.utils import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required
from preprocessing import DataPreview
from storage import DataDownloader, DataUploader
from flask_restful import Resource, reqparse
import werkzeug

from models.project import Project
from models.data import Dataset

class ProjectListResource(Resource):
    def __init__(self):
        self.create_argument_parser()

    def create_argument_parser(self):
        self.parser = reqparse.RequestParser()

        self.parser.add_argument(
            "project_name",
            type=str,
            required=True,
            help="Project name must be provided"
        )

        self.parser.add_argument(
            "project_description",
            type=str,
            required=True,
            help="Project description must be provided"
        )

        self.parser.add_argument(
            "project_type",
            type=str,
            required=True,
            help="Project type must be provided"
        )

        self.parser.add_argument(
            "project_data",
            type=werkzeug.datastructures.FileStorage,
            required=True,
            help="Project data must be provided",
            location="files"
        )

    def parse_arguments(self):
        args =  self.parser.parse_args()
        project_name = args["project_name"]
        project_description = args["project_description"]
        project_type = args["project_type"]
        project_data = args["project_data"]
        return project_name, project_description, project_type, project_data

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()

        project_name, project_description, project_type, project_data = self.parse_arguments()   

        project = Project(project_name, project_description, project_type, user_id)
        project.save()

        uploader = DataUploader(project.location_name, project_data)
        uploader.upload()
        
        data = Dataset(
                bucket_name=uploader.get_bucket_name(), 
                folder_name=project.location_name, 
                object_name=uploader.get_object_name(),
                file_name=project_data.filename,
                project_id=project.id
            )
        data.save()

        return {
            "project": project.json()
        }

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        projects = Project.find_project_from_user(user_id)

        return {
            "projects": [project.json() for project in projects]
        }


class ProjectResource(Resource):
    def project_does_not_exist_response(self):
        return {
            "message": "Project does not exist"
        }, 404

    def get_data_preview(self, project_data):
        file = DataDownloader(project_data.folder_name, project_data.object_name).get_file()
        preview = DataPreview(file)
        return preview.parse()
    
    @jwt_required()
    def get(self, project_id):
        project = Project.find_project_with_id(project_id)
        user_id = get_jwt_identity()
        if not project or not project.belongs_to_user(user_id):
            return self.project_does_not_exist_response()

        project_data = Dataset.find_data_by_id(project.id)
        project_data_preview = self.get_data_preview(project_data)

        return {
            "project": project.json(),
            "data": project_data_preview
        }
