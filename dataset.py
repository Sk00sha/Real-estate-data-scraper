import pandas as pd
from helper import *

def constructDataFrame(dictOfContent:list)->pd.DataFrame:
    """
    Function creates pandas dataFrame from list of dictionaries

    returns: dataFrame
    """
    
    dataFrame=pd.DataFrame(dictOfContent)
    return dataFrame





