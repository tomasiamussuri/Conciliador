import pandas as pd
from typing import List, Dict, Tuple

class DataPreprocessor:
    @staticmethod
    def convert_to_string(df: pd.DataFrame) -> pd.DataFrame:
        """Convert all columns to string type and clean the data"""
        df_processed = df.copy()
        for column in df_processed.columns:
            df_processed[column] = df_processed[column].fillna('')  # Lida com valores nulos
            df_processed[column] = df_processed[column].astype(str)
            df_processed[column] = df_processed[column].str.upper()
            df_processed[column] = df_processed[column].str.strip()
            df_processed[column] = df_processed[column].str.replace(r'\s+', ' ', regex=True)
        return df_processed

    @staticmethod
    def convert_to_date(df: pd.DataFrame, date_columns: List[str], formats: Dict[str, str]) -> pd.DataFrame:
        """Convert specified columns to a standard date format 'YYYY-MM-DD'"""
        df_processed = df.copy()
        for column in date_columns:
            if column in df_processed.columns:
                date_format = formats.get(column, '%Y-%m-%d')  # Default format if not specified
                df_processed[column] = pd.to_datetime(df_processed[column], format=date_format, errors='coerce').dt.strftime('%Y-%m-%d')
        return df_processed

    @staticmethod
    def add_unique_id(df: pd.DataFrame, prefix: str) -> pd.DataFrame:
        """Add a unique ID column to the dataframe"""
        df = df.copy()
        df['ID_' + prefix] = [f"{prefix}_{i:06d}" for i in range(len(df))]
        return df
