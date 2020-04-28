# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 19:14:54 2020

@author: Kanmani
"""

import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import warnings
warnings.filterwarnings("ignore")

total=pd.read_csv('https://api.covid19india.org/csv/latest/case_time_series.csv')

Confirmed=list(total['Total Confirmed'])
Recovered=list(total['Total Recovered'])
Deceased=list(total['Total Deceased'])

X = np.arange(len(Confirmed))

fig = plt.figure(figsize=(10,10))
ax = fig.add_axes([0,0,1,1])
ax.bar(X + 0.00, Confirmed, color = 'b', width = 0.25,label='Confirmed')
ax.bar(X + 0.25, Recovered, color = 'g', width = 0.25,label='Recoverd')
ax.bar(X + 0.50, Deceased, color = 'r', width = 0.25,label='Deaths')
ax.legend()
plt.title('Cummulative')


D_Confirmed=list(total['Daily Confirmed'])
D_Recovered=list(total['Daily Recovered'])
D_Deceased=list(total['Daily Deceased'])
X = np.arange(len(D_Confirmed))
fig = plt.figure(figsize=(10,10))
ax = fig.add_axes([0,0,1,1])
ax.bar(X + 0.00, D_Confirmed, color = 'b', width = 0.25,label='Confirmed')
ax.bar(X + 0.25, D_Recovered, color = 'g', width = 0.25,label='Recoverd')
ax.bar(X + 0.50, D_Deceased, color = 'r', width = 0.25,label='Deaths')
ax.legend()
plt.title('Daily')

data=pd.DataFrame(columns=['Date', 'Survived','Death','Hazard_rate','Survival_Probability(K_M)','Cum_HR','Survival_Probability(A_N)'])

data['Date']=total['Date']

data['Survived'][0]=sum(total['Daily Confirmed'])
data['Survival_Probability(K_M)'][0]=1
data['Survival_Probability(A_N)'][0]=1
data['Hazard_rate'][0]=0
data['Death'][0]=0
data['Cum_HR'][0]=0

for i in range(1,total.shape[0]):
    data['Death'][i]=total['Daily Deceased'][i]
    data['Survived'][i]=data['Survived'][i-1]-data['Death'][i]
    data['Hazard_rate'][i]=data['Death'][i]/data['Survived'][i-1]
    data['Cum_HR'][i]=data['Hazard_rate'][i]+data['Cum_HR'][i-1]
    data['Survival_Probability(K_M)'][i]=data['Survival_Probability(K_M)'][i-1]*(1-data['Hazard_rate'][i])
    data['Survival_Probability(A_N)'][i]=pow(math.e,(-1*data['Cum_HR'][i]))

plt.figure(figsize=(15,15))
plt.subplot(2,2,1)
plt.title('Kaplan Meir')  
plt.xlabel('Date')
plt.ylabel('Survival_Probability(K_M)')  
plt.step(data['Date'],data['Survival_Probability(K_M)'],label='SP(K_M)')
plt.step(data['Date'], data['Cum_HR'],label='HR')
plt.legend()

plt.subplot(2,2,2)
plt.title('Alder Nelson')  
plt.xlabel('Date')
plt.ylabel('Survival_Probability(A_N)')  
plt.step(data['Date'],data['Survival_Probability(A_N)'],label='SP(A_N)')
plt.step(data['Date'],data['Cum_HR'],label='HR')
plt.legend()
plt.show()
print('\n')
print('SURVIVALPROBABILITY_KM : '+str(data['Survival_Probability(K_M)'][i]))
print('\n')
print('SURVIVALPROBABILITY_AN : '+str(data['Survival_Probability(A_N)'][i]))