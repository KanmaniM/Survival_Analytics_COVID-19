# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 19:16:17 2020

@author: Kanmani
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 10:19:12 2020

@author: Kanmani
"""

import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np

import warnings
warnings.filterwarnings("ignore")

raw_data=pd.read_csv('https://api.covid19india.org/csv/latest/raw_data.csv')

group_data=raw_data.groupby(raw_data['Gender'])

genders=['M','F']
expansion={'M':'MALE','F':'FEMALE'}
s_p={}
data_gender={}
deceased_count=[]
confirmed_count=[]
s_km=[]
s_an=[]
for gender in genders:
    gender_data=group_data.get_group(gender)
    confirmed_count.append(gender_data.shape[0])
    is_confirmed=gender_data['Current Status']=='Hospitalized'
    is_recovered=gender_data['Current Status']=='Recovered'
    is_deceased=gender_data['Current Status']=='Deceased'
    
    Confirmed=gender_data[is_confirmed].shape[0]
    Recovered=gender_data[is_recovered].shape[0]
    Deceased=gender_data[is_deceased]
    deceased_count.append(Deceased.shape[0])
    data=pd.DataFrame(columns=['Date','Patient Number','Survived','Death','Hazard_rate','Survival_Probability(K_M)','Cum_HR','Survival_Probability(A_N)'],index=list(range(gender_data.shape[0])))
    
    data['Date']=list(gender_data['Date Announced'])
    data['Patient Number']=list(gender_data['Patient Number'])
    data['Survived'][0]=Confirmed+Recovered
    data['Survival_Probability(K_M)'][0]=1
    data['Survival_Probability(A_N)'][0]=1
    data['Hazard_rate'][0]=0
    data['Death'][0]=0
    data['Cum_HR'][0]=0
    
    for i in range(1,gender_data.shape[0]):
        if data['Patient Number'][i] in list(Deceased['Patient Number']):
            data['Death']=1
        else:
            data['Death']=0
        data['Survived'][i]=data['Survived'][i-1]-data['Death'][i]
        data['Hazard_rate'][i]=data['Death'][i]/data['Survived'][i-1]
        data['Cum_HR'][i]=data['Hazard_rate'][i]+data['Cum_HR'][i-1]
        data['Survival_Probability(K_M)'][i]=data['Survival_Probability(K_M)'][i-1]*(1-data['Hazard_rate'][i])
        data['Survival_Probability(A_N)'][i]=pow(math.e,(-1*data['Cum_HR'][i]))
        
    s_p[gender]=(data['Survival_Probability(K_M)'][i], data['Survival_Probability(A_N)'][i])
    s_km.append(data['Survival_Probability(K_M)'][i])
    s_an.append(data['Survival_Probability(A_N)'][i])
    data_gender[gender]=data
   
ind = np.arange(len(genders))
plt.figure(figsize=(10,10))
width = 0.3       

bar1=plt.bar(ind, confirmed_count , width, label='Confirmed')
bar2=plt.bar(ind + width, deceased_count, width, label='Deceased')

plt.ylabel('Cases_count')
plt.title('Confirmed and Deceased based on gender')

plt.xticks(ind + width / 2, genders)

for bar in bar1:
    yval = bar.get_height()
    plt.text(bar.get_x(), yval + .005, yval)
    
for bar in bar2:
    yval = bar.get_height()
    plt.text(bar.get_x(), yval + .005, yval)
plt.legend(loc='best')
plt.show()

for gender in genders:
    plt.figure(figsize=(15,15))
    exp=expansion[gender]
    plt.subplot(2,2,1)
    plt.title(exp)
    plt.xlabel('Date')
    plt.ylabel('K_M')
    plt.step(data_gender[gender]['Date'],data_gender[gender]['Survival_Probability(K_M)'])
    plt.subplot(2,2,2)
    plt.xlabel('Date')
    plt.ylabel('A_N')
    plt.step(data_gender[gender]['Date'],data_gender[gender]['Survival_Probability(A_N)'])
    plt.show()

plt.figure(figsize=(15,15))
plt.subplot(2,2,1)
plt.title('Kaplan Mier')    
plt.xlabel('Gender')
plt.ylabel('Sur_Prob_K_M')
plt.plot(genders,s_km,label='K_M')
plt.legend()

plt.subplot(2,2,2)

plt.xlabel('Gender')
plt.ylabel('Sur_Prob_A_N')
plt.plot(genders,s_an,label='A_N')
plt.legend()

print('Sr_Probs')
print(s_p)