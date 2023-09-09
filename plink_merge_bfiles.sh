#!/bin/bash                                                                                                                                                                                                                                                                     

#                                                                                                                                                                                                                                                                               
#$ -S /bin/bash                                                                                                                                                                                                                                                                 
#$ -o /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/log/                                                                                                                                                                                                            
#$ -e /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/log/                                                                                                                                                                                                            
#$ -cwd                                                                                                                                                                                                                                                                         
#$ -r y                                                                                                                                                                                                                                                                         
#s -j y                                                                                                                                                                                                                                                                         
#$ -pe smp 4                                                                                                                                                                                                                                                                    
#$ -l mem_free=20G                                                                                                                                                                                                                                                              
#$ -l scratch=30G                                                                                                                                                                                                                                                               
#$ -l h_rt=1:00:00                                                                                                                                                                                                                                                              

#                                                                                                                                                                                                                                                                               
module load CBI
module load plink

plink --allow-no-sex --bfile plink_binary/chr20 --merge-list plink_binary/bfile_merge.txt --make-bed --out plink_binary/chrs
