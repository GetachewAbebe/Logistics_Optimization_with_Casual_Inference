import pandas as pd
from typing import List

class DataCleaning:
    def __init__(self) -> None:
        pass
    
    def drop_columns(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """
        Drops specified columns from the DataFrame.
        
        Parameters:
        df (pd.DataFrame): The input DataFrame.
        columns (List[str]): List of column names to be dropped.
        
        Returns:
        pd.DataFrame: DataFrame with specified columns dropped.
        """
        # Check if columns exist in DataFrame
        columns_to_drop = [col for col in columns if col in df.columns]
        return df.drop(columns=columns_to_drop, errors='ignore')
    
    def get_lat_long(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """
        Splits specified columns containing latitude and longitude into separate columns.
        
        Parameters:
        df (pd.DataFrame): The input DataFrame.
        columns (List[str]): List of column names containing lat-long values in 'lat,long' format.
        
        Returns:
        pd.DataFrame: DataFrame with new latitude and longitude columns.
        """
        for col in columns:
            if col in df.columns:
                df[col + '_lat'] = df[col].apply(lambda x: x.split(',')[0] if isinstance(x, str) and ',' in x else None)
                df[col + '_long'] = df[col].apply(lambda x: x.split(',')[1] if isinstance(x, str) and ',' in x else None)
        return df
