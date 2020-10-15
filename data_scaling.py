    
"""
這部分是參考:https://ithelp.ithome.com.tw/articles/10216967?sc=rss.iron 進行處理
"""

from sklearn import preprocessing
import pandas as pd

df = pd.read_csv('./taoyuan_data.csv', usecols = ['insurance_visit','PM','temp','RH','children'])
df_date = pd.read_csv('./taoyuan_data.csv', usecols = ['year-week','year','week'])
#以平均值填補缺失值
df = df.fillna(df.mean())

def maxmin():
    #新資料=（原始資料-最小值）/（最大值-最小值）
    minmax = preprocessing.MinMaxScaler()
    data_minmax = minmax.fit_transform(df)
    data_minmax = pd.DataFrame({'insurance_visit': data_minmax[:, 0], 'PM': data_minmax[:, 1], 'temp': data_minmax[:, 2], 'RH': data_minmax[:, 3], 'children': data_minmax[:, 4]})
    data_minmax=pd.merge(df_date,data_minmax,right_index=True, left_index=True)
    data_minmax.to_csv("taoyuan_minmax.csv",index=False,columns=['year-week','year','week','insurance_visit','PM','temp','RH','children'],sep=',')
    
def zscore():
    #新資料=（原始資料-均值）/標準差
    zscore = preprocessing.StandardScaler()
    data_zs = zscore.fit_transform(df)
    data_zs = pd.DataFrame({'insurance_visit': data_zs[:, 0], 'PM': data_zs[:, 1], 'temp': data_zs[:, 2], 'RH': data_zs[:, 3], 'children': data_zs[:, 4]})
    data_zs=pd.merge(df_date,data_zs,right_index=True, left_index=True)
    data_zs.to_csv("taoyuan_zscore.csv",index=False,columns=['year-week','year','week','insurance_visit','PM','temp','RH','children'],sep=',')
    
def maxabs():
    #新資料 = 原始資料 / |原始資料的最大值|
    maxabs = preprocessing.MaxAbsScaler()
    data_maxabs = maxabs.fit_transform(df)
    data_maxabs = pd.DataFrame({'insurance_visit': data_maxabs[:, 0], 'PM': data_maxabs[:, 1], 'temp': data_maxabs[:, 2], 'RH': data_maxabs[:, 3], 'children': data_maxabs[:, 4]})
    data_maxabs=pd.merge(df_date,data_maxabs,right_index=True, left_index=True)
    data_maxabs.to_csv("taoyuan_maxabs.csv",index=False,columns=['year-week','year','week','insurance_visit','PM','temp','RH','children'],sep=',')

def robustscaler():
    robust = preprocessing.RobustScaler()
    data_rob = robust.fit_transform(df)
    data_rob = pd.DataFrame({'insurance_visit': data_rob[:, 0], 'PM': data_rob[:, 1], 'temp': data_rob[:, 2], 'RH': data_rob[:, 3], 'children': data_rob[:, 4]})
    data_rob=pd.merge(df_date,data_rob,right_index=True, left_index=True)
    data_rob.to_csv("taoyuan_robustscaler.csv",index=False,columns=['year-week','year','week','insurance_visit','PM','temp','RH','children'],sep=',')

