
from sklearn.metrics import d2_tweedie_score
from pureml_evaluate.metrics.metric_base import MetricBase
from typing import Any

class D2TweedieScore(MetricBase):
    name = 'd2_tweedie_score'
    input_type = 'int'
    output_type: Any = None
    kwargs = { }
        

    def parse_data(self, data):
        
        return data



    def compute(self, references, predictions, power=0, sample_weight=None, **kwargs):

        score = d2_tweedie_score(y_true=references, y_pred=predictions, power=power,
                                sample_weight=sample_weight)
        
        score = {
            self.name : {'value' :float(score)}
            }
 

        return score