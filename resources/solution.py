from flask_jwt_extended.utils import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required
from mlmodels.creator import ModelCreator
from flask_restful import Resource, reqparse

from models.project import Project
from models.data import Dataset
from models.solution import Solution
from models.analytics import Analytics


class SolutionListResource(Resource):
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

    def project_does_not_exist_response(self):
        return {
            "message": "Project does not exist"
        }, 404

    def wrong_class_of_algorithm(self):
        return {
            "message": "Algorithm not available"
        }, 400

    @jwt_required()
    def get(self, project_id):
        project = Project.find_project_with_id(project_id)
        user_id = get_jwt_identity()
        if not project or not project.belongs_to_user(user_id):
            return self.project_does_not_exist_response()

        return {
            "solution_ids": Solution.find_solutions_of_projects(project.type, project.id)
        }

    @jwt_required()
    def post(self, project_id):
        project = Project.find_project_with_id(project_id)
        user_id = get_jwt_identity()
        if not project or not project.belongs_to_user(user_id):
            return self.project_does_not_exist_response()

        algorithm_name, hyperparameters = self.parse_arguments()

        if not ModelCreator.if_algorithm_belongs_to_problem_type(project.type, algorithm_name):
            return self.wrong_class_of_algorithm()

        project_data = Dataset.find_data_by_id(project.id)

        ml_model = ModelCreator.create_model(
            algorithm_name,
            data_path=project_data.get_data_path(),
            hyperparameters=hyperparameters
        )
        ml_model.fit()

        training_job_name = ml_model.get_training_name()

        ml_database_model = Solution(
            training_job_name=training_job_name,
            algorithm_name=algorithm_name,
            project_id=project_id,
            type=project.type
        )
        ml_database_model.save()
        
        return {
            "solution": ml_database_model.json()
        }, 201


class SolutionResource(Resource):
    def project_does_not_exist_response(self):
        return {
            "message": "Project does not exist"
        }, 404

    def solution_does_not_exist_response(self):
        return {
            "message": "Solution does not exist"
        }, 404

    @jwt_required()
    def get(self, project_id, solution_id):
        project = Project.find_project_with_id(project_id)
        user_id = get_jwt_identity()
        if not project or not project.belongs_to_user(user_id):
            return self.project_does_not_exist_response()

        solution = Solution.find_solution_with_id(project.type, solution_id)
        if not solution or not solution.if_belongs_to(project.id):
            return self.solution_does_not_exist_response()

        analytics = Analytics(solution)
        status = analytics.get_status()
        main_stats, secondary_stats = status["main_status"], status["secondary_status"]
        parameters = status["hyperparameters"]

        if not solution.analytics_filled():
            if analytics.solution_has_completed(main_stats):
                solution.update_analytics(analytics.get_solution_metrics())

        return {
            "type": project.type,
            "status": main_stats,
            "secondary_status": secondary_stats,
            "parameters": parameters,
            "solution": solution.json()
        }

        



        


