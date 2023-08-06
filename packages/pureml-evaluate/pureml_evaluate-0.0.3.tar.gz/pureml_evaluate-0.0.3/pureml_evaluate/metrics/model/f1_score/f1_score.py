from typing import Any
from sklearn.metrics import f1_score
from pureml_evaluate.metrics.metric_base import MetricBase


class F1(MetricBase):

    name = 'f1'
    input_type = 'int'
    output_type: Any = None
    kwargs = { }
        

    def parse_data(self, data):
        
        return data



    def compute(self, predictions, references, labels=None, pos_label=1, average="binary", sample_weight=None, **kwargs):
        
        
        if 'kwargs' in kwargs and 'average' in kwargs['kwargs']:
            average = kwargs['kwargs']['average']
            
        score = f1_score(y_true=references, y_pred=predictions, labels=labels, 
                         pos_label=pos_label, average=average, sample_weight=sample_weight)
        
        # score = {
        #     self.name : float(score) if score.size == 1 else score
        #     }

        score = {
            self.name : {'value' : float(score) if score.size == 1 else score}
        }

        return score