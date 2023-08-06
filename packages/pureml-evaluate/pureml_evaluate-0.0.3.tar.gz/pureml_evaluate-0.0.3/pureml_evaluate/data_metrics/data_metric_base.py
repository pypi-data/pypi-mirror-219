from typing import List, Dict, Any, Union, Optional
import pandas as pd
from pydantic import BaseModel
from abc import ABC, abstractmethod, abstractproperty


class DataMetricBase(BaseModel):
    name : str = 'data_duplicates'
    input_type : str = 'dataframe'
    output_type : str = 'dataframe'


    @abstractmethod
    def parse_data(self, data: pd.DataFrame, **kwargs) -> pd.DataFrame:
        return data
    
    @abstractmethod
    def compute(self, data: pd.DataFrame, **kwargs):
        return data
