from mlmodels.algorithms.logistic_regression import SagemakerLogisticRegression
import os


class ModelNotFoundException(Exception):
    pass


class ModelCreator: 
    ALGORITHMS = {
        "classification": ["logistic_regression"],
        "regression": ["linear_regression"]
    }

    @classmethod
    def if_algorithm_belongs_to_problem_type(cls, problem_type, algorithm):
        return algorithm in cls.ALGORITHMS[problem_type]

    @classmethod
    def create_model(cls, algorithm_name, data_path, hyperparameters):
        print(os.getcwd())
        if algorithm_name == "logistic_regression":
            return SagemakerLogisticRegression(
                "mlmodels/scripts/logistic_regression_script.py",
                data_path=data_path,
                hyperparameters=hyperparameters
            )
        raise ModelNotFoundException()