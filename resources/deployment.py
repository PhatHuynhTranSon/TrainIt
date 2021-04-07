from flask_jwt_extended.view_decorators import jwt_required
from flask_jwt_extended import get_jwt_identity
from mlmodels.predictor import Predictor
from models.deployment import DeploymentModel
from mlmodels.creator import ModelCreator
from mlmodels.deployment import Deployment, DeploymentStatus, get_model_artifact_path
from flask_restful import Resource

from models.project import Project
from models.solution import Solution
from models.user import UserModel


class DeploymentResource(Resource):
    def project_does_not_exist_response(self):
        return {
            "message": "Project does not exist"
        }, 404 

    def solution_not_finish_message(self):
        return {
            "message": "Solution does not exist or not trained"
        }, 400

    def no_deployed_model_message(self):
        return {
            "message": "No deployed model found"
        }, 404

    def already_deployed_message(self):
        return {
            "message": "This project has already been deployed"
        }, 400

    def not_enough_tokens(self):
        return {
            "message": "Not enough tokens for deployment"
        }, 400

    @jwt_required()
    def get(self, project_id):
        project = Project.find_project_with_id(project_id)
        user_id = get_jwt_identity()
        if not project or not project.belongs_to_user(user_id):
            return self.project_does_not_exist_response()

        deployment_model = DeploymentModel.find_by_project_id(project_id)
        if not deployment_model:
            return {
                "deployed": False,
                "deployment": None
            }
        
        # Update status if possible
        if DeploymentStatus.in_transition_state(deployment_model.status):
            # Get model status and update
            deployment_status = DeploymentStatus(deployment_model.endpoint_name)
            new_status = deployment_status.get_status()
            deployment_model.update_status(new_status)

        return {
            "deployed": True,
            "deployment": deployment_model.json()
        }, 200

    @jwt_required()
    def post(self, project_id):
        project = Project.find_project_with_id(project_id)
        user_id = get_jwt_identity()
        if not project or not project.belongs_to_user(user_id):
            return self.project_does_not_exist_response()

        # Check if user have enough tokens
        user = UserModel.find_user_with_id(user_id);
        if user.tokens == 0:
            return self.not_enough_tokens()

        best_solution = Solution.find_best_solution_of_project(project.type, project.id)
        if not best_solution:
            return self.solution_not_finish_message()

        if DeploymentModel.if_a_deployment_exist(project.id):
            return self.already_deployed_message()

        model_artifact_path = get_model_artifact_path(best_solution.job_name)
        script_path = ModelCreator.get_algorithm_script(best_solution.algorithm_name)

        # Deploy model and get endpoint name
        deployment = Deployment(
            model_path=model_artifact_path,
            script_path=script_path
        )
        deployment.deploy()
        endpoint_name = deployment.get_endpointname()

        # Save into database
        deployment_model = DeploymentModel(
            project_id=project.id,
            endpoint_name=endpoint_name
        )
        deployment_model.save()

        # Decrease user tokens by 1
        user.increase_tokens(-1);

        return {
            "deployment": deployment_model.json()
        }, 201

    @jwt_required()
    def delete(self, project_id):
        project = Project.find_project_with_id(project_id)
        user_id = get_jwt_identity()
        if not project or not project.belongs_to_user(user_id):
            return self.project_does_not_exist_response()

        deployment_model = DeploymentModel.find_by_project_id(project.id)
        endpoint_name = deployment_model.endpoint_name

        predictor = Predictor(endpoint_name)
        predictor.undeploy()

        deployment_model.delete()

        return {
            "message": "Successfully deleted the endpoint"
        }, 200