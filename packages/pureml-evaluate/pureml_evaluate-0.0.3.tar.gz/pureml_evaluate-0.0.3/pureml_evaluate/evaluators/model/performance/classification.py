from pureml_evaluate.metrics.model.accuracy.accuracy import Accuracy
from pureml_evaluate.metrics.model.precision.precision import Precision
from pureml_evaluate.metrics.model.recall.recall import Recall
from pureml_evaluate.metrics.model.f1_score.f1_score import F1
from pureml_evaluate.metrics.model.confusion_matrix.confusion_matrix import ConfusionMatrix
from pureml_evaluate.metrics.model.balanced_accuracy_score.balanced_accuracy_score import BalancedAccuracyScore
from pureml_evaluate.metrics.model.top_k_accuracy_score.top_k_accuracy_score import TopKAccuracyScore
from pureml_evaluate.metrics.model.log_loss.log_loss import LogLoss
from pureml_evaluate.metrics.model.roc_auc.roc_auc import ROC_AUC
from pureml_evaluate.metrics.model.average_precision_score.average_precision_score import AveragePrecisionScore
from pureml_evaluate.metrics.model.brier_score_loss.brier_score_loss import BrierScoreLoss

class Classification:
    def __init__(self):
        self.task_type = "classification"
        self.evaluation_type = "performance"

        self.kwargs = {}

        self.references = None
        self.predictions = None
        self.prediction_scores = None

        self.label_type = "binary"

        self.metrics = [
            Accuracy(),
            Precision(),
            Recall(),
            F1(),
            #ConfusionMatrix(),
            BalancedAccuracyScore(),
            TopKAccuracyScore(),
            LogLoss(),
            AveragePrecisionScore(),
          ROC_AUC()
          ]
        self.scores = {}

    def compute(self):
        self.setup()
        if self.label_type == 'binary':   #To Get results for BrierScoreLoss. As it supports only for binary classification
            self.metrics.append(BrierScoreLoss())
        

        for m in self.metrics:
            # Adding  prediction scores to kwargs. It will be utilized my metrics needing it(roc_auc).

            try:

                self.kwargs["prediction_scores"] = self.prediction_scores
                score = m.compute(
                    references=self.references, predictions=self.predictions, kwargs=self.kwargs
                )
                # **self.kwargs is changed to kwargs=self.kwargs. As **self.kwargs when passed to compute function is having type None.

                self.scores.update(score)
            except Exception as e:
                print("Unable to compute", m)
                print(f"Exception: {e}")

        return self.scores

    def setup(self):
        self.is_multiclass()
        self.setup_kwargs()

    def get_predictions(self):
        pass

    def is_multiclass(self):
        # print(self.predictions)
        # print(self.references)
        if self.predictions is not None:
            self.references = tuple(self.references)
            self.predictions = tuple(self.predictions)
            labels_all = set(self.references).union(self.predictions)
            if len(labels_all) > 2:
                self.label_type = "multilabel"
            

    def setup_kwargs(self):
        if "average" not in self.kwargs:
            if self.label_type == "multilabel":
                self.kwargs["average"] = "micro"
    