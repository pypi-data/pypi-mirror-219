from sklearn.metrics.pairwise import rbf_kernel
from typing import Any,Dict
from pureml_evaluate.metrics.metric_base import MetricBase


class RBFKernel(MetricBase):
    name = 'rbf_kernel'
    input_type = 'int'
    output_type: Any = None
    kwargs: Dict  = None

    def parse_data(self,data):
        return data
    
    def compute(self,X,Y=None,gamma = None,**kwargs):
        
        kernel = rbf_kernel(X=X,Y=Y,gamma=gamma)

        return {
            self.name : kernel
        }