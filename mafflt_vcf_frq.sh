

#$ -S /bin/bash
#$ -o /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/log/
#$ -e /wynton/home/guolab/henpeckedxu/GWAS/Association_analysis/log/
#$ -cwd
#$ -r y
#$ -j y
#$ -pe smp 20
#$ -l mem_free=10G
#$ -l scratch=50G
#$ -l h_rt=12:00:00

##
module load CBI
module load vcftools


for ((i=1; i<=25; i++));
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


     vcf="${chr}_mafflt.vcf.gz"
     output="${chr}_mafflt"
	
        vcftools --gzvcf ~/GWAS/Association_analysis/Genotype/V2/"$vcf"  --freq --out  ~/GWAS/Association_analysis/Genotype/V2/"$output"

done
