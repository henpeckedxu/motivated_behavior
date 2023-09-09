

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


module load CBI
module load gcta

for ((i=1; i<=41; i++));
do
    output='Trait'$i
    gcta64 --autosome-num 25 --grm $1 --pheno $2 --mpheno $i --reml --qcovar /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/results/gcta/grm/V5_pruned/pca.eigenvec --out $3$output --thread-num 8
    result=$output'.hsq'
    grep 'V(G)/Vp' $3$result >> $3$4'.txt'
    
done
