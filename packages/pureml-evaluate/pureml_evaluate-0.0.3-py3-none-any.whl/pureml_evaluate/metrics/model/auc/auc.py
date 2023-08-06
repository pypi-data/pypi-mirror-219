
from sklearn.metrics import auc, roc_curve
from pureml_evaluate.metrics.metric_base import MetricBase

class AUC(MetricBase):
    name = 'auc'
    input_type = 'float'
    output_type = 'float'
    kwargs = { }
        

    def parse_data(self, data):
        
        return data



    def compute(self, references, predictions, pos_label=1, **kwargs):

        fpr, tpr, thresholds = roc_curve(references, predictions, pos_label=pos_label)


        score = auc(x=fpr, y=tpr)
        
        score = {
            self.name : float(score)
            }
 

        return score