import pandas as pd
import numpy as np
df_maf = pd.read_csv('~/GWAS/Association_analysis/results/plink_binary/V3_pruned/plink.ld', delim_whitespace=True)
df_maf['MAF_diff']=df_maf['MAF_A']-df_maf['MAF_B']
df_maf_flt = df_maf.loc[(df_maf['MAF_diff']>-0.05)&(df_maf['MAF_diff']<0.05)]
df_maf_flt['Distance']=df_maf_flt['BP_B']-df_maf_flt['BP_A']

r2_list=[]
distance_list=[]

for i in range (0,50):
    start = 100000*i
    end = 100000*(i+1)
    r2 = df_maf_flt.loc[(df_maf_flt['Distance']>start)&(df_maf_flt['Distance']<end)]['R2'].mean()
    distance=(start+end)/2
    r2_list.append(r2)
    distance_list.append(distance)
    print(start)

df_test = pd.DataFrame({'r2':r2_list, 'distance':distance_list})
df_test.to_csv('LD_decay.txt')
