from typing import Any
from sklearn.metrics import jaccard_score
from pureml_evaluate.metrics.metric_base import MetricBase

class JaccardScore(MetricBase):
    name = 'jaccard_score'
    input_type = 'int'
    output_type: Any = None
    kwargs = { }
        

    def parse_data(self, data):
        
        return data



    def compute(self, references, predictions, pos_label=1, average='binary',
                 sample_weight=None, **kwargs):

        score = jaccard_score(y_true=references, y_pred=predictions, pos_label=pos_label,
                                average=average, sample_weight=sample_weight)
        
        score = {
            self.name : score
            }
 

        return score