from typing import Any
from sklearn.metrics import fbeta_score
from pureml_evaluate.metrics.metric_base import MetricBase

class FbetaScore(MetricBase):
    name = 'fbeta_score'
    input_type = 'int'
    output_type: Any = None
    kwargs = { }
        

    def parse_data(self, data):
        
        return data


    def compute(self, references, predictions, average='binary', sample_weight=None,beta = 0.5, pos_label=1, **kwargs):

        score = fbeta_score(y_true=references, y_pred=predictions, average=average,
                                sample_weight=sample_weight, pos_label=pos_label,beta=beta)
        
        score = {
            self.name : float(score)
            }
 

        return score