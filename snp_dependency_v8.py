
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import subprocess
import os
import sys

#find the peak marker and save it to a txt file
traitsfile = sys.argv[sys.argv.index('-to')+1]
Traits = pd.read_csv(traitsfile, sep = ' ',index_col=0).columns#get the trait list
print('All the traits are \n')
print(Traits)
Trait = sys.argv[sys.argv.index('-to')+2]#use the first argument as trait name
result_folder = sys.argv[sys.argv.index('-out')+1]+Trait+'/'
Trait_order = list(Traits).index(Trait)+1#get the order of the trait in the trait list
print('Analyzing Trait%s'%sys.argv[1])

#read mlma file of the current trait using -mlma
df_list = []
for i in range(0, 25):
    if i<9:
        chr_num = i+1
        chr_num = '0'+str(chr_num)
    else:
        chr_num = i+1
        chr_num = str(chr_num)
    print(chr_num)
    df_chr = pd.read_csv(sys.argv[sys.argv.index('-mlmadir')+1]+'Trait'+str(Trait_order)+'_'+'chr'+chr_num+'.mlma', header=0, index_col=False, sep='\t')
    df_list.append(df_chr)
df = pd.concat(df_list)
df.insert(0, '-log10_P', df['p'].apply(lambda x: math.log(x, 10)*(-1)))
df_detected_snp = df.loc[df['-log10_P']>6.659161]
print('dependency test will be permformed on chromosomes: %s'%df_detected_snp['Chr'].unique())

peak_snp_list = []
for chr_no in df_detected_snp['Chr'].unique():
   df_detected_snp_chr = df_detected_snp.loc[df_detected_snp['Chr']==chr_no]
   print(df_detected_snp_chr)
   while df_detected_snp_chr.shape[0] > 1:
        SNP_ID = df_detected_snp_chr.loc[df_detected_snp_chr['-log10_P']==df_detected_snp_chr['-log10_P'].max()]['SNP'].values[0]#find the ID of the peak snp
        df_peak_snp = df_detected_snp_chr.loc[df_detected_snp_chr['-log10_P']==df_detected_snp_chr['-log10_P'].max()].loc[:, ['Chr','bp']]#find the position info of the peak snp
        df_peak_snp['Chr']=df_peak_snp['Chr'].apply(lambda x: 'chr'+str(x) if x > 9 else 'chr0'+str(x))#change the format of chromosome number of the snp ID for VCF file indexing later
        df_current_snp = df_detected_snp_chr.loc[df_detected_snp_chr['-log10_P']==df_detected_snp_chr['-log10_P'].max()].loc[:, ['Chr','bp']]
        df_current_snp['Chr'] = df_current_snp['Chr'].apply(lambda x: 'chr'+ str(x))
        peak_snp_number = len(peak_snp_list)+1#count the independent snp
        peak_snp_list.append(SNP_ID)
        pd.Series(peak_snp_list).to_csv(result_folder+'peak_snp.txt',header=False, sep = '\t', index=False)

        #Step1. extract the gentype of the peak marker from the vcf file
        vcffile = sys.argv[sys.argv.index('-genodir')+1]+df_peak_snp['Chr'].values[0]+'_hwe_maf_flt.vcf.gz'#set input vcf file harboring the current peak snp
        output = result_folder+'peak_snp'+str(peak_snp_number)+'_vcf_'+Trait#set output vcf file with the  current peak snp number
        current_snp_pos = result_folder+'peak_snp'+str(peak_snp_number)+'.txt'#make a txt file to store the current peak snp
        df_current_snp.to_csv(current_snp_pos, header=False, sep = '\t', index=False)
        print('extract vcf of current peak snp \n')
        print(df_peak_snp)
        command1 = 'vcftools --gzvcf '+ vcffile + ' ' + '--positions ' + current_snp_pos + ' ' +  '--recode --recode-INFO-all --out ' + output
        command1 = command1.split()
        subprocess.run(command1)

        #Step2. preprocess the raw phentoype data using all the genotype of the collected peak snps as covaraibles
        print('adjust phentoype by using independent peak snps as covariables')
        command2 = 'python3 phenotype_preprocess_v6.py '+ sys.argv[sys.argv.index('-rawpheno')+1]+' '+'--adjust-peaksnp '+ result_folder + ' ' + Trait
        subprocess.run(command2.split())

        #Step3. run mlma using phentoype adjusted by peak snps as covariables
        print('run mlma with phenotype adjusted for snps: \n')
        #store all the independent peak snp into one file
        if (Trait_order>=31 and Trait_order<=37) or (Trait_order>=17 and Trait_order<=23):
            covariable = Trait_order - 7 
            command3 = 'gcta64 --autosome-num 25  --exclude ' + result_folder+'peak_snp.txt' + ' --mlma --grm /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/results/gcta/grm/V5_pruned/chrs_pruned --mlma-subtract-grm /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/results/gcta/grm/V5_pruned/' +df_peak_snp['Chr'].values[0] +  ' --bfile /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/results/plink_binary/V5_pruned/chrs_pruned '+'--chr ' + str(chr_no)+ ' --pheno ' + result_folder + 'peaksnp_adjusted_pheno.txt ' + '--mpheno ' + str(Trait_order) + ' --mlma-no-preadj-covar'  + ' --qcovar /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/Phenotype/20220822/'+str(covariable)+'_pheno_'+Traits[covariable-1]+'_pro_20220822.txt' +' --out ' + result_folder+'peak_marker_adjusted --threads 8'
        elif Trait_order in [39, 41]:
            covariable = Trait_order - 1
            command3 = 'gcta64 --autosome-num 25  --exclude ' + result_folder+'peak_snp.txt' + ' --mlma --grm /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/results/gcta/grm/V5_pruned/chrs_pruned --mlma-subtract-grm /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/results/gcta/grm/V5_pruned/' +df_peak_snp['Chr'].values[0] +  ' --bfile /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/results/plink_binary/V5_pruned/chrs_pruned '+'--chr ' + str(chr_no)+ ' --pheno ' + result_folder + 'peaksnp_adjusted_pheno.txt ' + '--mpheno ' + str(Trait_order) + ' --mlma-no-preadj-covar'  + ' --qcovar /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/Phenotype/20220822/'+str(covariable)+'_pheno_'+Traits[covariable-1]+'_pro_20220822.txt' +' --out ' + result_folder+'peak_marker_adjusted --threads 8'
        else:
            command3 = 'gcta64 --autosome-num 25  --exclude ' + result_folder+'peak_snp.txt' + ' --mlma --grm /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/results/gcta/grm/V5_pruned/chrs_pruned --mlma-subtract-grm /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/results/gcta/grm/V5_pruned/' +df_peak_snp['Chr'].values[0] +  ' --bfile /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/results/plink_binary/V5_pruned/chrs_pruned '+'--chr ' + str(chr_no)+ ' --pheno ' + result_folder + 'peaksnp_adjusted_pheno.txt ' + '--mpheno ' + str(Trait_order) + ' --out ' + result_folder+'peak_marker_adjusted --threads 8'
        command3 = command3.split()
        subprocess.run(command3)
        df = pd.read_csv(result_folder+'peak_marker_adjusted.mlma', header=0, index_col=False, sep='\t')
        df.insert(0, '-log10_P', df['p'].apply(lambda x: math.log(x, 10)*(-1)))
        df_detected_snp_chr = df.loc[df['-log10_P']>6.659161]
   if df_detected_snp_chr.shape[0] == 1:
        SNP_ID = df_detected_snp_chr.loc[df_detected_snp_chr['-log10_P']==df_detected_snp_chr['-log10_P'].max()]['SNP'].values[0]#find the ID of the peak snp
        peak_snp_list.append(SNP_ID)
        pd.Series(peak_snp_list).to_csv(result_folder+'peak_snp.txt',header=False, sep = '\t', index=False)
   else:
        for file in os.listdir(result_folder):
            if file.endswith(".recode.vcf"):
                os.remove(result_folder+file)
   print('test for chr %i is done'%chr_no)
