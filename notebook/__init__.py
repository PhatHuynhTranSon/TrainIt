from s3 import get_sagemaker_client
from config import aws_role


class NoteBookCreator:
    def __init__(self, name, instance_type="ml.t3.medium"):
        self.name = name
        self.instance_type = instance_type
        self.client = get_sagemaker_client()

    def create(self):
        self.client.create_notebook_instance(
            NotebookInstanceName=self.name,
            InstanceType=self.instance_type,
            RoleArn=aws_role
        )

    def stop(self):
        self.client.stop_notebook_instance(
            NotebookInstanceName=self.name
        )

    def delete(self):
        self.client.delete_notebook_instance(
            NotebookInstanceName=self.name
        )

    def start(self):
        self.client.start_notebook_instance(
            NotebookInstanceName=self.name
        )


class NoteBookStatus:
    def __init__(self, name):
        self.name = name
        self.client = get_sagemaker_client()

    def get_status(self):
        response = self.client.describe_notebook_instance(
            NotebookInstanceName=self.name
        )
        return self.parse_status(response)

    def parse_status(self, response):
        return response["NotebookInstanceStatus"]


class NoteBookUrlCreator:
    def __init__(self, name):
        self.name = name
        self.client = get_sagemaker_client()

    def create(self):
        response = self.client.create_presigned_notebook_instance_url(
            NotebookInstanceName=self.name
        )
        return self.parse_url(response)

    def parse_url(self, response):
        return response["AuthorizedUrl"]