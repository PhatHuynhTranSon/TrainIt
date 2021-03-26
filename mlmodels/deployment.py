from sagemaker.sklearn.model import SKLearnModel
from s3 import get_sagemaker_session, get_sagemaker_client
from config import aws_role, aws_sagemaker_bucket

class ScriptNotFoundException(Exception):
    pass

def get_model_artifact_path(job_name):
    return f"s3://{aws_sagemaker_bucket}/{job_name}/output/model.tar.gz"

class ModelNotDeployedException(Exception):
    pass

class Deployment:
    def __init__(self, model_path, script_path):
        self.model_path = model_path
        self.script_path = script_path
        self.session = get_sagemaker_session()
        self.attach_model()

    def attach_model(self):
        # Ok this is working -> Just need to provide a model func
        self.model = SKLearnModel(
            model_data=self.model_path,
            role=aws_role,
            entry_point=self.script_path,
            framework_version="0.20.0",
            sagemaker_session=self.session
        )

    def deploy(self):
        self.predictor = self.model.deploy(
            instance_type="ml.c4.xlarge", 
            initial_instance_count=1,
            wait=False
        )
        self.deployed = True

    def get_endpointname(self):
        return self.predictor.endpoint_name


class DeploymentStatus:
    def __init__(self, endpoint_name):
        self.client = get_sagemaker_client()
        self.endpoint_name = endpoint_name

    def extract_status(self, response):
        return response["EndpointStatus"]

    def get_status(self):
        response = self.client.describe_endpoint(
            EndpointName=self.endpoint_name
        )
        status = self.extract_status(response)
        return status

    @classmethod
    def in_transition_state(cls, status):
        return status not in ["OutOfService", "InService", "Failed"]


