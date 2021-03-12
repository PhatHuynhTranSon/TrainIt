import boto3
import sagemaker
from config import (
    aws_access_key_id,
    aws_secret_access_key,
    aws_bucket,
    region_name
)


# Handling of session
def get_boto_session():
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )
    return session


def get_sagemaker_session():
    boto_session = get_boto_session()
    sagemaker_session = sagemaker.Session(
        boto_session=boto_session
    )
    return sagemaker_session

# Handling of s3 bucket
class S3Storage:
    def __init__(self, bucket):
        self.bucket = bucket
        self.boto_session = get_boto_session()
        self.s3_client = self.boto_session.client("s3")

    def upload_file(self, path, file):
        self.s3_client.upload_fileobj(
            file,
            self.bucket,
            path
        )

    def get_bucket(self):
        return self.bucket


def get_s3_storage():
    return S3Storage(aws_bucket)