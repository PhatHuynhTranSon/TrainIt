from s3 import get_s3_storage
import uuid


class DataUploader:
    def __init__(self, subfolder, file):
        self.subfolder = subfolder
        self.file = file
        self.s3 = get_s3_storage()

    def get_train_subfolder_name(self):
        return self.subfolder + "/train"

    def combine_name(self, subfolder_name, object_name):
        return subfolder_name + "/" + object_name

    def get_random_object_name(self):
        return uuid.uuid4().hex

    def get_data_location(self):
        return "s3://" + self.s3.get_bucket()+ "/" + self.get_train_subfolder_name() + "/" + self.object_name

    def upload(self):
        random_object_name = self.get_random_object_name()
        subfolder_name = self.get_train_subfolder_name()
        path = self.combine_name(subfolder_name, random_object_name)

        self.s3.upload_file(
            path, 
            self.file
        )

        self.object_name = random_object_name # Cache object name

    def get_object_name(self):
        return self.object_name

    def get_bucket_name(self):
        return self.s3.bucket


class DataDownloader:
    def __init__(self, folder_name, object_name):
        self.folder_name = folder_name
        self.object_name = object_name
        self.s3 = get_s3_storage()

    def get_path(self):
        return self.folder_name + "/train/" + self.object_name

    def get_file(self):
        data_path = self.get_path()
        return self.s3.get_file(data_path)
