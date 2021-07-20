# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 18:15:10 2020

@author: mehmet.karaca
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 17:11:29 2020

@author: sarik
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

# Neural network
model = Sequential([
  Dense(16,  input_dim=49, kernel_initializer='normal', activation='relu'),
  Dense(16, activation='relu'),
  #Dense(16, activation='relu'),
  Dense(1, activation='sigmoid'),
])


df = pd.read_csv('dataset1.csv')
df = df[df.columns.difference(['Unnamed: 0'])]



input_data =  df.iloc[:,:49].values
label_MOS = df['MOS'].values


train_X, val_X, train_y, val_y = train_test_split(input_data, label_MOS, test_size = 0.25, random_state = 14)

x_train = train_X 
y_train =  train_y

x_test =  val_X
y_test =  val_y


# COMPILE
keras.optimizers.Adam(
   learning_rate = 0.01, beta_1 = 0.9, beta_2 = 0.999, amsgrad = False
)
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mae'])


#TRAINING
history = model.fit(x_train, y_train, epochs=200, batch_size=20)

    
NNpredictions = model.predict(x_test) 


MAE = mean_absolute_error(val_y , NNpredictions)

print('Neural Network validation MAE = ',MAE)
RMSE = mean_squared_error(val_y , NNpredictions, squared = False)

print('Neural Network validation RMSE = ',RMSE)

ip = [RMSE]

#Write RMSE as input to other xApp
with open('input.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(ip)

# save ML model
model.save('TrainedMLmodel.h5')