
# coding: utf-8

# In[15]:


import pandas as pd


# In[17]:


f  = pd.read_excel('Extrato Spending NW_ 2020.xlsx', sheet_name='F_Form1')


# In[18]:


f


# In[26]:


processed =f.loc[:, ['Month', 'Client name', 'Clip Level', 
                       'Total Amount in US Dollar of this spending request', 'Network Provider', 'Stage', 'ID', 'Renewal cost is:','Approval Justification' ]]


# In[27]:


processed.to_csv('extract_nw.csv', index=False)




f.columns

input('Done')