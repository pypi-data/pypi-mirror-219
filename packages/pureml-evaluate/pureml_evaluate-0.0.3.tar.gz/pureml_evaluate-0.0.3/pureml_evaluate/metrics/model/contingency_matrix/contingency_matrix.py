from pureml_evaluate.metrics.metric_base import  MetricBase
from typing import Any,Dict
from sklearn.metrics.cluster import contingency_matrix
import numpy as np

class ContingencyMatrix(MetricBase):
    name = 'contingency_matrix'
    input_type = 'int'
    output_type: Any = None
    kwargs: Dict = None


    def parse_data(self,data):
        return data
    
    def compute(self,labels_true,labels_pred,eps=None,sparse=False,dtype = np.int64):

        result = contingency_matrix(labels_true=labels_true,labels_pred=labels_pred,eps=eps,sparse=sparse,dtype=dtype)

        return {
            self.name : result
        }
    