from typing import Dict,Any
from sklearn.metrics import mean_pinball_loss
from pureml_evaluate.metrics.metric_base import MetricBase

class MeanPinballLoss(MetricBase):
    name = 'mean_pinball_loss'
    input_type = 'int'
    output_type: Any = None
    kwargs: Dict = None
        

    def parse_data(self, data):
        
        return data



    def compute(self, references, predictions, alpha=0.5, sample_weight=None, **kwargs):

        score = mean_pinball_loss(y_true=references, y_pred=predictions, alpha=alpha,
                                sample_weight=sample_weight)
        
        score = {
            self.name : score
            }
 

        return score