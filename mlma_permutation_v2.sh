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

##                                                                                                                                                                                                                                                                              
module load CBI
module load gcta
#argument1 is the start chromosome number                                                                                                                                                                                                                                    
#argument2 is the trait number
#argument3 is the permutation start round
#argument4 is the number of permutation round
if (("$1"<10))
then
    chr="chr0"$1
else
    chr="chr"$1
fi

for ((i=$3; i<=$3+$4; i++));
do
  gcta64 --autosome-num 25 --mlma --grm ~/GWAS/Association_analysis/results/gcta/grm/V5_pruned/chrs_pruned --mlma-subtract-grm ~/GWAS/Association_analysis/results/gcta/grm/V5_pruned/"$chr" --bfile ~/GWAS/Association_analysis/results/plink_binary/V5_pruned/chrs_\
pruned --chr $1 --pheno ~/GWAS/Association_analysis/results/gcta/permutation/perm_pheno_1_100/metapheno_pro_perm$i.txt --mpheno $2 --out ~/GWAS/Association_analysis/results/gcta/permutation/perm_pheno_1_100/"Trait"$2"_""$chr"_perm$i --thread-num 8

rm ~/GWAS/Association_analysis/results/gcta/permutation/perm_pheno_1_100/"Trait"$2"_""$chr"_perm$i.log
done
