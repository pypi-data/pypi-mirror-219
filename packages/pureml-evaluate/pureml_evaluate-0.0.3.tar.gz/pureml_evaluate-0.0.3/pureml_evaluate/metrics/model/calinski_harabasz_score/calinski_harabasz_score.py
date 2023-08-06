from pureml_evaluate.metrics.metric_base import MetricBase
from typing import Any,Dict
from sklearn.metrics import calinski_harabasz_score


class CalinskiHarabaszScore(MetricBase):
    name = 'calinski_harabasz_score'
    input_type = 'int'
    output_type: Any = None
    kwargs: Dict = None


    def parse_data(self,data):
        return data
    

    def compute(self,X,labels,**kwargs):

        score = calinski_harabasz_score(X=X,labels=labels)

        score = {
            self.name : float(score)
        }

        return score
    