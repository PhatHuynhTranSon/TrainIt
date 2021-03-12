from resources.project import ProjectListResource
from flask import Flask
from flask_restful import Api
from config import (
    DATABASE_URI
)
from database import database as db

# Create app
app = Flask(__name__)
api = Api(app)

# Set up database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI

@app.before_first_request
def create_all_tables_before_requests():
    db.create_all()

# Add resources
api.add_resource(ProjectListResource, "/projects")

if __name__ == "__main__":
    # Initialize database
    db.init_app(app)
    
    # Don't use debug=True in production
    app.run(port=5000, debug=True)