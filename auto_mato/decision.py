# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 08:35:24 2021

@author: mehmet.karaca
"""

import pandas as pd


df = pd.read_csv('input.csv')
input_data =  df.columns[0]

data = float(input_data)

if data < 0.15:
    print(' RMSE is good enough, continue')


