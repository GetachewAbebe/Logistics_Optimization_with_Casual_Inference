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

    def calculate_distances(starting_coordinates, ending_coordinates):
        calculated_distances = []
        for i in range(len(starting_coordinates)):
            val = str(starting_coordinates[i]).split(',')
            starting_tuple = (val[0], val[1])
            val_end = str(ending_coordinates[i]).split(',')
            ending_tuple = (val_end[0], val_end[1])
            calculated_distances.append(distance.distance(starting_tuple, ending_tuple).km)
        return calculated_distances
