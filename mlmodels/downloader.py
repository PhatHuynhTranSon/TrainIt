from s3 import get_s3_client
from config import aws_sagemaker_bucket

class SolutionMapper:
    # Get bucket and object name from solution
    def map(self, solution):
        bucket = aws_sagemaker_bucket
        object = solution.job_name + "/output/model.tar.gz"
        return bucket, object

class ObjectDownloader:
    def __init__(self):
        self.s3 = get_s3_client()

    def get_download_url(self, bucket_name, object_name):
        response = self.s3.generate_presigned_url(
            "get_object", 
            Params={ "Bucket": bucket_name, "Key": object_name },
            ExpiresIn=200
        )
        return response

class SolutionDownloader:
    def __init__(self, solution):
        self.solution = solution
        self.mapper = SolutionMapper()
        self.downloader = ObjectDownloader()

    def get_solution_url(self):
        # Map from solution to bucket and object
        bucket, object = self.mapper.map(self.solution)
        # Get download link from bucket and object
        download_url = self.downloader.get_download_url(bucket_name=bucket, object_name=object)
        return download_url