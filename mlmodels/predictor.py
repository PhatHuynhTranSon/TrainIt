from sagemaker.predictor import Predictor as SagemakerPredictor
from sagemaker.serializers import NumpySerializer
from sagemaker.deserializers import NumpyDeserializer
from s3 import get_sagemaker_session


class Predictor:
    def __init__(self, endpoint_name):
        self.endpoint_name = endpoint_name
        self.session = get_sagemaker_session()
        self.attach_predictor()

    def attach_predictor(self):
        self.predictor = SagemakerPredictor(
            endpoint_name=self.endpoint_name,
            sagemaker_session=self.session,
            serializer=NumpySerializer(),
            deserializer=NumpyDeserializer()
        )

    def predict(self, data):
        return self.predictor.predict(data)

    def undeploy(self):
        self.predictor.delete_endpoint()