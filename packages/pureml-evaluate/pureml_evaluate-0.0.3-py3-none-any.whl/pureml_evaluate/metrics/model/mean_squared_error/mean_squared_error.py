from sklearn.metrics import mean_squared_error
from pureml_evaluate.metrics.metric_base import MetricBase
from typing import Any,Dict

class MeanSquaredError(MetricBase):

    name = 'mean_squared_error'
    input_type = 'float'
    output_type: Any = None
    kwargs: Dict = None
        

    def parse_data(self, data):
        
        return data



    def compute(self, predictions, references, sample_weight=None, multioutput="uniform_average", squared=True, **kwargs):

        score = mean_squared_error(y_true=references, y_pred=predictions, sample_weight=sample_weight,
                                    multioutput=multioutput, squared=squared)
        
        score = {
            self.name : {'value': score}
            }
 

        return score