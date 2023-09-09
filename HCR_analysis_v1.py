#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import pingouin as pg
import scipy.stats as stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from matplotlib.lines import Line2D
import matplotlib.lines as mlines
import math
import seaborn as sns
import pickle
import h5py
import xlrd
import xlwt
import heapq
import maskdb_parsing as maskdb
import nibabel as nib


# In[3]:
wdir = sys.argv[1]
fish_id = sys.argv[2]
gene = sys.argv[3]
quantile = float(sys.argv[4])
image_file = wdir+fish_id+'_'+gene+'_registered_pro.nii'
test_load = nib.load(image_file).get_fdata()

# In[24]:


df_corr_list = []
for i in range(test_load.shape[2]):
    df= pd.DataFrame(test_load[:,:,i,0]).transpose()
    threshold = np.quantile(df, quantile)
    df = df.applymap(lambda x: 0 if x <threshold else x)
    df_corr = pd.DataFrame(df.stack().reset_index())
    df_corr.columns = [1,0,3]
    df_corr = df_corr.loc[df_corr[3]>0]
    df_corr[2] = i
    df_corr_list.append(df_corr)


# In[42]:


df_corr_expression = pd.concat(df_corr_list)
df_corr_expression
df_corr_expression.to_csv(wdir+fish_id+'_'+gene+'_coor'+str(quantile)+".csv")

# In[25]:


df_corr_new = np.array(pd.concat(df_corr_list)[[0,1,2]])


# In[27]:





# In[28]:


def anatomical_masking (coor):
    mdb = maskdb.mask_db()
    coor = coor [:,[2,1,0]]
    anatomical_mask = []
    for i in range(294):
        anatomical_mask_T = mdb.mask_multi_direct_search(i, coor)[0]
        for i in range(len(anatomical_mask_T)):
            if anatomical_mask_T[i] == False:
                anatomical_mask_T[i] = 0
            if anatomical_mask_T[i] == True:
                anatomical_mask_T[i] = 1
        anatomical_mask.append(anatomical_mask_T)
    return anatomical_mask


# In[29]:


mask = anatomical_masking(df_corr_new)


# In[30]:


anatomical_mask_MC = np.reshape (mask , [np.shape(mask)[0], np.shape(mask)[1]])


# In[31]:


msk_name = np.load ("MaskDatabaseNames.npz")['arr_0']
df_anatomical_mask = pd.DataFrame(anatomical_mask_MC)
df_msk_name = pd.DataFrame(msk_name)
df_msk_name[0] = df_msk_name[0].str.decode("utf-8").apply(lambda x: x.split("'")).str[1]
df_anatomical_mask.index = df_msk_name[0]
df_anatomical_mask.index.name=None
df_anatomical_mask = df_anatomical_mask.transpose()


# In[41]:


df_expression_count = df_anatomical_mask.sum()


# In[54]:


expression_intensity_list = []
for mask in df_anatomical_mask.columns:
    
    epixel  = df_anatomical_mask.loc[df_anatomical_mask[mask]==1].index
    df_target = pd.DataFrame(df_corr_new[epixel])
    new_df = pd.merge(df_target, df_corr_expression,  how='left', left_on=[0,1,2], right_on = [0,1,2])
    expression_intensity_list.append(new_df[3].sum())


# In[59]:


df_res = pd.concat((df_expression_count, pd.Series(expression_intensity_list, index=df_expression_count.index)), axis=1)
df_res.columns = ['ex_count', 'ex_intensity']
df_res.to_csv(wdir+fish_id+'_'+gene+'_'+str(quantile))


# In[60]:




