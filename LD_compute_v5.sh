

#$ -S /bin/bash
#$ -o /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/log/
#$ -e /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/log/
#$ -cwd
#$ -r y
#$ -j y
#$ -pe smp 8
#$ -l mem_free=10G
#$ -l scratch=50G
#$ -l h_rt=10:00:00


module load CBI gcta

#argument1 specifies the directory of the input and output files, which is also the directory of the result of snp dependency test. e.g. ~/GWAS/Association_analysis/results/gcta/snp_dependency/20220309/ 
#argument2 specifies the plink binary e.g. ~/GWAS/Association_analysis/results/plink_binary/V3_pruned/

for file in $1*/;

do
    trait=$(basename "$file")
    echo "$trait"
    if test -f "$file"peak_snp.txt; then
	gcta64 --bfile $2"chrs" --ld "$file"peak_snp.txt --ld-wind 10000 --ld-sig 0.05 --out $file"$trait""_no_prune"
    fi
done
