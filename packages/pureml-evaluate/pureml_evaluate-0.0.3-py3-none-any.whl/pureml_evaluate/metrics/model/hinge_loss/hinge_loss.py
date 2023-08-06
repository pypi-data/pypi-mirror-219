from sklearn.metrics import hinge_loss
from pureml_evaluate.metrics.metric_base import MetricBase
from typing import Any

class HingeLoss(MetricBase):

    name = 'hinge_loss'
    input_type = 'float'
    output_type: Any = None
    kwargs = { }
        

    def parse_data(self, data):
        
        return data


    def compute(self, references, predictions=None, prediction_scores=None, sample_weight=None,
                 labels=None, **kwargs):
        
        if prediction_scores is None and predictions is None:
            score = None
        elif predictions is None:
            score = hinge_loss(y_true=references, pred_decision=prediction_scores, sample_weight=sample_weight,
                                  labels=labels)
            score = float(score)
        elif prediction_scores is None:
            score = hinge_loss(y_true=references, pred_decision=predictions,  sample_weight=sample_weight,
                             labels=labels)
            score = float(score)
        
        score = {
            self.name : score
            }
 

        return score