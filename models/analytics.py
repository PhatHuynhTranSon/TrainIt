from mlmodels.status import Status
from mlmodels.analytics import Analytics as ModelAnalytics


class Analytics:
    def __init__(self, solution):
        self.solution = solution

    def get_solution_metrics(self):
        model_analytics = ModelAnalytics(self.solution.job_name)
        return model_analytics.get_analytics()

    def get_status(self):
        model_status = Status(self.solution.job_name)
        return model_status.get_status()

    def solution_has_completed(self, main_status):
        return main_status == "Completed"

    def solution_has_failed(self, main_status):
        return main_status == "Failed"