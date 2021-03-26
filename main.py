from resources.deployment import DeploymentResource
from resources.preview import DataPreviewRersource
from resources.solution import SolutionResource, SolutionListResource
from resources.project import ProjectListResource, ProjectResource
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from config import (
    DATABASE_URI
)
from database import database as db

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

# Add resources
api.add_resource(ProjectListResource, "/projects")
api.add_resource(ProjectResource, "/projects/<int:project_id>")
api.add_resource(DeploymentResource, "/projects/<int:project_id>/deploy")
api.add_resource(SolutionListResource, "/projects/<int:project_id>/solutions")
api.add_resource(SolutionResource, "/projects/<int:project_id>/solutions/<int:solution_id>")
api.add_resource(DataPreviewRersource, "/preview")

if __name__ == "__main__":
    # Initialize database
    db.init_app(app)

    # Don't use debug=True in production
    app.run(port=5000, debug=True)