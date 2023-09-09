

#$ -S /bin/bash
#$ -o /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/log/
#$ -e /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/log/
#$ -cwd
#$ -r y
#$ -j y
#$ -pe smp 8
#$ -l mem_free=8G
#$ -l scratch=50G
#$ -l h_rt=50:00:00

##
module load CBI
module load gcta

# argument1 is the start chromosome number 
# argument2 is the trait number

for ((i=$1; i<=$1+0; i++));
do

 if (("$i"<10))
 then
	chr="chr0"
	chr+="$i"
	echo "$chr"
 else
	chr="chr"
	chr+="$i"
	echo "$chr"
 fi
 if ((($2 >= 31 && $2 <= 37) || ($2 >= 17 && $2 <= 23))) 
 then
     cov=$2
     cov=$((cov-7)) 
     gcta64 --autosome-num 25 --mlma --grm ~/GWAS/Association_analysis/results/gcta/grm/V5_pruned/chrs_pruned --mlma-subtract-grm ~/GWAS/Association_analysis/results/gcta/grm/V5_pruned/"$chr" --bfile ~/GWAS/Association_analysis/results/plink_binary/V5_pruned/chrs_pruned --chr $i --pheno ~/GWAS/Association_analysis/Phenotype/20220822/metapheno_pro_20220822.txt --mpheno $2 --mlma-no-preadj-covar --qcovar ~/GWAS/Association_analysis/Phenotype/20220822/"$cov"* --out /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/results/gcta/MLMA/20220822/"Trait"$2"_""$chr" --thread-num 8
 elif ((($2 == 39)||($2 == 41)))
 then
     cov=$2
     cov=$((cov-1))
     gcta64 --autosome-num 25 --mlma --grm ~/GWAS/Association_analysis/results/gcta/grm/V5_pruned/chrs_pruned --mlma-subtract-grm ~/GWAS/Association_analysis/results/gcta/grm/V5_pruned/"$chr" --bfile ~/GWAS/Association_analysis/results/plink_binary/V5_pruned/chrs_pruned --chr $i --pheno ~/GWAS/Association_analysis/Phenotype/20220822/metapheno_pro_20220822.txt --mpheno $2 --mlma-no-preadj-covar --qcovar ~/GWAS/Association_analysis/Phenotype/20220822/"$cov"* --out /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/results/gcta/MLMA/20220822/"Trait"$2"_""$chr" --thread-num 8
 else 
     gcta64 --autosome-num 25 --mlma --grm ~/GWAS/Association_analysis/results/gcta/grm/V5_pruned/chrs_pruned --mlma-subtract-grm ~/GWAS/Association_analysis/results/gcta/grm/V5_pruned/"$chr" --bfile ~/GWAS/Association_analysis/results/plink_binary/V5_pruned/chrs_pruned --chr $i --pheno ~/GWAS/Association_analysis/Phenotype/20220822/metapheno_pro_20220822.txt --mpheno $2 --out /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/results/gcta/MLMA/20220822/"Trait"$2"_""$chr" --thread-num 8
 fi
done
