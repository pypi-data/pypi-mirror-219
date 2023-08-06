
from sklearn.metrics import d2_pinball_score
from pureml_evaluate.metrics.metric_base import MetricBase
from typing import Any 

class D2PinballScore(MetricBase):
    name = 'd2_pinball_score'
    input_type = 'int'
    output_type:Any = None
    kwargs = {}
        

    def parse_data(self, data):
        
        return data


    def compute(self, references, predictions, alpha=0.5, sample_weight=None, **kwargs):

        score = d2_pinball_score(y_true=references, y_pred=predictions, alpha=alpha,
                                sample_weight=sample_weight)
        
        score = {
            self.name : {'value' : float(score) }
            }
 

        return score