import requests
import pandas as pd
import io
import datetime
import numpy as np

#insurance_visit
#RH
#PM
#children 
#week 
#temp

data = pd.read_csv('./taoyuan_data.csv')

#空氣品質監測月值
def aqm():
    #取得桃園測站的溫度、PM2.5、相對濕度資料
    get_aqm = requests.get("https://data.epa.gov.tw/api/v1/aqx_p_08?format=csv&limit=999&api_key=9be7b239-557b-4c10-9775-78cadfc555e9&filters=SiteId,EQ,17|ItemId,EQ,33,38,14").content
    aqm_rawdata = pd.read_csv(io.StringIO(get_aqm.decode('utf-8')))
    
    new_data = {
            'RH':[],
            'PM':[],
            'temp':[],
            '年月':[]     
            }
    
    for index,row in data[data['RH'].isnull()].iterrows():
        nullmonth = datetime.datetime.strptime(row['year-week']+'0', "%Y-%W%w").strftime("%Y%m")
        break
    for index,row in aqm_rawdata[pd.to_datetime(aqm_rawdata['MonitorMonth'], format = "%Y%m") >= datetime.datetime.strptime(nullmonth, "%Y%m")].iterrows():
        new_data['年月'].append(row['MonitorMonth'])
        if row['ItemId'] == 38:
            new_data['RH'].append(row['Concentration'])
        elif row['ItemId'] == 33:
            new_data['PM'].append(row['Concentration'])
        elif row['ItemId'] == 14:
            new_data['temp'].append(row['Concentration'])
            
    new_data['年月'] = np.unique(new_data['年月']).tolist()
    new_data_df = pd.DataFrame(new_data)
    new_data_df.set_index('年月' , inplace=True)
    
    for index,row in data[data['RH'].isnull()].iterrows():
        date_index = int(datetime.datetime.strptime(row['year-week']+'0', "%Y-%W%w").strftime("%Y%m"))
        if date_index in new_data_df.index:    
            data.at[index,'RH'] = new_data_df.loc[date_index,'RH']
            data.at[index,'PM'] = new_data_df.loc[date_index,'PM']
            data.at[index,'temp'] = new_data_df.loc[date_index,'temp'] 
    
    data.to_csv("taoyuan_data.csv",index=False,columns=['year-week','year','week','insurance_visit','PM','temp','RH','children'],sep=',')
    
    
#人口
def population(yearmonth):  #yearmonth:要下載的年月，格式為民國三碼+月分兩碼  
    get_population = requests.get("https://www.ris.gov.tw/info-popudata/app/awFastDownload/file/m0s7-"+yearmonth+".xls/m0s7/"+yearmonth+"/").content
    populaion_rawdata = pd.read_excel(get_population,encoding='utf-8')
    #桃園市0-5歲人口數總和
    child_population = int(populaion_rawdata.iloc[12,3]) + int(populaion_rawdata.iloc[12,10])
    #轉換年月計算週數
    year = 1911 + int(yearmonth[0:3])
    month = int(yearmonth[3:5])
    week = datetime.date(year ,month ,1).strftime("%Y-%V")
    next_month_week = datetime.date(year ,month+1 ,1).strftime("%Y-%V")

    for index,row in data[pd.to_datetime(data['year-week']+'0', format = "%Y-%W%w") >= datetime.datetime.strptime(week + '0', "%Y-%W%w") ].iterrows():
        if datetime.datetime.strptime(row['year-week']+'0', "%Y-%W%w") == datetime.datetime.strptime(next_month_week + '0', "%Y-%W%w"):
            break
        data.at[index, "children"] = child_population
    data.to_csv("taoyuan_data.csv",index=False,columns=['year-week','year','week','insurance_visit','PM','temp','RH','children'],sep=',')

    
#門診人次
def infect():
    #獲取最新資料
    NHI_EnteroviralInfection = requests.get("https://od.cdc.gov.tw/eic/NHI_EnteroviralInfection.csv").content
    NHI_E_rawdata = pd.read_csv(io.StringIO(NHI_EnteroviralInfection.decode('utf-8')))
    NHI_E_rawdata['年']=NHI_E_rawdata['年'].map(lambda x:str(x))
    NHI_E_rawdata['週']=NHI_E_rawdata['週'].map(lambda x:str(x))
    NHI_E_rawdata['年-週']=NHI_E_rawdata['年'].str.cat(NHI_E_rawdata['週'],sep='-')
    
    year_week=[]
    people_Infection=[]
    
    infection_dict = {
                "year-week": year_week,
                "insurance_visit": people_Infection,
                }
    infection_df = pd.DataFrame(infection_dict)
    
    #與舊資料合併    
    for index,row in NHI_E_rawdata[pd.to_datetime(NHI_E_rawdata['年-週']+'0', format = "%Y-%W%w") > datetime.datetime.strptime(data['year-week'].iloc[-1]+'0', "%Y-%W%w")].iterrows():
        if row['縣市']=="桃園市":
            year_week=row['年-週']
            people = row["腸病毒健保就診人次"]
            if year_week in infection_df["year-week"].values:
                infection_df.set_index("year-week" , inplace=True)
                infection_df.loc[year_week,"insurance_visit"]+=people
                infection_df.reset_index(inplace=True)
            else:
                new=pd.DataFrame({"year-week": year_week, "insurance_visit": people},index=[1])
                infection_df=infection_df.append(new,ignore_index=True)
       
    infection_df2=pd.DataFrame((x.split('-') for x in infection_df['year-week']),index=infection_df.index,columns=['year','week'])
    infection_df=pd.merge(infection_df2,infection_df,right_index=True, left_index=True)
    infection_df = pd.concat([data ,infection_df], join = 'outer')
    infection_df.to_csv("taoyuan_data.csv",index=False,columns=['year-week','year','week','insurance_visit','PM','temp','RH','children'],sep=',')