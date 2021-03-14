from preprocessing import DataPreview, InvalidDataException
from flask_restful import Resource, reqparse
import werkzeug


class DataPreviewRersource(Resource):
    def __init__(self):
        self.create_argument_parser()

    def create_argument_parser(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "file",
            type=werkzeug.datastructures.FileStorage,
            required=True,
            location="files",
            help="A data file is required"
        )

    def parse_arguments(self):
        args = self.parser.parse_args()
        return args["file"]

    def post(self):
        file = self.parse_arguments()

        try:
            data_preview = DataPreview(file)
        except InvalidDataException:
            return self.invalid_dataset()

        return data_preview.parse()

    def invalid_dataset(self):
        return {
            "message": "The data is in invalid format."
        }, 400