from pureml_evaluate.metrics.metric_base import MetricBase
from sklearn.metrics.pairwise import laplacian_kernel
from typing import Any,Dict


class LaplacianKernel(MetricBase):
    name = 'laplacian_kernel'
    input_type = 'int'
    output_type: Any = None
    kwargs: Dict = None

    def parse_data(self,data):
        return data
    
    def compute(self,X,Y=None,gamma=None,**kwargs):
        
        kernel_matrix = laplacian_kernel(X=X,Y=Y,gamma=gamma)

        return {
            self.name : kernel_matrix
        }