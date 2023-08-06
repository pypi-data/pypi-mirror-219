from sklearn.metrics import mutual_info_score
from typing import Any,Dict
from pureml_evaluate.metrics.metric_base import MetricBase

class MutualInfoScore(MetricBase):
    name = 'mutual_info_score'
    input_type = 'int'
    output_type: Any = None
    kwargs: Dict = None

    def parse_data(self,data):
        return data
    
    def compute(self,labels_true,labels_pred,contingency=None,**kwargs):

        if contingency is None:
            score = mutual_info_score(labels_true=labels_true,labels_pred=labels_pred)
        else:
            score = mutual_info_score(None,None,contingency=contingency)

        return {
            self.name : float(score)
        }