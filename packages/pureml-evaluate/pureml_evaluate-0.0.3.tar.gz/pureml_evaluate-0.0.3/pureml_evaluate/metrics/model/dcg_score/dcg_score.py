
from sklearn.metrics import dcg_score
from pureml_evaluate.metrics.metric_base import MetricBase
from typing import Any

class DcgScore(MetricBase):
    name = 'dcg_score'
    input_type = 'int'
    output_type: Any = None
    kwargs = {}
        

    def parse_data(self, data):
        
        return data



    def compute(self, references, predictions=None, prediction_scores=None, k=None, sample_weight=None, **kwargs):
        
        if prediction_scores is None and predictions is None:
            score = None
        elif predictions is None:
            score = dcg_score(y_true=references, y_score=prediction_scores, k=k,
                                sample_weight=sample_weight)
            score = float(score)
        elif prediction_scores is None:
            score = dcg_score(y_true=references, y_score=predictions, k=k,
                                sample_weight=sample_weight)
            score = float(score)
        
        
        score = {
            self.name : float(score)
            }
 

        return score