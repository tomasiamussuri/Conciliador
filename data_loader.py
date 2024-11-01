import pandas as pd
from typing import Tuple
from data_preprocessor import DataPreprocessor

class DataLoader:
    def __init__(self):
        self.preprocessor = DataPreprocessor()

    def load_and_prepare_data(self, file, base_type: str) -> Tuple[pd.DataFrame, str]:
        """Load and preprocess Excel file"""
        try:
            df = pd.read_excel(file)
            df = self.preprocessor.add_unique_id(df, base_type.upper())

            # Apply transformations based on the base type
            if base_type.lower() == 'gama':
                df = self.preprocessor.clean_cpf_column(df, 'cpfusu')
                df = self.preprocessor.convert_to_date(df, ['data_inicio_vigencia'], {'data_inicio_vigencia': '%Y-%m-%d'})
            
            # Convert all columns to string after transformations
            df = self.preprocessor.convert_to_string(df)

            # Add columns for matched IDs
            df['MATCHED_ID'] = None
            df['MATCH_RULE'] = None

            return df, None
        except Exception as e:
            return None, str(e)
