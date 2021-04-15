from mlmodels.algorithms.regression import SagemakerRegression
from mlmodels.algorithms.classification import SagemakerClassification


class ModelNotFoundException(Exception):
    pass


class ModelCreator: 
    ALGORITHMS = {
        "classification": ["logistic_regression", "gaussian_naive_bayes", "decision_tree_classification"],
        "regression": ["linear_regression", "decision_tree_regression", "elastic_net_regression"]
    }

    @classmethod
    def if_algorithm_belongs_to_problem_type(cls, problem_type, algorithm):
        return algorithm in cls.ALGORITHMS[problem_type]

    @classmethod
    def get_algorithm_script(cls, algorithm):
        if algorithm == "logistic_regression":
            name = "logistic_regression_script"
        elif algorithm == "gaussian_naive_bayes":
            name = "naive_bayes_script"
        elif algorithm == "linear_regression":
            name = "linear_regression_script"
        elif algorithm == "decision_tree_regression":
            name = "decision_tree_regression_script"
        elif algorithm == "decision_tree_classification":
            name = "decision_tree_classification_script"
        elif algorithm == "elastic_net_regression":
            name = "elastic_net_regression_script"
        else:
            raise ModelNotFoundException()

        return f"mlmodels/scripts/{name}.py"

    @classmethod 
    def is_classification(cls, algorithm):
        return algorithm in cls.ALGORITHMS["classification"]

    @classmethod
    def create_model(cls, algorithm_name, data_path, hyperparameters):
        algorithm_script = cls.get_algorithm_script(algorithm_name)

        if cls.is_classification(algorithm_name):
            return SagemakerClassification(
                algorithm_script,
                data_path=data_path,
                hyperparameters=hyperparameters
            )
        else: 
            return SagemakerRegression(
                algorithm_script,
                data_path=data_path,
                hyperparameters=hyperparameters
            )