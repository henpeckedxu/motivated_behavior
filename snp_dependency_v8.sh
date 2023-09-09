#$ -S /bin/bash                                                                                                                                                                                                                                                                
#$ -o /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/log/                                                                                                                                                                                                           
#$ -e /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/log/                                                                                                                                                                                                           
#$ -cwd                                                                                                                                                                                                                                                                        
#$ -r y                                                                                                                                                                                                                                                                        
#$ -j y                                                                                                                                                                                                                                                                        
#$ -pe smp 8                                                                                                                                                                                                                                                                  
#$ -l mem_free=8G                                                                                                                                                                                                                                                             
#$ -l scratch=50G                                                                                                                                                                                                                                                              
#$ -l h_rt=80:00:00 


module load CBI vcftools
module load CBI gcta
#argument1, the first argument following '-to', is a txt file of trait orders e.g. '~/GWAS/Association_analysis/Phenotype/20220105/traits.txt'
#argument2, the second argument  following '-to' is the trait name for analysis. e.g. 'LDCI'
#argument3 following '-out' is the output directory. e.g. '~/GWAS/Association_analysis/results/gcta/snp_dependency/20220113/'
#argument4 following '-mlmadir' is the folder of  mlma files for the trait under analysis. e.g. '~/GWAS/Association_analysis/results/gcta/MLMA/20220105/'
#argument5 following '-genodir' is the folder of the vcf files. e.g. '~/GWAS/Association_analysis/Genotype/V4/'
#argument6 following '-rawpheno' is the raw phenotype data of the entire population. e.g. '~/GWAS/Association_analysis/Phenotype/20220105/AccumulativeResults-20201222.xlsx'

mkdir $3
mkdir $3$2/
python3 snp_dependency_v8.py -to $1 $2 -out $3 -mlmadir $4 -genodir $5 -rawpheno $6 


