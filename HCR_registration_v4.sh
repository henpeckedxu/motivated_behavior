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
#argument2: input the prefix of the output of the matrix from first command
#argument3: output of the transformed image


cd $1

sh  /wynton/home/guolab/henpeckedxu/LD_NeuralNetwork/bin/ANTs/install/bin/antsRegistrationSyN.sh -d 3 -f T_AVG_vglu2b_template.nii -m $2_vglu2b_raw.nii  -n 8 -o $2 -t s

~/LD_NeuralNetwork/bin/ANTs/install/bin/antsApplyTransforms -d 3 -v 0 -n WelchWindowedSinc -i $2_gad1b_raw.nii -r T_AVG_vglu2b_template.nii -o $2'_gad1b_registered.nii.gz' -t $2'1Warp.nii.gz' -t $2'0GenericAffine.mat'

~/LD_NeuralNetwork/bin/ANTs/install/bin/antsApplyTransforms -d 3 -v 0 -n WelchWindowedSinc -i $2_nos1_raw.nii -r T_AVG_vglu2b_template.nii  -o $2'_nos1_registered.nii.gz' -t $2'1Warp.nii.gz' -t $2'0GenericAffine.mat'

 ~/LD_NeuralNetwork/bin/ANTs/install/bin/antsApplyTransforms -d 3 -v 0 -n WelchWindowedSinc -i $2_vglu2b_raw.nii -r T_AVG_vglu2b_template.nii  -o $2'_vglu2b_registered.nii.gz' -t $2'1Warp.nii.gz' -t $2'0GenericAffine.mat'






