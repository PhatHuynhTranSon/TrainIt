from storage import DataUploader
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

    def post(self):
        project_name, project_description, project_type, project_data = self.parse_arguments()   

        project = Project(project_name, project_description, project_type)
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


class ProjectResource(Resource):
    def project_not_found(self):
        return {
            "mesage": "Project not found"
        }, 404
    
    def get(self, project_id):
        project = Project.find_project_with_id(project_id)

        if not project:
            return self.project_not_found()

        return {
            "project": project.json()
        }
