from typing import Any,Dict
from pureml_evaluate.metrics.metric_base import MetricBase
from sklearn.metrics import completeness_score


class CompletenessScore(MetricBase):
    name = 'completeness_score'
    input_type = 'int'
    output_type: Any = None
    kwargs:Dict = None

    def parse_data(self,data):
        return data
    
    def compute(self,references,predictions,**kwargs):

        score = completeness_score(labels_true=references,labels_pred=predictions)

        score = {
            self.name : float(score)
        }

        return score
    