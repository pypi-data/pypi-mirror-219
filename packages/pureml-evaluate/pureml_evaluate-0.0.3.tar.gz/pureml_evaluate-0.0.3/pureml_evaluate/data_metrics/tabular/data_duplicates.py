import pandas as pd
import numpy as np
from pureml_evaluate.data_metrics.data_metric_base import DataMetricBase

class DataDuplicatesCheck(DataMetricBase):
    name = 'data_duplicates'
    input_type = 'dataframe'
    output_type = pd.DataFrame

    def parse_data(self, data):
        return data

    def compute(self, data, **kwargs):
        duplicates = data[data.duplicated(keep=False)]
        duplicates_count = duplicates.groupby(duplicates.columns.tolist()).size().reset_index(name='Number of Duplicates')
        duplicates_count['Entropy'] = duplicates_count.groupby(duplicates.columns.tolist())['Number of Duplicates'].transform(lambda x: -np.sum((x / x.sum()) * np.log2(x / x.sum())))
        duplicates_count['NumParams'] = duplicates_count[duplicates.columns.tolist()].apply(lambda x: len(set(x)), axis=1)

        return duplicates_count
