import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import subprocess
import os
import sys

df = pd.read_csv('/wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/results/gcta/ld_mlma_update/20230203/input_data.csv', sep=',',header=None).iloc[31:, :]
traitlist = pd.read_csv('/wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/Phenotype/20220822/traits.txt', sep = '\t')
df['trait_order'] = df[1].apply(lambda x: traitlist.columns[0].split(' ').index(x))
def func1(chr,mid,size,trait_order, trait, peak_snp):
    if chr<=10:
        chr_id = 'chr0'+str(chr)
    else:
        chr_id = 'chr'+str(chr)
    if ((trait_order>=32 and trait_order<=37) or (trait_order>=17 and trait_order<=23)):
        cov = trait_order - 7
    elif (trait_order == 39 or trait_order == 41):
        cov = trait_order - 1
    else:
        cov = 0 
    if cov == 0:
        return ('gcta64 --autosome-num 25 --mlma --grm /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/results/gcta/grm/V5_pruned/chrs_pruned --mlma-subtract-grm /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/results/gcta/grm/V5_pruned/'+chr_id+ ' --bfile /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/results/plink_binary/V5/'+chr_id + ' --chr '+str(chr) +' --extract-region-bp ' + str(chr) + ' ' + str(mid)+' ' + str(size) + ' ' + '--pheno /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/Phenotype/20220822/metapheno_pro_20220822.txt' + ' --mpheno ' + str(trait_order) + ' ' + '--out ' + '/wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/results/gcta/ld_mlma_update/20230203/Trait'+str(trait_order)+'_'+ trait+'_'+peak_snp)
    else:
        cov_trait = str(cov)+'_pheno_'+traitlist.columns[0].split(' ')[cov]+'_pro_20220822.txt'
        return ('gcta64 --autosome-num 25 --mlma --grm /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/results/gcta/grm/V5_pruned/chrs_pruned --mlma-subtract-grm /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/results/gcta/grm/V5_pruned/'+chr_id+ ' --bfile /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/results/plink_binary/V5/'+chr_id + ' --chr '+str(chr) +' --extract-region-bp ' + str(chr) + ' ' + str(mid)+' ' + str(size) + ' ' + '--pheno /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/Phenotype/20220822/metapheno_pro_20220822.txt' + ' --mpheno ' + str(trait_order) + ' --mlma-no-preadj-covar --qcovar /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/Phenotype/20220822/' + cov_trait+' --out ' + '/wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/results/gcta/ld_mlma_update/20230203/Trait'+str(trait_order)+'_'+trait+'_'+peak_snp)

df['command'] = df.apply(lambda x: func1(x[2], x[3], x[4], x['trait_order'], x[1],x[0]),axis=1)
#print(df['command'].iloc[0])
for i in range(df.shape[0]):
    command = df.iloc[i, -1].split()
    subprocess.run(command)
