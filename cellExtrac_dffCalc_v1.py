#!/usr/bin/env python
#!modul load h5py

import cv2
from matplotlib import animation
import glob
import logging
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import caiman as cm
import re 
from os import listdir
from os.path import isfile, join                                                
from caiman.motion_correction import MotionCorrect                              
from caiman.source_extraction.cnmf import cnmf as cnmf                          
from caiman.source_extraction.cnmf import params as params                      
from caiman.utils.utils import download_demo 
import subprocess
from future.utils import old_div
from matt_functions import com
print (cm)
print ("DONE!")
'''
try:
    cv2.setNumThreads(0)
except:
    pass

import caiman as cm
from caiman.motion_correction import MotionCorrect
from caiman.source_extraction.cnmf import cnmf as cnmf
from caiman.source_extraction.cnmf import params as params
from caiman.utils.utils import download_demo
'''

DFF_folder = sys.argv[1]#argument1 specifies the input data folder


logging.basicConfig(format=
                    "%(relativeCreated)12d [%(filename)s:%(funcName)20s():%(lineno)s]"\
                    "[%(process)d] %(message)s",
                    level=logging.INFO)

all_input_data_file_raw = [f for f in listdir(DFF_folder) if isfile  (join(DFF_folder, f))]

all_input_data_file = []
for fish_id in range(len(all_input_data_file_raw)):
    if os.path.basename(all_input_data_file_raw[fish_id][-3:])  == 'tif' and os.path.basename(all_input_data_file_raw[fish_id][:4]) == 'Fish':        
        all_input_data_file.append (os.path.basename(all_input_data_file_raw[fish_id]))

all_input_data_file.sort()
print (all_input_data_file)

# ----------------------------------------------------


fr = 1.1                             # imaging rate in frames per second
decay_time = 1.7                   # length of a typical transient in seconds

# motion correction parameters
strides = (8, 8)          # start a new patch for pw-rigid motion correction every x pixels
overlaps = (25, 25)         # overlap between pathes (size of patch strides+overlaps)
max_shifts = (6,6)          # maximum allowed rigid shifts (in pixels)
max_deviation_rigid = 3     # maximum shifts deviation allowed for patch with respect to rigid shifts
pw_rigid = True             # flag for performing non-rigid motion correction

# parameters for source extraction and deconvolution
p = 1                       # order of the autoregressive system
gnb = 2                     # number of global background components
merge_thr = 2               # merging threshold, max correlation allowed
rf = 12                     # half-size of the patches in pixels. e.g., if rf=25, patches are 50x50
stride_cnmf = 5             # amount of overlap between the patches in pixels
K = 8                       # number of components per patch
gSig = [2, 2]               # expected half size of neurons in pixels
method_init = 'greedy_roi'  # initialization method (if analyzing dendritic data using 'sparse_nmf')
ssub = 1                    # spatial subsampling during initialization
tsub = 1                    # temporal subsampling during intialization

# parameters for component evaluation
min_SNR = 0.5               # signal to noise ratio for accepting a component
rval_thr = 0              # space correlation threshold for accepting a component
cnn_thr = 0.1              # threshold for CNN based classifier

cnn_lowest = 0.1  # neurons with cnn probability lower than this value are rejected


"""
MAHDI ZAREI; 10-11-2019
"""


dff_all = {}
coor_all = {}
print('jiale')

#for stack_id in range (0, len(all_input_data_file)): # (2,8)

# ......................................................#
#                   zNO_to_analyse                      #
#              SHOULD BE SET BY USER                    #
# ......................................................#                                                                                                  
zNO_to_analyse = int(sys.argv[2]) # argument2 is the start number of the image stack   

#for stack_id in range (zNO_to_analyse, int(sys.argv[3])):#argument3 is the number of image stacks
for stack_id in range (zNO_to_analyse, zNO_to_analyse+1): # JX 03-20-2022                                                                        
#%% Select file(s) to be processed (download if not present)
    movie_file_address = DFF_folder + all_input_data_file[stack_id]
    
    fnames = [download_demo(movie_file_address)]
    #fnames = [download_demo("demoMovie.tif")]

    print (movie_file_address)    
    print (fnames)

    opts_dict = {'fnames': fnames,
                'fr': fr,
                'decay_time': decay_time,
                'strides': strides,
                'overlaps': overlaps,
                'max_shifts': max_shifts,
                'max_deviation_rigid': max_deviation_rigid,
                'pw_rigid': pw_rigid,
                'p': 1,
                'nb': gnb,
                'rf': rf,
                'K': K,
                'gSig' : gSig,
                'stride': stride_cnmf,
                'method_init': method_init,
                'rolling_sum': True,
                'only_init': True,
                'ssub': ssub,
                'tsub': tsub,
                'merge_thr': merge_thr, 
                'min_SNR': min_SNR,
                'rval_thr': rval_thr,
                'use_cnn': True,
                'min_cnn_thr': cnn_thr,
                'cnn_lowest': cnn_lowest}

    opts = params.CNMFParams(params_dict=opts_dict)       
    
    Zstep = stack_id    
    
    opts_dict = {'fnames': fnames,
                'fr': fr,
                'decay_time': decay_time,
                'strides': strides,
                'overlaps': overlaps,
                'max_shifts': max_shifts,
                'max_deviation_rigid': max_deviation_rigid,
                'pw_rigid': pw_rigid,
                'p': 1,
                'nb': gnb,
                'rf': rf,
                'K': K, 
                'gSig' : gSig,
                'stride': stride_cnmf,
                'method_init': method_init,
                'rolling_sum': True,
                'only_init': True,
                'ssub': ssub,
                'tsub': tsub,
                'merge_thr': merge_thr, 
                'min_SNR': min_SNR,
                'rval_thr': rval_thr,
                'use_cnn': True,
                'min_cnn_thr': cnn_thr,
                'cnn_lowest': cnn_lowest}

    opts = params.CNMFParams(params_dict=opts_dict)    

    #%% start a cluster for parallel processing (if a cluster already exists it will be closed and a new session will be opened)
    if 'dview' in locals():
        cm.stop_server(dview=dview)
    c, dview, n_processes = cm.cluster.setup_cluster(
        backend='local', n_processes=None, single_thread=False)    

    # first we create a motion correction object with the parameters specified
    mc = MotionCorrect(fnames, dview=dview, **opts.get_group('motion'))
    # note that the file is not loaded in memory

    #%% Run piecewise-rigid motion correction using NoRMCorre
    mc.motion_correct(save_movie=True)
    m_els = cm.load(mc.fname_tot_els)
    border_to_0 = 0 if mc.border_nan is 'copy' else mc.border_to_0 
        # maximum shift to be used for trimming against NaNs          
        
    display_movie = False
    if display_movie:
        m_orig = cm.load_movie_chain(fnames)
        ds_ratio = 0.2
        cm.concatenate([m_orig.resize(1, 1, ds_ratio) - mc.min_mov*mc.nonneg_movie,
                        m_els.resize(1, 1, ds_ratio)], 
                       axis=2).play(fr=60, gain=15, magnification=2, offset=0)  # press q to exit        
        
        
    #%% MEMORY MAPPING
    # memory map the file in order 'C'
    fname_new = cm.save_memmap(mc.mmap_file, base_name=all_input_data_file[stack_id][:-4]+'memmap_', order='C',border_to_0=border_to_0) # exclude borders
    print('memmap_c_saved')

    # now load the file
    Yr, dims, T = cm.load_memmap(fname_new)
    images = np.reshape(Yr.T, [T] + list(dims), order='F') 
        #load frames in python format (T x X x Y)                
        
    #%% restart cluster to clean up memory
    cm.stop_server(dview=dview)
    c, dview, n_processes = cm.cluster.setup_cluster(
        backend='local', n_processes=None, single_thread=False)        
    
    
    #%% RUN CNMF ON PATCHES

    # First extract spatial and temporal components on patches and combine them
    # for this step deconvolution is turned off (p=0)
    opts.change_params({'p': 0})
    cnm = cnmf.CNMF(n_processes, params=opts, dview=dview)
    cnm = cnm.fit(images)
    #plt.close()
    
    
    
    #%% plot contours of found components
    Cn = cm.local_correlations(images.transpose(1,2,0))
    Cn[np.isnan(Cn)] = 0
    cnm.estimates.plot_contours_nb(img=Cn)

    fig = plt.figure (figsize= (10,9))
    plt.imshow(Cn, aspect='auto')
    fig.savefig ( DFF_folder + os.path.basename(all_input_data_file[stack_id][:-4]) + ".jpg")
    print ("Done 02!")
    #plt.close()
    
    fig = plt.figure (figsize= (10,9))
    plt.imshow(Cn, aspect='auto')
    #plt.close()
    
    #%% RE-RUN seeded CNMF on accepted patches to refine and perform deconvolution 
    cnm.params.change_params({'p': p})
    cnm2 = cnm.refit(images, dview=dview)        
    #plt.close()    
    
    #%% COMPONENT EVALUATION
    # the components are evaluated in three ways:
    #   a) the shape of each component must be correlated with the data
    #   b) a minimum peak SNR is required over the length of a transient
    #   c) each shape passes a CNN based classifier

    cnm2.estimates.evaluate_components(images, cnm2.params, dview=dview)


    # MAHDI ...
    #fr = 1.25 # approx final rate  (after eventual downsampling )
    #decay_time = 1.8  # length of typical transient in seconds 
    use_cnn = False  # CNN classifier is designed for 2d (real) data
    #min_SNR = 3      # accept components with that peak-SNR or higher
    #rval_thr = 0.7   # accept components iwth speace correlation threshold or higher
    cnm2.params.change_params(params_dict={'fr': fr,
                                          'decay_time': decay_time,
                                          'min_SNR': min_SNR,
                                          'rval_thr': rval_thr,
                                          'use_cnn': use_cnn})    

 
    print (" 01     ------------------- cnm2.estimates.idx_components    ")
    print (np.shape(cnm2.estimates.idx_components ))

    
    #%% PLOT COMPONENTS
    cnm2.estimates.htmlpath = DFF_folder + os.path.basename(all_input_data_file[stack_id][:-4])+'.html'
    cnm2.estimates.plot_contours_nb(img=Cn, idx=cnm2.estimates.idx_components)

    
    # accepted components
    cnm2.estimates.nb_view_components(img=Cn, idx=cnm2.estimates.idx_components)   

    print (" 02     ------------------- cnm2.estimates.idx_components    ")
    print (np.shape(cnm2.estimates.idx_components ))
    print (np.shape(cnm2.estimates.C ))

   
    # rejected components if 3==6: len(cnm2.estimates.idx_components_bad) > 0:
    if len(cnm2.estimates.idx_components_bad) > 0:
        cnm2.estimates.nb_view_components(img=Cn, idx=cnm2.estimates.idx_components_bad)
    else:
        print("No components were rejected.")    
    
    print (" 03     ------------------- cnm2.estimates.idx_components    ")
    print (np.shape(cnm2.estimates.idx_components ))
    print (np.shape(cnm2.estimates.C ))


    #%% Extract DF/F values
    cnm2.estimates.detrend_df_f(quantileMin=8, frames_window=250)
    #cnm2.estimates.detrend_df_f(use_residuals = True) # MAHDI
    
    # We retain the original indices                                                                                                        
    idx_comp = cnm2.estimates.idx_components
    idx_comp_bad = cnm2.estimates.idx_components_bad


    print (" 04     ------------------- cnm2.estimates.idx_components    ")
    print (np.shape(cnm2.estimates.idx_components ))
    print (np.shape(cnm2.estimates.C ))
 
    # Center of the COORDINATES of all cells are extacted                                                                                                                  
    stack_coord = [[cnm2.estimates.coordinates[i]['CoM'][1] ,
                cnm2.estimates.coordinates[i]['CoM'][0]] for i in idx_comp]# range(len(cnm2.estimates.C))  #MZ 02-03-2020                                                  


    # Select only high quality components
    cnm2.estimates.select_components(use_object=True)    

    # Display final results
    cnm2.estimates.nb_view_components(img=Cn, denoised_color='red')
    
    # Jan 03 - MZ
    save_results = False
    if save_results:
        cnm2.save('analysis_results'+ str (stack_id) +'.hdf5')
 
    
    # dff signals filtered using gaussian method by MAHDI 
    '''
    dff_denoised_fsh = [sp.ndimage.filters.gaussian_filter 
                        (cnm2.estimates.F_dff [i], sigma= 0.8) 
                        for i in range(len( cnm2.estimates.F_dff))]                        
    '''
    
    
    # Center of the COORDINATES of all cells are extacted
    '''
    coord_aver_fsh = [cnm2.estimates.coordinates[i]['CoM'] 
                      for i in range(len(cnm2.estimates.coordinates))
    #                   if cnm2.estimates.coordinates[i]['neuron_id']  in idx_comp  
                     ]
    coord_aver_fsh = [coord_aver_fsh[idx_comp[i]] for i in range(len(idx_comp))]    
    '''
    
    print (" 05     ------------------- cnm2.estimates.idx_components    ")
    print (np.shape(cnm2.estimates.idx_components ))
    print (np.shape(cnm2.estimates.C ))

    stack_dff = cnm2.estimates.C
    '''
    # Center of the COORDINATES of all cells are extacted    
    stack_coord = [[cnm2.estimates.coordinates[i]['CoM'][1] , 
                cnm2.estimates.coordinates[i]['CoM'][0]] for i in idx_comp]# range(len(cnm2.estimates.C))  #MZ 02-03-2020
    '''
    '''
    stack_coord = [[cnm2.estimates.coordinates[i]['CoM'][1] ,
                cnm2.estimates.coordinates[i]['CoM'][0]] for i in range(len(cnm2.estimates.C))  #MZ 02-10-2020 idx_comp
    '''

    print ("      ------------------- stack dff @ coord    ")
    print (np.shape(stack_dff ))
    print (np.shape(stack_coord ))

    # MZ 02-03-2020 DEACTIVATED TO GET ONLY ON STACK RESULTS 
    #dff_all [stack_id] = stack_dff
    #coor_all [stack_id] = stack_coord
    
    # SAVE DFF HEATMAP
    fig = plt.figure (figsize= (10,9))
    plt.imshow(stack_dff, aspect='auto')
    plt.xlabel("Time", fontsize=17)
    plt.ylabel ("Cell", fontsize =17)
    plt.title (" DF/F of stack {}".format(os.path.basename(all_input_data_file[stack_id][:-4])),fontsize=20)
    fig.savefig ( DFF_folder + os.path.basename(all_input_data_file[stack_id][:-4]) + "_stack_id_dff.jpg")
    

    # SAVE image and the detected cells together
    coor_x = [stack_coord[i][0] for i in range(len(stack_coord))]
    coor_y = [stack_coord[i][1] for i in range(len(stack_coord))]
    fig = plt.figure (figsize= (10,10))
    plt.imshow(Cn)
    plt.scatter (coor_x,coor_y, s= 50, facecolors = 'none', color = '#ff0015')
    plt.title (" Detected ROIs stack {}".format(os.path.basename(all_input_data_file[stack_id][:-4])),fontsize=20)
    fig.savefig ( DFF_folder + os.path.basename(all_input_data_file[stack_id][:-4]) + "_detected_ROIs.jpg")

    

    print ("------------------------------------------------")
    #MZ 02-19-2020  +  02-17-2020
    np.savez ( DFF_folder + os.path.basename(all_input_data_file[stack_id][:-4]),
              dff = stack_dff,
              coord = stack_coord )
    print ("Size of dff = {}".format(str(np.shape(stack_dff  ) )))
    print ("Size of coord = {}".format(str(np.shape(stack_coord  ) )))

    # MZ 02-19-2020
    crt = com (cnm2.estimates.A , cnm2.estimates.dims[0] , cnm2.estimates.dims[1])
    print ("Center of mass for spatial components (K x 2) ") 
    print (np.shape(crt))

    np.savez ( DFF_folder + os.path.basename(all_input_data_file[stack_id][:-4]) + "_sparse_matrix_A" ,
                      com_A = crt )
    
    '''
    np.savez ( DFF_folder + os.path.basename(all_input_data_file[stack_id][:-4]),
               C = cnm2.estimates.C,
               A = cnm2.estimates.A,
               d1 = cnm2.estimates.dims[0],
               d2 = cnm2.estimates.dims[1],
               coord = stack_coord )
    '''
       
    #%% STOP CLUSTER and clean up log files
    cm.stop_server(dview=dview)
    log_files = glob.glob('*_LOG_*')
    for log_file in log_files:
        os.remove(log_file)   
    
    command = 'rm ' + DFF_folder + os.path.basename(all_input_data_file[stack_id][:-4]) + '_els__d1_512_d2_1024_d3_1_order_F_frames_900_.mmap'
    command = command.split()
    subprocess.run(command)
