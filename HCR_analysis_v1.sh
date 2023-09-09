#!/bin/bash 
#
#$ -S /bin/bash
#$ -o /wynton/home/guolab/henpeckedxu/LD_NeuralNetwork/log/                                                                                                                                                                                                                
#$ -e /wynton/home/guolab/henpeckedxu/LD_NeuralNetwork/log/
#$ -cwd 
#$ -l mem_free=8G 
#$ -l h_rt=24:00:00
#$ -l hostname=qb3-id*
#$ -pe smp 8
#$ -l scratch=50G

#argument1: input the working directory
#argument2: input fish id
#argument3: input gene
#argument4: input threshold quantile

python3 HCR_analysis_v1.py $1 $2 $3 $4







 






