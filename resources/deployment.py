from mlmodels.predictor import Predictor
from models.deployment import DeploymentModel
from mlmodels.creator import ModelCreator
from mlmodels.deployment import Deployment, DeploymentStatus, get_model_artifact_path
from flask_restful import Resource

from models.project import Project
from models.solution import Solution


class DeploymentResource(Resource):
    def project_does_not_exist_message(self):
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

    def get(self, project_id):
        deployment_model = DeploymentModel.find_by_project_id(project_id)
        if not deployment_model:
            return self.no_deployed_model_message()
        
        # Update status if possible
        if DeploymentStatus.in_transition_state(deployment_model.status):
            # Get model status and update
            deployment_status = DeploymentStatus(deployment_model.endpoint_name)
            new_status = deployment_status.get_status()
            deployment_model.update_status(new_status)

        return {
            "deployment": deployment_model.json()
        }, 200

    def post(self, project_id):
        project = Project.find_project_with_id(project_id)
        if not project:
            return self.project_does_not_exist_message()

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

        return {
            "deployment": deployment_model.json()
        }, 201

    def delete(self, project_id):
        project = Project.find_project_with_id(project_id)
        if not project:
            return self.project_does_not_exist_message()

        deployment_model = DeploymentModel.find_by_project_id(project.id)
        endpoint_name = deployment_model.endpoint_name

        predictor = Predictor(endpoint_name)
        predictor.undeploy()

        deployment_model.delete()

        return {
            "message": "Successfully deleted the endpoint"
        }, 200