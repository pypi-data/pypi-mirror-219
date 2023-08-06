
from sklearn.metrics import d2_absolute_error_score
from pureml_evaluate.metrics.metric_base import MetricBase
from typing import Any

class D2AbsoluteErrorScore(MetricBase):
    name = 'd2_absolute_error_score'
    input_type = 'int'
    output_type: Any = None
    kwargs = { }
        

    def parse_data(self, data):
        
        return data



    def compute(self, references, predictions, sample_weight=None, **kwargs):

        score = d2_absolute_error_score(y_true=references, y_pred=predictions,
                                sample_weight=sample_weight)
        
        score = {
            self.name : {'value' :float(score)}
            }
 

        return score