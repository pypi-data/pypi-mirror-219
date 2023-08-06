from pydantic import BaseModel
from .grade import Grader
from typing import Any, Union
from importlib import import_module
import numpy as np
from collections import defaultdict
from .risk_evaluator import RiskEvaluator
from .graphs_generator import GraphsGenerator
import pkg_resources

class Evaluator(BaseModel):
    y_true: Any
    y_pred: Any
    y_pred_scores: Any = None
    sensitive_features: Union[None, Any]

    evaluators: Union[list[str], str]
    grader: list[Grader] = []
    dataset: Any = None

    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True

    def load_graders(self):
        if type(self.evaluators) == str:
            self.grader.append(Grader(task_type=self.evaluators))
        elif type(self.evaluators) == list:
            for e in self.evaluators:
                self.grader.append(Grader(task_type=e))
        else:
            print("Unknown Evaluators: ", self.evaluators)

    def load(self):
        self.load_graders()

    def evaluate(self):

        values_all = defaultdict(dict)

        for g in self.grader:
            grader_type = g.task_grader.evaluation_type

            values = g.compute(
                references=self.y_true, predictions=self.y_pred,
                sensitive_features=self.sensitive_features, prediction_scores=self.y_pred_scores
            )

            values_all[grader_type].update(values)
            #values_all[grader_type] = {'value' : values}
        
        values_all = dict(values_all)

        return values_all

    def evaluate_subsets(self):
        if self.sensitive_features is None:  # If No Sensitive Features are given
            return 
    
        if self.sensitive_features is not None: 
            subsets = self.give_subsets()

            values_subsets_all = {}

            for subset in subsets:
                values_all = defaultdict(dict)

                key = subset['key']
                y_true = subset['y_true']
                y_pred = subset['y_pred']
                sensitive_features = subset['sensitive_features']
                y_pred_scores = subset['y_pred_scores']

                for g in self.grader:
                    grader_type = g.task_grader.evaluation_type

                    values = g.compute(
                        references=y_true, predictions=y_pred,
                        sensitive_features=sensitive_features, prediction_scores=y_pred_scores
                    )

                    values_all[grader_type].update(values)
                    #values_all[grader_type] = {'value': values} # To Add Status (Pass/Fail) and Risk (No/Low/Medium/High) based on Threshold in Future.
                values_all = dict(values_all)
                values_subsets_all[key] = values_all
        return values_subsets_all

    def give_subsets(self):
        subsets = []
        unique_values = np.unique(self.sensitive_features)

        #print(f"Unique values: {unique_values}")
        for value in unique_values:
            #print(f"values: {value}")
            ind = np.where(self.sensitive_features == value)

            #print(f"Ind: {ind}")
            sub_dict = {
                "key": value,
                "y_true": self.y_true[ind],
                "y_pred": self.y_pred[ind],
                "sensitive_features": self.sensitive_features[ind],
            }

            #print(f"sub_dict: {sub_dict}")
            if self.y_pred_scores is not None:
                sub_dict.update({"y_pred_scores": self.y_pred_scores[ind]})
            else:
                sub_dict.update({"y_pred_scores": self.y_pred_scores})

            #print("Sub dict passed")
            subsets.append(sub_dict)

        return subsets


def eval(y_true, y_pred, sensitive_features, evaluators, y_pred_scores=None,threshold = 80,path_to_config=None,as_html=False,as_pdf=False,pdf_file_name='metrics_graph.pdf'):
    evaluator = Evaluator(
        y_true=y_true, y_pred=y_pred, sensitive_features=sensitive_features, evaluators=evaluators, y_pred_scores=y_pred_scores
    )

    evaluator.load()

    values_all = evaluator.evaluate()
    values_subset_all = evaluator.evaluate_subsets()

    if pdf_file_name is None:
        pdf_file_name = 'metrics_graph.pdf'

    if path_to_config is None:
        path_to_config = pkg_resources.resource_filename(__name__, 'config.json')
    else:
        path_to_config = path_to_config
    riskevaluate = RiskEvaluator(values_all,values_subset_all,path_to_config=path_to_config)
    riskevaluate.compute_status()

    if as_pdf != False or as_html != False:
        graphs_generator = GraphsGenerator()
        if as_pdf == True:
            graphs_generator.get_graphs_as_pdf(values_all=values_all,values_subset_all=values_subset_all,pdf_file_name=pdf_file_name)
        if as_html == True:
            graphs_generator.get_graphs_as_html(values_all=values_all,values_subset_all=values_subset_all)

    values = {
        "complete": values_all,
        "subsets": values_subset_all
    }

    return values
