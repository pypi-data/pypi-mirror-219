from typing import Any
from sklearn.metrics import class_likelihood_ratios
from pureml_evaluate.metrics.metric_base import MetricBase

class ClassLikelihoodRatios(MetricBase):
    name = 'class_likelihood_ratios'
    input_type = 'int'
    output_type: Any = None
    kwargs = { }
        

    def parse_data(self, data):
        
        return data



    def compute(self, references, predictions, sample_weight=None, **kwargs):

        score = class_likelihood_ratios(y_true=references, y_pred=predictions,  sample_weight=sample_weight)
        
        score = {
            self.name : score
            }
 

        return score