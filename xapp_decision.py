# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 08:35:24 2021

@author: mehmet.karaca
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error 
import xgboost
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
import torch
import torch.nn as nn
import torch.nn.functional as F
from datetime import datetime, timedelta
from sklearn.preprocessing import StandardScaler
from torch.autograd import Variable
import time
import random
import torch.optim as optim
import torch.utils.data as Data

from numpy import loadtxt

import keras
from keras.models import Sequential
from keras.layers import Dense

import pathlib
import matplotlib.pyplot as plt
import seaborn as sns


import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers

import csv

df = pd.read_csv('input.csv')
input_data =  df.columns[0]

data = float(input_data)

if data < 0.15:
    print(' RMSE is good enough, continue')


