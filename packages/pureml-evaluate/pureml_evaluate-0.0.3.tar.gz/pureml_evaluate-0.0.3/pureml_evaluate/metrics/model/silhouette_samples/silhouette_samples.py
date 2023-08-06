from pureml_evaluate.metrics.metric_base import MetricBase
from typing import Any,Dict
from sklearn.metrics import silhouette_samples

class SilhouetteSamples(MetricBase):
    name = 'silhouette_samples'
    input_type = 'int'
    output_type: Any = None
    kwargs: Dict  = None

    def parse_data(self,data):
        return data
    
    def compute(self,X,labels,metric='euclidean',**kwargs):

        score = silhouette_samples(X,labels=labels,metric=metric)

        return {
            self.name : score
        }