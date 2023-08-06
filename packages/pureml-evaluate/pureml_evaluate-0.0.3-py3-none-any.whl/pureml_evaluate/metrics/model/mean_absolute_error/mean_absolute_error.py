from sklearn.metrics import mean_absolute_error
from pureml_evaluate.metrics.metric_base import MetricBase
from typing import Any,Dict

class MeanAbsoluteError(MetricBase):

    name = 'mean_absolute_error'
    input_type = 'float'
    output_type: Any = None
    kwargs: Dict = None
        

    def parse_data(self, data):
        
        return data



    def compute(self, predictions, references, sample_weight=None, multioutput="uniform_average", **kwargs):
        
        score = mean_absolute_error(y_true=references, y_pred=predictions, sample_weight=sample_weight, multioutput=multioutput)
        
        score = {
            self.name : {'value' : score }
            }
 

        return score