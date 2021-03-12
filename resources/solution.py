from mlmodels.creator import ModelCreator
from flask_restful import Resource, reqparse

from models.project import Project
from models.data import Dataset
from models.classification import ClassficationProblem
from models.regression import RegressionProblem

class SolutionResource(Resource):
    def __init__(self):
        self.create_argument_parser()

    def create_argument_parser(self):
        self.parser = reqparse.RequestParser()

        self.parser.add_argument(
            "algorithm_name",
            type=str,
            required=True,
            help="Algorithm name is required"
        )

        self.parser.add_argument(
            "hyperparameters",
            type=dict,
            required=True,
            help="Algorithm parameter is required"
        )

    def parse_arguments(self):
        data = self.parser.parse_args()

        algorithm_name = data["algorithm_name"]
        hyperparameters = data["hyperparameters"]

        return algorithm_name, hyperparameters

    def project_not_found(self):
        return {
            "message": "Project not found"
        }, 404

    def wrong_class_of_algorithm(self):
        return {
            "message": "Algorithm not available"
        }, 400

    def post(self, project_id):
        project = Project.find_project_with_id(project_id)
        if not project:
            return self.project_not_found()

        algorithm_name, hyperparameters = self.parse_arguments()
        if not ModelCreator.if_algorithm_belongs_to_problem_type(project.type, algorithm_name):
            return self.wrong_class_of_algorithm()

        project_type = project.type
        project_data = Dataset.find_data_by_id(project.id)

        ml_model = ModelCreator.create_model(
            algorithm_name,
            data_path=project_data.get_data_path(),
            hyperparameters=hyperparameters
        )
        ml_model.fit()

        training_job_name = ml_model.get_training_name()

        if project_type == "classification":
            ml_database_model = ClassficationProblem(
                job_name=training_job_name,
                algorithm_name=algorithm_name,
                project_id=project_id
            )
        else:
            ml_database_model = RegressionProblem(
                job_name=training_job_name,
                algorithm_name=algorithm_name,
                project_id=project_id
            )
        ml_database_model.save()

        return {
            "solution": ml_database_model.json()
        }, 201
        

