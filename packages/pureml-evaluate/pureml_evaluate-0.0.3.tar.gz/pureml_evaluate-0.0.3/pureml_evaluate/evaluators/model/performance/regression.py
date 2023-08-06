from pureml_evaluate.metrics.model.mean_absolute_error.mean_absolute_error import MeanAbsoluteError
from pureml_evaluate.metrics.model.mean_squared_error.mean_squared_error import MeanSquaredError
from pureml_evaluate.metrics.model.max_error.max_error import MaxError
from pureml_evaluate.metrics.model.r2_score.r2_score import R2Score
from pureml_evaluate.metrics.model.mean_squared_log_error.mean_squared_log_error import MeanSquaredLogError
from pureml_evaluate.metrics.model.median_absolute_error.median_absolute_error import MedianAbsoluteError
from pureml_evaluate.metrics.model.mean_poisson_deviance.mean_poisson_deviance import MeanPoissonDeviance
from pureml_evaluate.metrics.model.mean_gamma_deviance.mean_gamma_deviance import MeanGammaDeviance
from pureml_evaluate.metrics.model.mean_absolute_percentage_error.mean_absolute_percentage_error import MeanAbsolutePercentageError
from pureml_evaluate.metrics.model.d2_absolute_error_score.d2_absolute_error_score import D2AbsoluteErrorScore
from pureml_evaluate.metrics.model.d2_pinball_score.d2_pinball_score import D2PinballScore
from pureml_evaluate.metrics.model.d2_tweedie_score.d2_tweedie_score import D2TweedieScore
from pureml_evaluate.metrics.model.explained_variance_score.explained_variance_score import ExplainedVarianceScore

class Regression():
    def __init__(self):
        self.task_type = 'regression'
        self.evaluation_type = "performance"

        self.kwargs = None
        self.evaluator = None
        self.metrics = [MeanAbsoluteError(), MeanSquaredError(),R2Score(),MaxError(),MeanSquaredLogError(),MedianAbsoluteError(),
                        MeanPoissonDeviance(),MeanGammaDeviance(),MeanAbsolutePercentageError(),
                        D2AbsoluteErrorScore(),D2PinballScore(),D2TweedieScore(),ExplainedVarianceScore()]

        self.scores = {}

    def compute(self):

        for m in self.metrics:
            # Adding  prediction scores to kwargs. It will be utilized my metrics needing it(roc_auc).
            try:
                self.kwargs['prediction_scores'] = self.prediction_scores

                score = m.compute(references=self.references,
                                  predictions=self.predictions, **self.kwargs)

                self.scores.update(score)

            except Exception as e:
                print("Unable to compute", m)
                print(e)

        return self.scores
