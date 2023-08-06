
from sklearn.metrics import det_curve
from pureml_evaluate.metrics.metric_base import MetricBase
from typing import Any

class DetCurve(MetricBase):
    name = 'det_curve'
    input_type = 'int'
    output_type: Any = None
    kwargs = { }
        

    def parse_data(self, data):
        
        return data



    def compute(self, references, predictions=None, prediction_scores=None, sample_weight=None, **kwargs):

        if prediction_scores is None and predictions is None:
            fpr, fnr, thresholds =  None, None, None
        elif predictions is None:
            fpr, fnr, thresholds  = det_curve(y_true=references, y_score=prediction_scores, sample_weight=sample_weight)
            
        elif prediction_scores is None:
            fpr, fnr, thresholds = det_curve(y_true=references, y_score=predictions, sample_weight=sample_weight,)
            
        
        score = {
            self.name : {"fpr":fpr, "fnr":fnr, "thresholds":thresholds}
            }
 

        return score