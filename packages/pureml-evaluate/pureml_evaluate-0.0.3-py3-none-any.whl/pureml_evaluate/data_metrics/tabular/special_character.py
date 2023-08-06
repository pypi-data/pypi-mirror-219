import pandas as pd
from pureml_evaluate.data_metrics.data_metric_base import DataMetricBase
from typing import Any

class SpecialCharacters(DataMetricBase):
    name = 'special_characters'
    input_type = 'dataframe'
    output_type: Any = pd.DataFrame

    def parse_data(self, data):
        return data

    def compute(self, data, **kwargs):
        special_characters_info = []

        for column in data.columns:
            total_entries = len(data[column])
            special_character_entries = self.count_special_character_entries(data[column])
            special_character_percentage = (special_character_entries / total_entries) * 100

            special_characters_info.append({
                'Column': column,
                'Special_Character_Count': special_character_entries,
                'Total_Count': total_entries,
                'Special_Character_Percentage': special_character_percentage
            })

        result_df = pd.DataFrame(special_characters_info)

        return result_df

    def count_special_character_entries(self, column):
        pattern = r'^[\W_]+$'  # Match only special characters
        return column.astype(str).str.match(pattern).sum()
