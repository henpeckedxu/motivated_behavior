#!/bin/bash 
#
#$ -S /bin/bash
#$ -o /wynton/home/guolab/henpeckedxu/LD_NeuralNetwork/log/                                                                                                                                                                                                                
#$ -e /wynton/home/guolab/henpeckedxu/LD_NeuralNetwork/log/
#$ -cwd 
#$ -l mem_free=8G 
#$ -l h_rt=3:00:00
#$ -l hostname=qb3-id*
#$ -pe smp 8
#$ -l scratch=50G

#argument1: input the working directory
#argument2: input the prefix of the output of the matrix from first command
#argument3: output of the transformed image


cd ~/LD_NeuralNetwork/experiments/antsRegistration/HCR/ref

sh ~/LD_NeuralNetwork/bin/ANTs/install/bin/antsRegistrationSyNQuick.sh -d 3 -f Zbrain_Elavl3-H2BRFP.nii -m T_AVG_HuCH2BGCaMP2-tg_ch0.nii  -n 8 -o T_AVG_HuCH2BGCaMP2-tg -t s

~/LD_NeuralNetwork/bin/ANTs/install/bin/antsApplyTransforms -d 3 -v 0 -n WelchWindowedSinc -i T_AVG_nns25Tg.nii -r Zbrain_Elavl3-H2BRFP.nii -o T_AVG_gad1b_template.nii.gz -t T_AVG_HuCH2BGCaMP2-tg1Warp.nii.gz -t T_AVG_HuCH2BGCaMP2-tg0GenericAffine.mat








