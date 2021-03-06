# -*- coding: utf-8 -*-
"""prediction.ipynb

Automatically generated by Colaboratory.

"""

## An inorganic ABX3 perovskite dataset for target property prediction and classification using machine learning

# AUTHOR - (1) * Ericsson Chenebuah, (1) Michel Nganbe and (2) Alain Tchagang 
# 1: Department of Mechanical Engineering, University of Ottawa, 75 Laurier Ave. East, Ottawa, ON, K1N 6N5 Canada
# 2: Digital Technologies Research Centre, National Research Council of Canada, 1200 Montréal Road, Ottawa, ON, K1A 0R6 Canada
# * email: echen013@uottawa.ca 
# (09-Feb-2022)

import pandas as pd
import pylab as pl
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
# %matplotlib inline 
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

df = pd.read_csv('oqmd_data.csv') #Reading the data

# Formation Energy Prediction. For Band gap change target (y) from 'Ef' to 'Eg' and include 'Ef' among inputs (X)
y = np.asarray(df['Ef'].astype('float64'))
X = np.asarray(df.drop(["name","entry_id","icsd_id","sg","cs","cs1","Ef","Eg"], 1))
X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.3, random_state=9)

# PREDICTION EXPERIMENT 1: Support Vector Regression (SVM)
#from sklearn.svm import SVR
#from sklearn.pipeline import make_pipeline
#from sklearn.preprocessing import StandardScaler
#regr = make_pipeline(StandardScaler(), SVR(C=100.0, epsilon=0.001, gamma='auto', kernel='rbf'))
#regr.fit(X_train, y_train)
#y_pred = regr.predict(X_test)

# PREDICTION EXPERIMENT 2: RANDOM FOREST (RFR)
#from sklearn.ensemble import RandomForestRegressor
#params = {'max_depth':None, 'random_state':6, 'criterion':'mse'}
#regr = RandomForestRegressor(**params)
#regr.fit(X_train, y_train)
#y_pred = regr.predict(X_test)

# PREDICTION EXPERIMENT 3: XGB0OST
#import xgboost
#regr = xgboost.XGBRegressor(n_estimators=1000)
#regr.fit(X_train, y_train)
#y_pred = regr.predict(X_test)

# PREDICTION EXPERIMENT 4: LGBM
import lightgbm
regr = lightgbm.LGBMRegressor(n_estimators=1000)
regr.fit(X_train, y_train)
y_pred = regr.predict(X_test)

# Evaluation
print('R-square: %.4f' % (r2_score(y_test, y_pred)*100))
print("Mean squared error: %.4f"% mean_squared_error(y_test, y_pred))
print("RMSE test: %.4f" % np.sqrt(mean_squared_error(y_test, y_pred)))
print("Mean absolute error: %.4f"% mean_absolute_error(y_test, y_pred))

# PLOT REGRESSION FITTING

fig, ax = plt.subplots()
ax.scatter(y_test, y_pred, color='magenta', s=3)
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=1)
ax.set_xlabel('Actual')
ax.set_ylabel('Predicted')
plt.xticks(fontsize=16, fontweight='bold')
plt.yticks(fontsize=16, fontweight='bold')

ax.text(0.095, 0.95, 'LGB',
        verticalalignment='top', horizontalalignment='left',
        transform=ax.transAxes,
        color='black', fontsize=30, fontweight='bold')

ax.text(-3.7, 0.5, r'$R^2=99.12\%$', fontsize=15, fontweight='bold')
plt.show()

