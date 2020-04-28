# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 19:33:23 2020

@author: Kanmani
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 13:16:48 2020

@author: Kanmani
"""
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")

raw_data=pd.read_csv('https://api.covid19india.org/csv/latest/raw_data.csv')
#print(raw_data.shape)

#print(raw_data['Age Bracket'].unique())

null_age=raw_data['Age Bracket'].isnull()==True
nullage_data=raw_data[null_age]

age=raw_data['Age Bracket'].isnull()==False
age_data=raw_data[age]

below_10=pd.DataFrame(columns=raw_data.columns)
between_10_30=pd.DataFrame(columns=raw_data.columns)
between_30_60=pd.DataFrame(columns=raw_data.columns)
above_60=pd.DataFrame(columns=raw_data.columns)

groups=  ['below_10','between_10_30','between_30_60','above_60']     

age_list=list(age_data['Age Bracket'])
for i in range(len(age_list)):
    if'.' in age_list[i]:
        check=age_list[i].split('.')
        update=int(check[0])+1
        age_list[i]=str(update)
    if '-' in age_list[i]:
        check=age_list[i].split('-')
        update=int((int(check[0])+int(check[1]))/2)
        age_list[i]=str(update)
        
for i in range(len(age_list)):
    check_age=int(age_list[i])
    if check_age<10:
        below_10=below_10.append(age_data.iloc[i,:])
    elif 9<check_age<30:
        between_10_30=between_10_30.append(age_data.iloc[i,:])
    elif 29<check_age<60:
        between_30_60=between_30_60.append(age_data.iloc[i,:])
    else:
        above_60=above_60.append(age_data.iloc[i,:])
    
agegroups=[below_10,between_10_30,between_30_60,above_60]

count_groups=[below_10.shape[0],between_10_30.shape[0],between_30_60.shape[0],above_60.shape[0]]

deceased_count=[]
age_sp=[]
data_sp=[]
for agegroup in agegroups:
    is_confirmed=agegroup['Current Status']=='Hospitalized'
    is_recovered=agegroup['Current Status']=='Recovered'
    is_deceased=agegroup['Current Status']=='Deceased'
    
    Confirmed=agegroup[is_confirmed].shape[0]
    Recovered=agegroup[is_recovered].shape[0]
    Deceased=agegroup[is_deceased]
    deceased_count.append(Deceased.shape[0])
    data=pd.DataFrame(columns=['Date','Patient Number','Survived','Death','Hazard_rate','Survival_Probability(K_M)','Cum_HR','Survival_Probability(A_N)'],index=list(range(agegroup.shape[0])))
    
    data['Date']=list(agegroup['Date Announced'])
    data['Patient Number']=list(agegroup['Patient Number'])
    data['Survived'][0]=Confirmed+Recovered
    data['Survival_Probability(K_M)'][0]=1
    data['Survival_Probability(A_N)'][0]=1
    data['Hazard_rate'][0]=0
    data['Death'][0]=0
    data['Cum_HR'][0]=0
    
    for i in range(1,agegroup.shape[0]):
        if data['Patient Number'][i] in list(Deceased['Patient Number']):
            data['Death']=1
        else:
            data['Death']=0
        data['Survived'][i]=data['Survived'][i-1]-data['Death'][i]
        data['Hazard_rate'][i]=data['Death'][i]/data['Survived'][i-1]
        data['Cum_HR'][i]=data['Hazard_rate'][i]+data['Cum_HR'][i-1]
        data['Survival_Probability(K_M)'][i]=data['Survival_Probability(K_M)'][i-1]*(1-data['Hazard_rate'][i])
        data['Survival_Probability(A_N)'][i]=pow(math.e,(-1*data['Cum_HR'][i]))
        
    age_sp.append((data['Survival_Probability(K_M)'][i], data['Survival_Probability(A_N)'][i]))
    data_sp.append(data)

ind = np.arange(len(groups))
plt.figure(figsize=(10,10))
width = 0.3       

bar1=plt.bar(ind, count_groups , width, label='Confirmed')
bar2=plt.bar(ind + width, deceased_count, width, label='Deceased')

plt.ylabel('Cases_count')
plt.title('Confirmed and Deceased based on age group')

plt.xticks(ind + width / 2, groups)

for bar in bar1:
    yval = bar.get_height()
    plt.text(bar.get_x(), yval + .005, yval)
    
for bar in bar2:
    yval = bar.get_height()
    plt.text(bar.get_x(), yval + .005, yval)
plt.legend(loc='best')
plt.show()
i=0
while i<len(groups):
    plt.figure(figsize=(15,15))
    plt.subplot(2,2,1)
    plt.title(groups[i])
    plt.xlabel('Date')
    plt.ylabel('K_M')
    plt.step(data_sp[i]['Date'],data_sp[i]['Survival_Probability(K_M)'])
    plt.subplot(2,2,2)
    plt.xlabel('Date')
    plt.ylabel('A_N')
    plt.step(data_sp[i]['Date'],data_sp[i]['Survival_Probability(A_N)'])
    plt.show()
    i=i+1
    
Sur_prob=list(zip(groups,age_sp))
s_km=[]
s_an=[]
for i in age_sp:
    s_km.append(i[0])
    s_an.append(i[1])

plt.figure(figsize=(15,15))
plt.subplot(2,2,1)
plt.title('Kaplan Mier')    
plt.xlabel('age groups')
plt.ylabel('Sur_Prob_K_M')
plt.plot(groups,s_km,label='K_M')
plt.legend()
plt.show()

plt.figure(figsize=(15,15))
plt.subplot(2,2,2)
plt.title('Alder Nelson')
plt.xlabel('age groups')
plt.ylabel('Sur_Prob_A_N')
plt.plot(groups,s_an,label='A_N')
plt.legend()
plt.show()
