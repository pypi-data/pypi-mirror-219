from typing import Any
from sklearn.metrics import hamming_loss
from pureml_evaluate.metrics.metric_base import MetricBase

class HammingLoss(MetricBase):
    name = 'hamming_loss'
    input_type = 'int'
    output_type: Any = None
    kwargs = { }
        

    def parse_data(self, data):
        
        return data



    def compute(self, references, predictions,sample_weight=None, **kwargs):

        score = hamming_loss(y_true=references, y_pred=predictions,
                                sample_weight=sample_weight)
        
        score = {
            self.name : float(score)
            }
 

        return score