from s3 import get_sagemaker_session
from sagemaker.sklearn.estimator import SKLearn
from config import aws_role


class SagemakerClassification:
    def __init__(self, script_path, data_path, hyperparameters):
        self.script_path = script_path
        self.data_path = data_path
        self.hyperparameters = hyperparameters

        self.create_sagemaker_session()
        self.create_sklearn_estimator()

    def create_sagemaker_session(self):
        self.sagemaker_session = get_sagemaker_session()

    def create_sklearn_estimator(self):
        self.estimator = SKLearn(
            self.script_path,
            instance_type="ml.m4.xlarge",
            framework_version="0.20.0",
            sagemaker_session=self.sagemaker_session,
            role=aws_role,
            metric_definitions=[
                {
                    "Name": "train:accuracy",
                    "Regex": "Train_accuracy=(.*?);"
                },
                {
                    "Name": "test:accuracy",
                    "Regex": "Test_accuracy=(.*?);"
                },
                {
                    "Name": "train:f1",
                    "Regex": "Train_f1=(.*?);"
                },
                {
                    "Name": "test:f1",
                    "Regex": "Test_f1=(.*?);"
                }
            ],
            hyperparameters=self.hyperparameters
        )

    def fit(self):
        self.estimator.fit({ "train": self.data_path }, wait=False)

    def get_training_name(self):
        return self.estimator.latest_training_job.job_name


