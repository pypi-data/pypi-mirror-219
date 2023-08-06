from abc import ABC, abstractmethod, abstractproperty
from pydantic import BaseModel
import typing


class MetricBase(ABC, BaseModel):
    name:str = 'accuracy'
    input_type:str = 'int'
    output_type:str = None
    kwargs:dict = None


    

    @abstractmethod
    def parse_data(self):
        pass

    @abstractmethod
    def compute(self):
        pass