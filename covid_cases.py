#!/usr/bin/env python
# coding: utf-8

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os

import matplotlib.pyplot as plt
#@get_ipython().run_line_magic('matplotlib', 'inline')

import warnings
warnings.filterwarnings("ignore")

import subprocess

##############################################################
#code to pull data
#repeated in the app_callback function below for refreshing
completed = subprocess.run(['sudo', 'rm', '-r', 'COVID-19/'],                             stdout=subprocess.PIPE,)
print(completed.stdout.decode('utf-8'))
 
completed = subprocess.run(['git', 'clone', 'https://github.com/CSSEGISandData/COVID-19.git', 'COVID-19'],                         stdout=subprocess.PIPE,)
print(completed.stdout.decode('utf-8'))
 
data = pd.read_csv('COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')


print(data.shape)

#missing values
tot = len(data['Province/State'])
missing = len(data[~data['Province/State'].notnull()]) 
print('% records missing, Province/State: ' + str(round(100*missing/tot, 2)))

#min, max
print('min: '+str(data['3/30/20'].min())), print('max: '+str(data['3/30/20'].max()))

#data.describe()

data=data.drop(columns=['Province/State','Lat','Long'])

countries = data.groupby('Country/Region').sum()
countries = countries.sort_values(countries.columns[-1], ascending = False)

#Select top 10 countries by reported confirmed cases

countries_selected = countries[:10]

labels = list()
for row in countries_selected.index: 
    labels.append(row)

plt.figure(figsize=(20,10))
plt.plot(countries_selected.T)
plt.title('selected countries - cumulative COVID cases as of latest available data',fontsize=18)
plt.xticks(fontsize=12, rotation=45)
plt.xlabel('date',fontsize=12)
plt.legend(labels,fontsize=12)

#plt.axislabelsize('small')
#graph = countries_selected.T.plot(title='selected countries - cumulative COVID cases as of latest date')
plt.savefig('results/cases.png')
#plt.show()



