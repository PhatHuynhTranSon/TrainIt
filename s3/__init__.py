import boto3
import sagemaker
from config import (
    aws_access_key_id,
    aws_secret_access_key,
    aws_bucket,
    region_name
)
from botocore.config import Config


# Handling of session
def get_boto_session():
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )
    return session


def get_sagemaker_client():
    session = get_boto_session()
    return session.client('sagemaker')


def get_s3_client():
    # Get configuration to use Sginature-V4
    config = Config(
        signature_version='s3v4'
    )
    session = get_boto_session()
    return session.client('s3', config=config)


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
        self.s3_client = get_s3_client()

    def upload_file(self, path, file):
        self.s3_client.upload_fileobj(
            file,
            self.bucket,
            path
        )

    def get_file(self, path):
        response = self.s3_client.get_object(
            Bucket=self.bucket,
            Key=path
        )
        return response["Body"];

    def get_bucket(self):
        return self.bucket


def get_s3_storage():
    return S3Storage(aws_bucket)