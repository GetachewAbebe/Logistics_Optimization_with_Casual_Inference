import pandas as pd
from geopy.geocoders import Nominatim
from geopy import distance

class DataCleaning:
    def __init__(self) -> None:
        pass
    
    def drop_columns(self, df: pd.DataFrame, columns: list) -> pd.DataFrame:
        """
        Drop columns from the DataFrame.

        Params:
            df (pd.DataFrame): The input DataFrame.
            columns (list): List of column names to drop.

        Returns:
            pd.DataFrame: DataFrame with specified columns dropped.
        """
        return df.drop(columns=columns)
    
    def get_lat_long(self, df: pd.DataFrame, columns: list) -> pd.DataFrame:
        """
        Extract latitude and longitude from columns containing 'lat, long' format.

        Params:
            df (pd.DataFrame): The input DataFrame.
            columns (list): List of column names containing 'lat, long' strings.

        Returns:
            pd.DataFrame: DataFrame with new columns for latitude and longitude.
        """
        for col in columns:
            df[col+'_lat'] = df[col].apply(lambda x: x.split(',')[0])
            df[col+'_long'] = df[col].apply(lambda x: x.split(',')[1])
        return df

    def find_distance(self,df:pd.DataFrame,distance_col_name:str="distance",trip_origin_col_names:list=["trip_origin"],trip_destination_col_names:list=["trip_destination"]):
        if len(trip_destination_col_names) > 1 and len(trip_origin_col_names) > 1:
            df[distance_col_name]=df.apply(lambda x:distance.distance((x[trip_origin_col_names[0]],x[trip_origin_col_names[1]]), (x[trip_destination_col_names[0]],x[trip_destination_col_names[1]])).km,axis=1)
        else:
            df[distance_col_name]=df.apply(lambda x:distance.distance((x[trip_origin_col_names[0]]), (x[trip_destination_col_names[0]])).km,axis=1)
        return df