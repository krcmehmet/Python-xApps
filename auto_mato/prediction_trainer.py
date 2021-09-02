# -*- coding: utf-8 -*-
"""
prediction_trainer.py

@author: Team AutoMato
"""
import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF
from sklearn.gaussian_process.kernels import WhiteKernel, ExpSineSquared, ConstantKernel
from sklearn.metrics import mean_absolute_error

# TODO: Needs refactoring

sns.set_style(
    style='darkgrid',
    rc={'axes.facecolor': '.9', 'grid.color': '.8'}
)
sns.set_palette(palette='deep')
sns_c = sns.color_palette(palette='deep')

plt.rcParams['figure.figsize'] = [12, 6]
plt.rcParams['figure.dpi'] = 100

# Number of samples.
n = 150
# Time
t = np.arange(n)

data_df = pd.DataFrame({'t': t})

df = pd.read_csv('/Users/mehmetkrc/Desktop/built-a-thon/Python-xApps/data/pla.csv')
df = df[df.columns.difference(['Unnamed: 0'])]

input_data = df.iloc[:, :1].values
label_PRB = df['prb_utilization_perc'].values


# PRB data.
def seasonal(t, amplitude, period):
    """PRB unilization."""
    # y1 = amplitude * np.sin((2*np.pi)*t/period)
    y1 = label_PRB[t] - 25
    return y1


# Time and PRB values
data_df['s1'] = data_df['t'].apply(lambda t: seasonal(t, amplitude=2, period=40))

# Define target variable.
data_df['y1'] = data_df['s1']

fig, ax = plt.subplots()
sns.lineplot(x='t', y='s1', data=data_df, color=sns_c[0], label='s1', ax=ax)
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax.set(title='PRB Component', xlabel='t', ylabel='')

# Set noise standard deviation.
sigma_n = 0.0

data_df['epsilon'] = np.random.normal(loc=0, scale=sigma_n, size=n)
# Add noise to target variable.
data_df['y1'] = data_df['y1'] + data_df['epsilon']

fig, ax = plt.subplots()
sns.lineplot(x='t', y='y1', data=data_df, color=sns_c[0], label='y1', ax=ax)
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax.set(title='Sample Data 1', xlabel='t', ylabel='')

k0 = WhiteKernel(noise_level=0.3 ** 2, noise_level_bounds=(0.1 ** 2, 0.5 ** 2))

k1 = ConstantKernel(constant_value=2) * \
     ExpSineSquared(length_scale=1.0, periodicity=0.1, periodicity_bounds=(0.01, 45))

k2 = ConstantKernel(constant_value=10, constant_value_bounds=(1e-2, 1e3)) * \
     RBF(length_scale=1e2, length_scale_bounds=(1, 1e3))

kernel_1  = k1

gp1 = GaussianProcessRegressor(
    kernel=kernel_1,
    n_restarts_optimizer=10,
    normalize_y=True,
    alpha=0.0
)

X = data_df['t'].values.reshape(n, 1)
y = data_df['y1'].values.reshape(n, 1)

prop_train = 0.6
n_train = round(prop_train * n)

X_train = X[:n_train]
y_train = y[:n_train]

X_test = X[n_train:]
y_test = y[n_train:]

gp1_prior_samples = gp1.sample_y(X=X_train, n_samples=100)

fig, ax = plt.subplots()
for i in range(100):
    sns.lineplot(x=X_train[..., 0], y=gp1_prior_samples[:, i], color=sns_c[1], alpha=0.2, ax=ax)
sns.lineplot(x=X_train[..., 0], y=y_train[..., 0], color=sns_c[0], label='y1', ax=ax)
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax.set(title='GP1 Prior Samples', xlabel='t')

gp1.fit(X_train, y_train)

with open("/Users/mehmetkrc//Desktop/built-a-thon/Python-xApps/data/basic_prediction_model.pkl", "wb") as f:
    pickle.dump(gp1, f)
#np.save("/Users/mehmetkrc//Desktop/build-a-thon/Python-xApps/data/input_time_series", y)
y_pred, y_std = gp1.predict(X, return_std=True)

data_df['y_pred'] = y_pred
data_df['y_std'] = y_std
data_df['y_pred_lwr'] = data_df['y_pred'] - 2 * data_df['y_std']
data_df['y_pred_upr'] = data_df['y_pred'] + 2 * data_df['y_std']

fig, ax = plt.subplots()

ax.fill_between(
    x=data_df['t'],
    y1=data_df['y_pred_lwr'],
    y2=data_df['y_pred_upr'],
    color=sns_c[2],
    alpha=0.15,
    label='credible_interval'
)

sns.lineplot(x='t', y='y1', data=data_df, color=sns_c[0], label='y1', ax=ax)
sns.lineplot(x='t', y='y_pred', data=data_df, color=sns_c[2], label='y_pred', ax=ax)

ax.axvline(n_train, color=sns_c[3], linestyle='--', label='train-test split')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax.set(title='Prediction Sample 1', xlabel='t', ylabel='')

print(f'R2 Score Train = {gp1.score(X=X_train, y=y_train): 0.3f}')
print(f'R2 Score Test = {gp1.score(X=X_test, y=y_test): 0.3f}')
print(f'MAE Train = {mean_absolute_error(y_true=y_train, y_pred=gp1.predict(X_train)): 0.3f}')
print(f'MAE Test = {mean_absolute_error(y_true=y_test, y_pred=gp1.predict(X_test)): 0.3f}')
