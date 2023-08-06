from sklearn.metrics import average_precision_score
from pureml_evaluate.metrics.metric_base import MetricBase
from typing import Any

class AveragePrecisionScore(MetricBase):
    name = 'average_precision_score'
    input_type = 'int'
    output_type: Any = 'int'
    kwargs = { }
        

    def parse_data(self, data):
        
        return data



    def compute(self, references, predictions=None, prediction_scores=None, average='macro', sample_weight=None, **kwargs):

        
        if prediction_scores is None and predictions is None:
            score = None
        elif predictions is None:
            score = average_precision_score(y_true=references, y_score=prediction_scores, average=average,
                                sample_weight=sample_weight)
            score = float(score)
        elif prediction_scores is None:
            score = average_precision_score(y_true=references, y_score=predictions, average=average,
                                sample_weight=sample_weight)
            score = float(score)
        
        score = {
            self.name : {'value' : float(score)}
            }
 

        return score