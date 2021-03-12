from database import database as db


class Dataset(db.Model):
    __tablename__ = "datasets"

    id = db.Column(db.Integer, primary_key=True)
    bucket_name = db.Column(db.String(255))
    folder_name = db.Column(db.String(255))
    object_name = db.Column(db.String(255))
    file_name = db.Column(db.String(255))

    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    project = db.relationship("Project")

    def __init__(self, bucket_name, folder_name, object_name, file_name, project_id):
        self.bucket_name = bucket_name
        self.folder_name = folder_name
        self.object_name = object_name
        self.file_name = file_name
        self.project_id = project_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_data_path(self):
        return f"s3://{self.bucket_name}/{self.folder_name}/train"

    @classmethod
    def find_data_by_id(cls, data_id):
        return cls.query.filter_by(id=data_id).first()
