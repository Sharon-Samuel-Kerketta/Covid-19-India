import pandas as pd
import numpy as np
import requests
import lxml.html as lh
import matplotlib.pyplot as plt
import datetime 
import seaborn as sns

import os 
my_path_sheets = os.path.join(os.getcwd(),'Sheets\\')
my_path_viz = os.path.join(os.getcwd(),'Viz\\')



sns.set()

#fetching the data
url='https://www.mohfw.gov.in/'
page = requests.get(url)

#storing the page in a variable
doc = lh.fromstring(page.content)

#getting all the table elements
tr_elements = doc.xpath('//tr')

#init
total_states = len(tr_elements)
date = datetime.date.today()

# finding the footer
footer_index = 0

for i in range(0,total_states):
    if "Total#" in str(tr_elements[i][1].text_content()) :
        footer_index = i
        print(footer_index)
        break

def get_columns(index):
    states = []
    for data in tr_elements[1:footer_index-1]:
        states.append(str(data[1].text_content().strip()))
    states.append('Total')
    data = pd.DataFrame(columns=states)
    print(data)
    return data

def get_total(index):
    last=[]
    total = 0
    last = tr_elements[footer_index]
    total = int(last[index].text_content().strip())
    return total
    
def get_statewise(index):
    data = get_columns(index)
    col = {}
    for elements in tr_elements[1:footer_index-1]:
        try:
            col[elements[1].text_content().strip()] = int(elements[index].text_content())
        except :
            col[elements[1].text_content().strip()] = None
    col['Total'] = get_total(index)
    
    if list(col.keys()) == list(data.columns) :
        print("Great to Go!")
        data.loc[str(date)] = col
    else:
        print("Didn't Work")
    return data

def get_data(index):

    data = get_statewise(index)
    print(data)
    
    # storing the graph of data fetched
    # print_viz(dataframe)

    return data

#figures
def print_viz(dataframe):
    f = plt.figure(figsize=(10,8))
    f.add_subplot(311)
    plt.axes(axisbelow=True)
    plt.barh(dataframe.sort_values(dataframe.columns[2])["Name of State / UT"].values,dataframe.sort_values(dataframe.columns[2])[dataframe.columns[2]],color="darkcyan")
    plt.tick_params(size=5,labelsize = 8)
    plt.xlabel("Confirmed Cases",fontsize=12)
    plt.title("Top States",fontsize=12)
    plt.grid(alpha=0.3)
    cases = dataframe[dataframe.columns[2]]
    
    for i, v in enumerate(sorted(cases)):
        plt.text(v+0.2, i, str(round(v, 2)), color='steelblue', va="center")
    
    plt.savefig(my_path_viz+"Viz "+str(date)+'.png')

def broadcast():
    dataframe_for_active = get_data(2)
    dataframe_for_cured = get_data(3)
    dataframe_for_death = get_data(4)
    dataframe_for_positive = get_data(5)
    
    #For Creation of the sheet
    # dataframe.to_csv("covid19_death.csv")
    # dataframe.to_csv("covid19_cured.csv")
    # dataframe.to_csv("covid19_death.csv")
    # dataframe.to_csv("covid19_positive.csv")

    #For opening and editing the sheet
    dataframe_for_active.to_csv("covid19_active.csv",mode='a',header=None)
    dataframe_for_cured.to_csv("covid19_cured.csv",mode='a',header=None)
    dataframe_for_death.to_csv("covid19_death.csv",mode='a',header=None)
    dataframe_for_positive.to_csv("covid19_positive.csv",mode='a',header=None)


broadcast()

