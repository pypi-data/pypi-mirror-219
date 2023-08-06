from typing import Dict,Any
from sklearn.metrics import adjusted_rand_score
from pureml_evaluate.metrics.metric_base import MetricBase


class AdjustedRandScore(MetricBase):
    name = 'adjusted_rand_score'
    input_type = 'int'
    output_type: Any = None
    kwargs: Dict = None


    def parse_data(self,data):
        return data
    

    def compute(self,references,predictions,**kwargs):

        score = adjusted_rand_score(labels_true=references,labels_pred=predictions)

        score = {
            self.name : float(score)
        }

        return score
    