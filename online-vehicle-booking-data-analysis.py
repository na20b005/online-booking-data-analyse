#!/usr/bin/env python
# coding: utf-8

# In[12]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


sns.set()


# In[13]:


df = pd.read_csv('/Users/macair/Downloads/archive-3/taxi_tripdata.csv')


# In[14]:


df.head()


# In[15]:


df.shape


# In[16]:


df.describe()


# In[17]:


df.dtypes


# ##### Unnecessary columns to drop.

# In[18]:


df = df.drop(['ehail_fee', 'VendorID', 'trip_type', 'congestion_surcharge'], axis= 1)


# ##### Total Amount cannot be negative , so I will drop those rows.

# In[19]:


len(df[df['total_amount'] <= 0])


# In[20]:


df = df[df['total_amount'] > 0]


# In[21]:


len(df[df['fare_amount'] <= 0])


# ##### Trip Distance cannot be zero.

# In[22]:


len(df[df['trip_distance'] <= 0])


# In[23]:


df.groupby('RatecodeID')['trip_distance'].median()


# In[24]:


df.loc[(df['trip_distance'] <= 0) & (df['RatecodeID'] == 1.0)] = 2.8
df.loc[(df['trip_distance'] <= 0) & (df['RatecodeID'] == 2.0)] = 20
df.loc[(df['trip_distance'] <= 0) & (df['RatecodeID'] == 3.0)] = 24
df.loc[(df['trip_distance'] <= 0) & (df['RatecodeID'] == 4.0)] = 12
df.loc[(df['trip_distance'] <= 0) & (df['RatecodeID'] == 5.0)] = 3.1


# In[25]:


for i in df.columns[[0, 1]]:
    df[i] = pd.to_datetime(df[i])


# ##### I will create a new column that contains the trip duration.

# In[26]:


timedeltas = df['lpep_dropoff_datetime'] - df['lpep_pickup_datetime']
trip_duration = []
for i in timedeltas :
    trip_duration.append(i.total_seconds() / 60)

df['trip_duration'] = trip_duration
df['trip_duration'] = df['trip_duration'].round(2)


# ##### I will drop the rows where the 'trip_duration' is less than a minute.

# In[27]:


df = df[df['trip_duration'] > 1]
df.shape


# In[28]:


df['store_and_fwd_flag'].value_counts()


# In[29]:


df['store_and_fwd_flag'].fillna('N', inplace= True)


# In[30]:


df['payment_type'].value_counts(normalize= True)


# In[31]:


df.groupby('payment_type')['total_amount'].quantile(0.95)


# In[47]:


df['passenger_count'].value_counts(normalize= True)


# In[48]:


df.loc[df['passenger_count']==0, 'passenger_count'] = 1.0
df.loc[df['passenger_count']==7, 'passenger_count'] = 1.0
df.loc[df['passenger_count']==32, 'passenger_count'] = 1.0


# In[49]:


df.loc[df['passenger_count'].isna(), 'passenger_count'] = 1.0


# In[50]:


df.isna().sum()


# In[40]:


df.head()


# In[41]:


df.shape


# In[42]:


plt.figure(figsize= (18, 10))
sns.heatmap(df.corr(), annot= True);


# ##### Which is the busiest day ?

# In[51]:


df['day_of_week'] = df['lpep_pickup_datetime'].dt.day_name()


# In[52]:


plt.figure(figsize= (18, 7))
sns.countplot(y= 'day_of_week', data= df)
plt.ylabel('');


# ##### Which is the busiest hour ?

# In[45]:


plt.figure(figsize= (18, 7))
sns.countplot(x= df['lpep_pickup_datetime'].dt.hour, data= df, color= 'goldenrod')
plt.ylabel('')
plt.xlabel('Hour of Day');

