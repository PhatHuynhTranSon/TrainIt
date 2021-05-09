from resources.notebook import NotebookListResource, NotebookResource, NotebookStartResource, NotebookStopResource, NotebookUrlResource
from resources.payment import PaymentResource
from resources.authentication import UserSigninResource, UserSignupResource
from resources.prediction import OnlinePredictionResource
from resources.deployment import DeploymentResource
from resources.preview import DataPreviewRersource
from resources.solution import SolutionDownloadResource, SolutionResource, SolutionListResource
from resources.project import ProjectListResource, ProjectResource

from flask_jwt_extended import JWTManager

from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from config import (
    DATABASE_URI,
    JWT_SECRET,
    JWT_EXPIRATION
)
from database import database as db
from hashing import bcrypt

# Create app
app = Flask(__name__)
api = Api(app)

# Handle Cross origin requst
CORS(app)

# Set up database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI

@app.before_first_request
def create_all_tables_before_requests():
    db.create_all()

# Set up password hashing
bcrypt.init_app(app)

# Set JWT
app.config["JWT_SECRET_KEY"] = JWT_SECRET
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = JWT_EXPIRATION
jwt = JWTManager(app)

# Add resources
api.add_resource(ProjectListResource, "/projects")
api.add_resource(ProjectResource, "/projects/<int:project_id>")

api.add_resource(DeploymentResource, "/projects/<int:project_id>/deploy")
api.add_resource(SolutionListResource, "/projects/<int:project_id>/solutions")
api.add_resource(SolutionDownloadResource, "/projects/<int:project_id>/solutions/<int:solution_id>/download")
api.add_resource(SolutionResource, "/projects/<int:project_id>/solutions/<int:solution_id>")

api.add_resource(DataPreviewRersource, "/preview")
api.add_resource(OnlinePredictionResource, "/projects/<int:project_id>/prediction/online")

api.add_resource(UserSignupResource, "/users/signup")
api.add_resource(UserSigninResource, "/users/signin")

api.add_resource(PaymentResource, "/tokens")

api.add_resource(NotebookListResource, "/notebooks")
api.add_resource(NotebookResource, "/notebooks/<int:notebook_id>")
api.add_resource(NotebookStartResource, "/notebooks/start/<int:notebook_id>")
api.add_resource(NotebookStopResource, "/notebooks/stop/<int:notebook_id>")
api.add_resource(NotebookUrlResource, "/notebooks/url/<int:notebook_id>")

if __name__ == "__main__":
    # Initialize database
    db.init_app(app)

    # Don't use debug=True in production
    app.run(port=5000, host="0.0.0.0", debug=True)