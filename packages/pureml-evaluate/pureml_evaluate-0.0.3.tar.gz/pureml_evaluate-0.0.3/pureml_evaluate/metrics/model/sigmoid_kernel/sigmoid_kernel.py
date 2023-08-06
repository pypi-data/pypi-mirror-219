from pureml_evaluate.metrics.metric_base import MetricBase
from typing import Any,Dict
from sklearn.metrics.pairwise import sigmoid_kernel


class SigmoidKernel(MetricBase):
    name = 'sigmoid_kernel'
    input_type = 'int'
    output_type: Any = None
    kwargs: Dict = None


    def parse_data(self,data):
        return data
    
    def compute(self,X, Y=None, gamma=None, coef0=1,**kwargs):

        kernel = sigmoid_kernel(X=X,Y=Y,gamma=gamma,coef0=coef0)

        return {
            self.name : kernel
        }