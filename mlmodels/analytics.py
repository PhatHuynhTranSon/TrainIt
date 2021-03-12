from s3 import get_sagemaker_session
import sagemaker


class Analytics:
    def __init__(self, job_name):
        self.job_name = job_name
        self.session = get_sagemaker_session()
        self.attach_estimator()

    def attach_estimator(self):
        self.estimator = sagemaker.estimator.Estimator.attach(
            self.job_name,
            sagemaker_session=self.session
        )

    def parse_dataframe(self, dataframe):
        metrics = {}

        for _, row in dataframe.iterrows():
            metric = row["metric_name"]
            value = row["value"]

            metrics[metric] = value

        return metrics

    def get_analytics(self):
        dataframe = self.estimator.training_job_analytics.dataframe()
        return self.parse_dataframe(dataframe)