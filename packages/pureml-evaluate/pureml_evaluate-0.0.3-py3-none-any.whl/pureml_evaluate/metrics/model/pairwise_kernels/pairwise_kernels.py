from pureml_evaluate.metrics.metric_base import MetricBase
from sklearn.metrics.pairwise import pairwise_kernels
from typing import Any,Dict

class PairwiseKernels(MetricBase):
    name = 'pairwise_kernels'
    input_type = 'int'
    output_type: Any  = None
    kwargs: Dict = None

    def parse_data(self,data):
        return data
    
    def compute(self,X,Y=None,metric='linear',filter_params = False,n_jobs = None,**kwargs):

        kernel = pairwise_kernels(X=X,Y=Y,metric=metric,filter_params=filter_params,n_jobs=n_jobs)

        return {
            self.name : kernel
        }