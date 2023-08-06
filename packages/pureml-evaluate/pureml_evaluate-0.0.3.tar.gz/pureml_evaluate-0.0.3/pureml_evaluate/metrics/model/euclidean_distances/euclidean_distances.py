from pureml_evaluate.metrics.metric_base import MetricBase
from sklearn.metrics.pairwise import euclidean_distances
from typing import Any,Dict


class EuclideanDistances(MetricBase):
    name = 'euclidean_distances'
    input_type = 'int'
    output_type: Any = None
    kwargs: Dict = None


    def parse_data(self,data):
        return data
    

    def compute(self,X, Y=None, Y_norm_squared=None, squared=False, X_norm_squared=None,**kwargs):

       distance = euclidean_distances(X=X,Y=Y,Y_norm_squared=Y_norm_squared,squared=squared,X_norm_squared=X_norm_squared)

       return {
           self.name : distance
       }