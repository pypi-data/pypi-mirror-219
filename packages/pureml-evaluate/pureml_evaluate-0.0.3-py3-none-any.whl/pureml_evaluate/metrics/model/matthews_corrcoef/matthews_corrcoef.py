from typing import Any
from sklearn.metrics import matthews_corrcoef
from pureml_evaluate.metrics.metric_base import MetricBase

class MatthewsCorrcoef(MetricBase):
    name = 'matthews_corrcoef'
    input_type = 'int'
    output_type: Any = None
    kwargs = { }
        

    def parse_data(self, data):
        
        return data



    def compute(self, references, predictions, sample_weight=None, **kwargs):

        score = matthews_corrcoef(y_true=references, y_pred=predictions,
                                sample_weight=sample_weight)
        
        score = {
            self.name : float(score)
            }
 

        return score