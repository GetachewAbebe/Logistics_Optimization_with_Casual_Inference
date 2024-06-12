import pandas as pd
class DataCleaning:
    def __init__(self) -> None:
        pass
    
    def drop_columns(self,df,columns:list)->pd.DataFrame:
        return df.drop(columns=columns)
    
    def get_lat_long(self,df,columns):
        for col in columns:
            df[col+'_lat'] = df[col].apply(lambda x:x.split(',')[0])
            df[col+'_long'] = df[col].apply(lambda x:x.split(',')[1])
        return df 