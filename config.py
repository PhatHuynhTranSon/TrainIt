from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv()

# Retrieve variables for easier usage
DATABASE_URI = os.environ.get("DATABASE_URI")
JWT_SECRET = os.environ.get("JWT_SECRET")
aws_access_key_id = os.environ.get("aws_access_key_id")
aws_secret_access_key = os.environ.get("aws_secret_access_key")
aws_role = os.environ.get("aws_role")
region_name = os.environ.get("region_name")
aws_bucket = os.environ.get("aws_bucket")
aws_sagemaker_bucket = os.environ.get("aws_sagemaker_bucket")