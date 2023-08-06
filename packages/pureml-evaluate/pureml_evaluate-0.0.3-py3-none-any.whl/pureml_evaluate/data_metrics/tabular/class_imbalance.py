from typing import Any
import pandas as pd
from pureml_evaluate.data_metrics.data_metric_base import DataMetricBase

class ClassImbalance(DataMetricBase):
    name = 'class_imbalance'
    input_type = 'dataframe'
    output_type: Any = None

    def parse_data(self, data):
        return data

    def compute(self, data, n_top_labels=5, ignore_nan=True, **kwargs):
        class_imbalance = {}

        for column in data.columns:
            class_counts = data[column].value_counts(normalize=True, dropna=ignore_nan)
            class_counts = class_counts.round(2)
            class_imbalance[column] = class_counts.head(n_top_labels).to_dict()

        return {
            self.name: class_imbalance
        }
