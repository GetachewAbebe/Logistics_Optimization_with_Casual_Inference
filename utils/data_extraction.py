import imp

import pandas as pd

class DataExtraction:
    def __init__(self) -> None:
        pass
    
    def load_data(self,filepath:str)->pd.DataFrame:
        return  pd.read_csv(filepath)