#$ -S /bin/bash                                                                                                                                                                                                                                                                
#$ -o /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/log/                                                                                                                                                                                                           
#$ -e /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/log/                                                                                                                                                                                                           
#$ -cwd                                                                                                                                                                                                                                                                        
#$ -r y                                                                                                                                                                                                                                                                        
#$ -j y                                                                                                                                                                                                                                                                        
#$ -pe smp 8                                                                                                                                                                                                                                                                  
#$ -l mem_free=8G                                                                                                                                                                                                                                                             
#$ -l scratch=50G                                                                                                                                                                                                                                                              
#$ -l h_rt=120:00:00

module load CBI gcta
python3 ld_mlma_update.py
