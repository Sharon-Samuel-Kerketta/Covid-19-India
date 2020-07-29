
import urllib.request, json 
import pandas as pd
import datetime

with urllib.request.urlopen("https://www.mohfw.gov.in/data/datanew.json") as url:
    raw_data = json.loads(url.read().decode())
    # print(raw_data)

data_df = pd.DataFrame(raw_data)
data_df = data_df.drop(['new_active', 'new_positive', 'new_cured', 'new_death', 'state_code'],axis=1)


# Todays date for Index
date = datetime.date.today()

# Daily Data Straight
data_df.to_csv(str(date)+'.csv',index = False)

# For Separate States
states = []
positive = []
cured = []
death = []
active = []


for dicts in raw_data:
    states.append(dicts['state_name'])
    positive.append(dicts['positive'])
    cured.append(dicts['cured'])
    death.append(dicts['death'])
    active.append(dicts['active'])


states_positive = pd.DataFrame(columns= states)
states_positive.loc[str(date)] =  positive

states_cured = pd.DataFrame(columns= states)
states_cured.loc[str(date)] =  cured

states_death = pd.DataFrame(columns= states)
states_death.loc[str(date)] =  death

states_active = pd.DataFrame(columns= states)
states_active.loc[str(date)] =  active

states_active.to_csv("covid19_active.csv",mode='a',header=None)
states_cured.to_csv("covid19_cured.csv",mode='a',header=None)
states_death.to_csv("covid19_death.csv",mode='a',header=None)
states_positive.to_csv("covid19_positive.csv",mode='a',header=None)