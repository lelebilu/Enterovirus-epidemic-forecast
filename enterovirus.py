# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 18:12:46 2019

@author: 史家瑩
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV
from sklearn.linear_model import LinearRegression
from sklearn import ensemble, metrics
from sklearn.metrics import r2_score
from sklearn.svm import SVR
from xgboost import XGBRegressor
from xgboost.sklearn import XGBClassifier
from sklearn.ensemble import RandomForestRegressor

from sklearn.ensemble import ExtraTreesClassifier

import xgboost as xgb

# 載入資料
enterovirus_train = pd.read_csv('taoyuan_data.csv')

# 建立訓練與測試資料
enterovirus_X = pd.DataFrame([enterovirus_train["week"]
                            , enterovirus_train["temp"]
                            , enterovirus_train["PM"]
                            , enterovirus_train["children"]
                            , enterovirus_train["RH"]
                            
]).T
enterovirus_y = enterovirus_train["insurance_visit"]
train_X, test_X, train_y, test_y = train_test_split(enterovirus_X, enterovirus_y, test_size = 0.3)


forest = RandomForestRegressor(n_estimators=100)

forest.fit(train_X, train_y)
importances = forest.feature_importances_
std = np.std([tree.feature_importances_ for tree in forest.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]

# Print the feature ranking
print("Feature ranking:")

for f in range(train_X.shape[1]):
    print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

# Plot the impurity-based feature importances of the forest
plt.figure()
plt.title("Feature importances")
plt.bar(range(train_X.shape[1]), importances[indices],
        color="r", yerr=std[indices], align="center")
plt.xticks(range(train_X.shape[1]), indices)
plt.xlim([-1, train_X.shape[1]])
plt.show()


#建立 Linear Regression 模型
lin_reg = LinearRegression()
lin_reg.fit(train_X, train_y)

# 預測
lin_reg_predicted = lin_reg.predict(test_X)
print('====Linear Regression====')
print('RMSE is ：', np.sqrt(metrics.mean_squared_error(test_y, lin_reg_predicted)))
print('r2_score is ：', r2_score(test_y, lin_reg_predicted))

# 建立 random forest 模型
forest = RandomForestRegressor(n_estimators = 100)
forest_fit = forest.fit(train_X, train_y)

forest_predicted = forest.predict(test_X)
print('====Random Forest====')
print('RMSE is ：', np.sqrt(metrics.mean_squared_error(test_y, forest_predicted)))
print('r2_score is ：', r2_score(test_y, forest_predicted))



svm = SVR(kernel='rbf', C=1e3, gamma=0.1)
svm.fit(train_X, train_y)

svm_predicted = svm.predict(test_X)
print('====SVM====')
print('RMSE is ：', np.sqrt(metrics.mean_squared_error(test_y, svm_predicted)))
print('r2_score is ：', r2_score(test_y, svm_predicted))
 


xgb_reg = xgb.XGBRegressor(objective="reg:linear", random_state=0)
xgb_reg.fit(train_X, train_y)
'''
xgb_reg.get_booster().get_score(importance_type='total_cover')
xgb_reg.feature_importances
'''
sorted_idx = xgb_reg.feature_importances_.argsort()
plt.barh(train_X.columns[sorted_idx], xgb_reg.feature_importances_[sorted_idx])
plt.xlabel("Xgboost Feature Importance")
plt.gca().set_position([0,0,1,1])
plt.savefig("123.svg")

xgb_predicted = xgb_reg.predict(test_X)
print('====XGBoost====')
print('RMSE is ：', np.sqrt(metrics.mean_squared_error(test_y, xgb_predicted)))
print('r2_score is ：', r2_score(test_y, xgb_predicted))
'''
plt.plot(test_X.index, xgb_predicted, 'r+', label='prediction model')
plt.plot(test_X.index, test_y, 'bo', label='actual model') 
'''