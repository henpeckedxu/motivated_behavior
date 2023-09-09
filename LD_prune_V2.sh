

#$ -S /bin/bash
#$ -o /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/log/
#$ -e /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/log/
#$ -cwd
#$ -r y
#$ -j y
#$ -pe smp 8
#$ -l mem_free=8G
#$ -l scratch=50G
#$ -l h_rt=4:00:00


module load CBI
module load plink

for ((i=$1; i<=$2; i++));
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
 out="$chr"
 out+="_pruned"
 input="$chr"
 input+="_pruned.prune.in"
 plink --bfile ~/GWAS/Association_analysis/results/plink_binary/V5/"$chr" --chr-set 25 no-xy --indep-pairwise 50 5 0.95 --out ~/GWAS/Association_analysis/results/plink_binary/V5_pruned/"$out" --thread-num 8
 plink --chr-set 25 no-xy --bfile ~/GWAS/Association_analysis/results/plink_binary/V5/"$chr" --extract ~/GWAS/Association_analysis/results/plink_binary/V5_pruned/"$input" --make-bed  --out ~/GWAS/Association_analysis/results/plink_binary/V5_pruned/"$out" --thread-num 8
done



