from flask_restful import Resource, reqparse

from models.project import Project
from models.deployment import DeploymentModel

from mlmodels.predictor import Predictor

class OnlinePredictionResource(Resource):
    def __init__(self):
        self.create_argument_parser()

    def create_argument_parser(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "data",
            type=list,
            required=True,
            help="Please kindly provide the data for inference",
            location="json"
        )

    def post(self, project_id):
        project = Project.find_project_with_id(project_id)
        if not project:
            return self.project_does_not_exist_message()

        deployment = DeploymentModel.find_by_project_id(project_id)
        if not deployment:
            return self.deployment_does_not_exist_message()

        predictor = Predictor(deployment.endpoint_name)
        data = self.parse_data()

        result = predictor.predict(data)
        result = self.parse_result(result)

        return {
            "result": result
        }

    def project_does_not_exist_message(self):
        return {
            "message": "Project does not exist"
        }, 404

    def deployment_does_not_exist_message(self):
        return {
            "message": "Project has not been deployed"
        }, 404

    def parse_data(self):
        args = self.parser.parse_args()
        data = args["data"]
        return [data] # Wrap around another array

    def parse_result(self, result):
        return result[0]
