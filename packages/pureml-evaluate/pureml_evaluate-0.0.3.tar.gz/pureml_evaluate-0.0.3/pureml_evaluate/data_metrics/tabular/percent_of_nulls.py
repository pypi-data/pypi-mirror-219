from pureml_evaluate.data_metrics.data_metric_base import DataMetricBase
import pandas as pd
import numpy as np
from collections import defaultdict
from typing import Any

class PercentOfNulls(DataMetricBase):
    name = 'percent_of_nulls'
    input_type = 'dataframe'
    output_type:Any = None


    def parse_data(self,data):
        return data
    
    def compute(self,data,**kwargs):

    
        data_columns = data.columns
        data_columns = data_columns.tolist()

        columns_result = {} 
        for i in data_columns:
            columns_result[i] = data[i].isnull().sum()/len(data[i])*100

        return {
            self.name : columns_result
        }