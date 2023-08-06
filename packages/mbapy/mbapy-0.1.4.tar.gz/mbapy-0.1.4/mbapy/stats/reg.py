'''
Author: BHM-Bob 2262029386@qq.com
Date: 2023-04-06 20:44:44
LastEditors: BHM-Bob 2262029386@qq.com
LastEditTime: 2023-06-15 23:01:10
Description: 
'''
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

def linear_reg(x:str, y:str, df:pd.DataFrame):
    """
    Performs linear regression on two given columns of a pandas dataframe.

    :param x: A string representing the name of the independent variable column.
    :type x: str
    :param y: A string representing the name of the dependent variable column.
    :type y: str
    :param df: A pandas dataframe containing the two columns.
    :type df: pd.DataFrame
    :return: A dictionary containing the fitted regressor object, slope, intercept, and R-squared value.
    :rtype: dict
    """
    x = np.array(df[x]).reshape(-1, 1)
    y = np.array(df[y]).reshape(-1, 1)
    regressor = LinearRegression()
    regressor = regressor.fit(x, y)
    equation_a, equation_b = regressor.coef_.item(), regressor.intercept_.item()
    equation_r2 = regressor.score(x, y)
    return {
        'regressor':regressor,
        'a':equation_a,
        'b':equation_b,
        'r2':equation_r2,
    }
    
