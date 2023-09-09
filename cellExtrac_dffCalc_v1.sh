#!/bin/env bash
# -cwd             ## use current working directory
#$ -l mem_free=20G                  #-- submits on nodes with enough free memory (required)
#$ -l scratch=30G  ## needs 400 GB of /scratch space
#$ -l h_rt=20:00:00
#$ -pe smp 8
#$ -o /wynton/home/guolab/henpeckedxu/LD_NeuralNetwork/log/                                                                                                                                                                                                                   
#$ -e /wynton/home/guolab/henpeckedxu/LD_NeuralNetwork/log/
# -j y


## 0. In case TMPDIR is not set, e.g. on development nodes, set
##    it to local /scratch, if it exists, otherwise to /tmp
if [[ -z "$TMPDIR" ]]; then
  if [[ -d /scratch ]]; then TMPDIR=/scratch/$USER; else TMPDIR=/tmp/$USER; fi
  mkdir -p "$TMPDIR"
  export TMPDIR
fi

## 1. Use a temporary working directory
#cd "$TMPDIR" #<<<<<<<<<<<<<< 01-06-2020

## 2. Copy input files from global disk to local scratch
#cp ~/sample.fq .
#cp ~/reference.fa .

## 3. Process input files
#/path/to/my_pipeline --cores="$NSLOTS" reference.fa sample.fq > output.bam



module load CBI
module load Sali
module load anaconda
source activate caiman
#argument1 is the input data folder e.g. ~/LD_NeuralNetwork/experiments/caiman/image_data/20220208/Fish_08/
#argument2 is the start image file e.g. 0 means Fish08_0.tif under the above folder
#argument3 is the number of image files needs to be processed e.g. 2 means Fish08_0.tif and Fish08_1.tif will be processed
start=$2
end=$3 
for ((number=$start; number<=$end; number++))
do
  echo $number
  python3 /wynton/home/guolab/henpeckedxu/LD_NeuralNetwork/bin/cellExtrac_dffCalc_v1.py $1 $number  -cores="$NSLOTS" #reference.fa sample.fq > output.bam
done

## 4. Move output files back to global disk
#mv output.bam ~

## 5. End-of-job summary
[[ -n "$JOB_ID" ]] && qstat -j "$JOB_ID"
