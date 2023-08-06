import pandas as pd
from pureml_evaluate.data_metrics.data_metric_base import DataMetricBase
from typing import Any

class FeatureFeatureCorrelation(DataMetricBase):
    name = 'feature_feature_correlation'
    input_type = 'dataframe'
    output_type: Any = pd.DataFrame

    def parse_data(self, data):
        return data

    def compute(self, data, **kwargs):
        correlation_matrix = data.corr()

        return correlation_matrix