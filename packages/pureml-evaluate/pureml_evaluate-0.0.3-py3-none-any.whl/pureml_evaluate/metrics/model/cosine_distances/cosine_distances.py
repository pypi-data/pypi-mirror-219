from sklearn.metrics.pairwise import cosine_distances
from pureml_evaluate.metrics.metric_base import MetricBase
from typing import Any,Dict


class CosineDistances(MetricBase):
    name = 'cosine_distances'
    input_type = 'int'
    output_type: Any = None
    kwargs: Dict = None

    def parse_data(self,data):
        return  data
    

    def compute(self,X,Y=None,**kwargs):
        if Y is None:
            score = cosine_distances(X)
        else:
            score = cosine_distances(X,Y)

        return {
            self.name : score
        }