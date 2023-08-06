from pureml_evaluate.metrics.metric_base import MetricBase
from typing import Any,Dict
from sklearn.metrics import silhouette_score


class SilhouetteScore(MetricBase):
    name = 'silhouette_score'
    input_type = 'int'
    output_type: Any = None
    kwargs: Dict = None

    def parse_data(self,data):
        return data
    
    def compute(self,X,labels,metric='euclidean',sample_size = None,random_state = None,**kwargs):

        score = silhouette_score(X,labels=labels,metric=metric,sample_size=sample_size,random_state=random_state) 

        
        return {
            self.name : float(score)
        }