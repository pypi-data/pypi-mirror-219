from sklearn.metrics import rand_score
from typing import Any,Dict
from pureml_evaluate.metrics.metric_base import MetricBase

class RandScore(MetricBase):
    name = 'rand_score'
    input_type = 'int'
    output_type: Any = None
    kwargs: Dict = None


    def parse_data(self,data):
        return data
    
    def compute(self,labels_true,labels_pred,**kwargs):

        score  = rand_score(labels_true=labels_true,labels_pred=labels_pred)

        return {
            self.name : float(score)
        }