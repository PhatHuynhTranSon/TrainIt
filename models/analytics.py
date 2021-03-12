from mlmodels.analytics import Analytics as ModelAnalytics


class Analytics:
    def __init__(self, solution):
        self.solution = solution

    def get_solution_metrics(self):
        model_analytics = ModelAnalytics(self.solution.job_name)
        return model_analytics.get_analytics()

        