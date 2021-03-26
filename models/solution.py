from models.project import Project
from models.classification import ClassficationProblem
from models.regression import RegressionProblem

class Solution:
    def __init__(self, project_id, algorithm_name, training_job_name, type):
        self.project_id = project_id
        self.algorithm_name = algorithm_name
        self.training_job_name = training_job_name
        
        if type == "classification":
            self.instance = ClassficationProblem(
                job_name=self.training_job_name,
                algorithm_name=algorithm_name,
                project_id=self.project_id
            )
        else:
            self.instance = RegressionProblem(
                job_name=self.training_job_name,
                algorithm_name=algorithm_name,
                project_id=self.project_id
            )

    def save(self):
        self.instance.save()

    def delete(self):
        self.instance.delete()

    def json(self):
        return self.instance.json()

    @classmethod
    def find_solution_with_id(self, type, solution_id):
        if type == "classification":
            solution = ClassficationProblem.find_solution_with_id(solution_id)
        else:
            solution = RegressionProblem.find_solution_with_id(solution_id)
        return solution

    @classmethod
    def find_solutions_of_projects(self, type, project_id):
        solution_ids =  ClassficationProblem.find_solutions_of_project(project_id) if type == "classification" else RegressionProblem.find_solutions_of_project(project_id)
        return solution_ids

    @classmethod
    def find_best_solution_of_project(self, type, project_id):
        if type == "classification":
            return ClassficationProblem.find_best_solution_of_project(project_id)
        else:
            return RegressionProblem.find_best_solution_of_project(project_id)

    def belongs_to(self, project_id):
        return self.instance.if_belongs_to(project_id)
