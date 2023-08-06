from pureml_evaluate.metrics.metric_base import MetricBase
from typing import Any,Dict
from sklearn.metrics.pairwise import nan_euclidean_distances
import numpy as np

class NanEuclideanDistances(MetricBase):
    name = 'nan_euclidean_distances'
    input_type = 'int'
    output_type: Any = None
    kwargs: Dict  = None

    def parse_data(self,data):
        return data
    
    def compute(self,X,Y=None,squared=False,missing_values = np.nan,copy = True,**kwargs):

        distance = nan_euclidean_distances(X=X,Y=Y,squared=squared,missing_values=missing_values,copy=copy)
        
        return {
            self.name : distance
        }