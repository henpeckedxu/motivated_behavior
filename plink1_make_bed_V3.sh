#!/bin/bash

#$ -S /bin/bash
#$ -o /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/log/
#$ -e /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/log/
#$ -cwd
#$ -r y
#s -j y
#$ -pe smp 8
#$ -l mem_free=8G
#$ -l scratch=30G
#$ -l h_rt=10:00:00

module load CBI
module load plink
 


cd ~/GWAS/Association_analysis/Genotype/V5
for ((i=$1; i<=$1+2; i++));
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
 input="${chr}_hwe_maf_flt.vcf.gz"
 output="$chr"

  
 plink --vcf "$input"  --const-fid --out ~/GWAS/Association_analysis/results/plink_binary/V5/"$output"
done

