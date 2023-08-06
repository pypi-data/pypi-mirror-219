from pureml_evaluate.metrics.metric_base import MetricBase
from typing import Dict,Any
from sklearn.metrics import davies_bouldin_score


class DaviesBouldinScore(MetricBase):
    name = 'davies_bouldin_score'
    input_type = 'int'
    output_type: Any = None
    kwargs: Dict = None

    
    def parse_data(self,data):
        return data
    

    def compute(self,X,labels,**kwargs):
        
        score = davies_bouldin_score(X=X,labels=labels)

        score = {
            self.name : float(score)
        }

        return score
    
    