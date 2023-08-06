from pureml_evaluate.metrics.metric_base import MetricBase
from typing import Any,Dict
from sklearn.metrics.pairwise import manhattan_distances

class ManhattanDistances(MetricBase):
    name = 'manhattan_distances'
    input_type = 'int'
    output_type: Any = None
    kwargs: Dict = None

    def parse_data(self,data):
        return data
    
    def compute(self,X,Y=None,**kwargs):
        
        distance = manhattan_distances(X=X,Y=Y)

        return {
            self.name : distance
        }