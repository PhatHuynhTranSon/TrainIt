from s3 import get_boto_session
import boto3


class Status:
    def __init__(self, job_name):
        self.job_name = job_name
        self.boto_session = get_boto_session()
        self.sagemaker_client = self.boto_session.client("sagemaker")

    def describe_training_job(self):
        return self.sagemaker_client.describe_training_job(
            TrainingJobName=self.job_name
        )

    def get_core_parameters(self, parameters):
        return {
            parameter: parameters[parameter] for parameter in parameters if not parameter.startswith("sagemaker") 
        }

    def get_status(self):
        response = self.describe_training_job()
        return {
            "main_status": response["TrainingJobStatus"],
            "secondary_status": response["SecondaryStatus"],
            "hyperparameters": self.get_core_parameters(response["HyperParameters"])
        }