from pureml_evaluate.data_metrics.data_metric_base import DataMetricBase
from typing import Any

class ConflictingLabels(DataMetricBase):
    name = 'conflicting_labels'
    input_type = 'dataframe'
    output_type: Any = None

    def parse_data(self, data):
        return data

    def compute(self, data, **kwargs):
        conflicting_samples = {}

        # Check for conflicts in identical samples based on the first column
        duplicate_samples = data[data.duplicated(subset=[data.columns[0]], keep=False)]
        if not duplicate_samples.empty:
            grouped_data = duplicate_samples.groupby(data.columns[0])
            for group_value, group in grouped_data:
                conflicting_samples[group_value] = group.iloc[:, 1:].values.tolist()

        percent_of_conflicting_samples = len(conflicting_samples) / data.shape[0]

        return {
            self.name: conflicting_samples,
            'percent_of_conflicting_samples': percent_of_conflicting_samples
        }
