import pandas as pd
import requests
import lxml.html as lh
import matplotlib.pyplot as plt
import datetime 
import seaborn as sns

import os 
# my_path_sheets = os.path.join(os.getcwd(),'Sheets\\')
# my_path_viz = os.path.join(os.getcwd(),'Viz\\')



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

def get_header():
    header = []
    for data in tr_elements[0]:
        header.append((data.text_content().strip(),[]))
    print(header)
    return header

def get_footer():
    last=[]
    last_row = get_header()
    # last = tr_elements[:][0].text_content().str.contains("Total number of confirmed")
    last = tr_elements[footer_index]
    last_row[0][1].append(str())
    last_row[1][1].append(str(last[1].text_content()).strip())
    last_row[2][1].append(str(last[2].text_content()).strip())
    last_row[3][1].append(str(last[3].text_content()).strip())
    last_row[4][1].append(str(last[4].text_content()).strip())
    print("\nLast Row:\n",last_row) 
    data = { column:data for (column,data) in last_row }
    last_dataframe = pd.DataFrame(data)
    return last_dataframe
    

def get_statewise():
    col= get_header()
    for elements in tr_elements[1:footer_index-1]:
        try:
            col[0][1].append(int(elements[0].text_content()))
        except :
            col[0][1].append(None)

        try:
            col[1][1].append(elements[1].text_content())
        except :
            col[1][1].append(None)
        
        try:
            col[2][1].append(int(elements[2].text_content()))
        except :
            col[2][1].append(None)
        
        try:
            col[3][1].append(int(elements[3].text_content()))
        except :
            col[3][1].append(None)

        try:
            col[4][1].append(int(elements[4].text_content()))
        except :

            col[4][1].append(None)
        
    return col

def get_data():
    col = get_statewise()

    #converting the data into dictionary type
    data = { column:data for (column,data) in col }

    #converting the data dictionary into dataframe
    dataframe = pd.DataFrame(data)
    dataframe = dataframe.sort_values([dataframe.columns[2]], ascending=False)
    
    # storing the graph of data fetched
    print_viz(dataframe)

    return dataframe

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
    
    plt.savefig("Viz "+str(date)+'.png')

def broadcast():
    dataframe = get_data()
    dataframe.to_csv(str(date)+".csv",index=False)
    last_dataframe = get_footer()
    last_dataframe.to_csv(str(date)+".csv",mode='a',header=None,index=False)

broadcast()

