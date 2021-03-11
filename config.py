from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv()

# Retrieve variables for easier usage
DATABASE_URI = os.environ.get("DATABASE_URI")