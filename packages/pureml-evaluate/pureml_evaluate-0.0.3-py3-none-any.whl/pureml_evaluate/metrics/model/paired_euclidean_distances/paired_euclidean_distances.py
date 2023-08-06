from pureml_evaluate.metrics.metric_base import MetricBase
from typing import Any,Dict
from sklearn.metrics.pairwise import paired_euclidean_distances

class PairedEuclideanDistances(MetricBase):
    name = 'paired_euclidean_distances'
    input_type = 'int'
    output_type: Any = None
    kwargs: Dict = None

    def parse_data(self,data):
        return data
    
    def compute(self,X,Y,**kwargs):
        
        distance = paired_euclidean_distances(X, Y)

        return {
            self.name : distance
        }