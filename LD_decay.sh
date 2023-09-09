

#$ -S /bin/bash
#$ -o /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/log/
#$ -e /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/log/
#$ -cwd
#$ -r y
#$ -j y
#$ -pe smp 8
#$ -l mem_free=10G
#$ -l scratch=50G
#$ -l h_rt=2:00:00


python3 LD_decay.py








    

