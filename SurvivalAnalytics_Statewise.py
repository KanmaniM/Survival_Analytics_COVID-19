# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 19:12:26 2020

@author: Kanmani
"""
import pandas as pd
import math
import warnings
import matplotlib.pyplot as plt
import numpy as np
warnings.filterwarnings("ignore")


abbrevations={'an': 'Andaman and Nicobar Islands', 'ap': 'Andhra Pradesh', 'ar': 'Arunachal Pradesh', 'as': 'Assam', 'br': 'Bihar', 'ch': 'Chandigarh', 
 'ct': 'Chhattisgarh', 'dd': 'Daman and Diu', 'dl': 'Delhi', 'dn': 'Dadra and Nagar Haveli', 'ga': 'Goa', 'gj': 'Gujarat', 'hp': 'Himachal Pradesh', 
 'hr': 'Haryana', 'jh': 'Jharkhand', 'jk': 'Jammu and Kashmir', 'ka': 'Karnataka', 'kl': 'Kerala', 'la': 'Ladakh', 'ld': 'Lakshadweep', 'mh': 'Maharashtra', 
 'ml': 'Meghalaya', 'mn': 'Manipur', 'mp': 'Madhya Pradesh', 'mz': 'Mizoram', 'nl': 'Nagaland', 'or': 'Orissa', 'pb': 'Punjab', 'py': 'Puducherry', 'rj': 'Rajasthan', 
 'sk': 'Sikkim', 'tg': 'Telangana', 'tn': 'Tamil Nadu', 'tr': 'Tripura', 'up': 'Uttar Pradesh', 'ut': 'Uttarakhand', 'wb': 'West Bengal'}

state_daily=pd.read_csv('https://api.covid19india.org/csv/latest/state_wise_daily.csv')
states=list(state_daily.columns)[3:]
dates=state_daily['Date'].unique()
survival_probs_states={}
data_refer={}
d_f={}
h_r={}
no_cases=0
for state in states:
    df=pd.DataFrame(columns=['Date','Confirmed','Deceased'])
    df['Date']=dates
    is_confirmed=state_daily['Status']=='Confirmed'
    is_recovered=state_daily['Status']=='Recovered'
    is_deceased=state_daily['Status']=='Deceased'
    
    df['Confirmed']=list(state_daily[is_confirmed][state])
    df['Recovered']=list(state_daily[is_recovered][state])
    df['Deceased']=list(state_daily[is_deceased][state])
    #X = np.arange(df.shape[0])
    #fig = plt.figure()
    #ax = fig.add_axes([0,0,1,1])

    #ax.bar(X + 0.00, list(df['Confirmed']), color = 'b', width = 0.25,label='Confirmed')
    #ax.bar(X + 0.25, list(df['Recovered']), color = 'g', width = 0.25,label='Recoverd')
    #ax.bar(X + 0.50, list(df['Deceased']), color = 'r', width = 0.25,label='Deaths')
    #ax.legend()
    if len(df['Confirmed'].unique())==1 and list(set(df['Confirmed'].unique()))[0]==0:
        survival_probs_states[state]=-1
        no_cases+=1
    else:
        data=pd.DataFrame(columns=['Date','Survived','Death','Hazard_rate','Survival_Probability(K_M)','Cum_HR','Survival_Probability(A_N)'])
        
        data['Date']=df['Date']
        
        data['Survived'][0]=sum(df['Confirmed'])
        #data['Active'][0]=sum(df['Confirmed'])
        data['Survival_Probability(K_M)'][0]=1
        data['Survival_Probability(A_N)'][0]=1
        data['Hazard_rate'][0]=0
        data['Death'][0]=0
        data['Cum_HR'][0]=0
        
        for i in range(1,df.shape[0]):
            data['Death'][i]=df['Deceased'][i]
            #data['Recovered'][i]=df['Recovered'][i]
            #data['Active'][i]=data['Survived'][i-1]-df['Recovered'][i]
            data['Survived'][i]=data['Survived'][i-1]-data['Death'][i]
            data['Hazard_rate'][i]=data['Death'][i]/data['Survived'][i-1]
            data['Cum_HR'][i]=data['Hazard_rate'][i]+data['Cum_HR'][i-1]
            data['Survival_Probability(K_M)'][i]=data['Survival_Probability(K_M)'][i-1]*(1-data['Hazard_rate'][i])
            data['Survival_Probability(A_N)'][i]=pow(math.e,(-1*data['Cum_HR'][i]))
        survival_probs_states[state]=(data['Survival_Probability(K_M)'][i])
        data_refer[state]=data
        d_f[state]=df
        h_r[state]=data['Cum_HR'][i] 

    #plt.title(abbrevations[state.lower()])
    #plt.subplot(2,2,1)
    #plt.xlabel('Date')
    #plt.ylabel('Survival_Probability(K_M)')  
    #plt.step(data['Date'],data['Survival_Probability(K_M)'])
    #plt.show()
    
    #plt.subplot(2,2,2)  
    #plt.xlabel('Date')
    #plt.ylabel('Survival_Probability(A_N)')  
    #plt.plot(data['Date'],data['Survival_Probability(A_N)'])
    #plt.show()


item=list(survival_probs_states.items())
value=list(survival_probs_states.values())
value_sort=sorted(value)

max_ind=value.index(value_sort[-1])
min_ind=value.index(value_sort[no_cases])

max_sp=item[max_ind]
min_sp=item[min_ind]
print('\n')
print('Max_SurProb : '+str(max_sp))
print('\n')
print('Min_SurProb : '+str(min_sp))
print('\n')
print('STATES_BY_SurProb : ')
a = sorted(survival_probs_states.items(), key=lambda x: -x[1])
k=1
for ele,count in a:
  print(str(k)+' '+abbrevations[ele.lower()]+' : '+str(count))
  k+=1
