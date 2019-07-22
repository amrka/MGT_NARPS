from nipype import config
cfg = dict(execution={'remove_unnecessary_outputs': False})
config.update_config(cfg)

import nipype.interfaces.fsl as fsl
import nipype.interfaces.afni as afni
import nipype.interfaces.ants as ants
import nipype.interfaces.spm as spm

from nipype.interfaces.utility import IdentityInterface, Function, Select, Merge
from os.path import join as opj
from nipype.interfaces.io import SelectFiles, DataSink
from nipype.pipeline.engine import Workflow, Node, MapNode

import numpy as np
import os, re
import matplotlib.pyplot as plt
from nipype.interfaces.matlab import MatlabCommand
MatlabCommand.set_default_paths('/Users/amr/Downloads/spm12')
MatlabCommand.set_default_matlab_cmd("matlab -nodesktop -nosplash")

# import nipype.interfaces.matlab as mlab
# mlab.MatlabCommand.set_default_matlab_cmd("matlab -nodesktop -nosplash")
# mlab.MatlabCommand.set_default_paths('/home/amr/Documents/MATLAB/toolbox/spm8')

#==========================================================================================================================================================
# In[2]:

experiment_dir = '/media/amr/Amr_4TB/NARPS/' 


task_list = ['gain','loss']


zstat_list = ['zstat1', 
              'zstat2',
              'zstat3',
              'zstat4',
              'zstat5',
              'zstat6']

                
output_dir  = '/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level_post_fitting'
working_dir = '/media/amr/Amr_4TB/NARPS/workingdir_narps_proc_3rd_level_post_fitting'


no_runs = 4

proc_3rd_level = Workflow (name = 'proc_3rd_level')
proc_3rd_level.base_dir = opj(experiment_dir, working_dir)


#==========================================================================================================================================================
# In[3]:
#to prevent nipype from iterating over the anat image with each func run-, you need seperate
#nodes to select the files
#and this will solve the problem I have for almost 6 months
#but notice that in the sessions, you have to iterate also over subject_id to get the {subject_id} var



# Infosource - a function free node to iterate over the list of subject names

infosource = Node(IdentityInterface(fields=['tasks', 'zstats' ]),
                  name="infosource")
infosource.iterables = [('tasks', task_list),
                        ('zstats', zstat_list)]


#==========================================================================================================================================================
# In[4]:
# sub-001_task-MGT_run--02_bold.nii.gz, sub-001_task-MGT_run--02_sbref.nii.gz
#/preproc_img/run--04sub-119/smoothed_all_maths_filt_maths.nii.gz
#functional run-s

out_1st = '/media/amr/Amr_4TB/NARPS/output_narps_proc_1st_level'
out_pre = '/media/amr/Amr_4TB/NARPS/output_narps_preproc_preproc'
study_template = '/Volumes/Amr_1TB/NARPS/narps_templateBrainExtractionBrain.nii.gz'
study_mask = '/Volumes/Amr_1TB/NARPS/narps_templateBrainExtractionMask.nii.gz'
MNI_1mm = '/usr/local/fsl/data/standard/MNI152_T1_1mm_brain.nii.gz'



templates = {

          'zstat'           :  '/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/{tasks}_stat_flameo_neg/+/{zstats}.nii.gz',
        }



selectfiles = Node(SelectFiles(templates,
                              base_directory=experiment_dir),
                              name="selectfiles")
#==========================================================================================================================================================
# In[5]:

datasink = Node(DataSink(), name = 'datasink')
datasink.inputs.container = output_dir
datasink.inputs.base_directory = experiment_dir

substitutions = [('_tasks_', ''),('_zstats_', '_')]

datasink.inputs.substitutions = substitutions

#==========================================================================================================================================================
#Smooth estimation
def smooth_est(zstat):
     import nipype.interfaces.fsl as fsl
     import os
     study_mask = '/Volumes/Amr_1TB/NARPS/narps_templateBrainExtractionMask.nii.gz'

     smooth_est = fsl.SmoothEstimate()
     smooth_est.inputs.dof = 53
     smooth_est.inputs.mask_file = study_mask


     if zstat[-36:-32] == 'gain':
          res4d = '/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/gain_stat_flameo_neg/+/res4d.nii.gz'
     elif zstat[-36:-32] == 'loss':
          res4d = '/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/loss_stat_flameo_neg/+/res4d.nii.gz'

     print(res4d)


     smooth_est.inputs.residual_fit_file = res4d
     smooth_est_outputs = smooth_est.run()

     print(zstat[-36:-32])
     dlh = smooth_est_outputs.outputs.dlh
     volume = smooth_est_outputs.outputs.volume
     resels = smooth_est_outputs.outputs.resels


     return dlh, volume, resels

smooth_est = Node(name = 'smooth_est',
                  interface = Function(input_names = ['zstat'],
                  output_names = ['dlh', 'volume', 'resels'],
                  function = smooth_est))

#==========================================================================================================================================================
#mask zstat1

# mask_zstat = Node(fsl.ApplyMask(), name='mask_zstat')
# mask_zstat.inputs.mask_file = study_mask
# mask_zstat.inputs.out_file = 'thresh_zstat.nii.gz'


#==========================================================================================================================================================
#cluster zstats1

def cluster_zstats(zstat, volume, dlh):

        import nipype.interfaces.fsl as fsl
        import os


        study_mask = '/Volumes/Amr_1TB/NARPS/narps_templateBrainExtractionMask.nii.gz'

        cope_no = zstat[-8] #number of the zstat file after taking into account .nii.gz

        if zstat[-36:-32] == 'gain':
            cope = '/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/gain_stat_flameo_neg/+/cope{0}.nii.gz'.format(cope_no)
        elif zstat[-36:-32] == 'loss':
            cope = '/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/loss_stat_flameo_neg/+/cope{0}.nii.gz'.format(cope_no)

        #mask here not in a seperate node, because I need the original zstat to get the number    
        mask_zstat = fsl.ApplyMask()
        mask_zstat.inputs.in_file = zstat
        mask_zstat.inputs.mask_file = study_mask
        mask_zstat_outputs = mask_zstat.run()
        masked_zstat = mask_zstat_outputs.outputs.out_file



        cluster_zstats = fsl.Cluster()

        cluster_zstats.inputs.in_file = masked_zstat
        cluster_zstats.inputs.cope_file = cope
        cluster_zstats.inputs.threshold = 3.1
        cluster_zstats.inputs.pthreshold = 0.001
        cluster_zstats.inputs.connectivity = 26
        cluster_zstats.inputs.volume = volume
        cluster_zstats.inputs.dlh = dlh

        cluster_zstats.inputs.out_threshold_file = 'thresh_zstat.nii.gz'
        cluster_zstats.inputs.out_index_file = 'cluster_mask_zstat.nii.gz'
        cluster_zstats.inputs.out_localmax_txt_file = 'lmax_zstat_std.txt'
        cluster_zstats.inputs.use_mm = True
        print(cluster_zstats.cmdline)



        cluster_zstats_outputs = cluster_zstats.run()

        threshold_file = cluster_zstats_outputs.outputs.threshold_file




        return  masked_zstat, threshold_file   

cluster_zstats = Node(name = 'cluster_zstats',
                  interface = Function(input_names = ['zstat', 'volume', 'dlh'],
                  output_names = ['threshold_file', 'masked_zstat'],
                  function = cluster_zstats))

#==========================================================================================================================================================
#Move the images to MNI space with precalculated transformations
unthresh_2_MNI = Node(ants.ApplyTransforms(), name='unthresh_2_MNI')
unthresh_2_MNI.inputs.reference_image = MNI_1mm
unthresh_2_MNI.inputs.transforms = '/Volumes/Amr_1TB/NARPS/narps_to_MNI_1mm_Composite.h5'
unthresh_2_MNI.inputs.dimension = 3
unthresh_2_MNI.inputs.output_image = 'unthreshold_file_MNI.nii.gz'


#==========================================================================================================================================================
#threshold the maps to 3.1 to make it ready for submission
thresh_2_MNI = unthresh_2_MNI.clone(name='thresh_2_MNI')

#==========================================================================================================================================================
#overlay thresh_zstat1

overlay_zstat = Node(fsl.Overlay(), name='overlay')
overlay_zstat.inputs.auto_thresh_bg = True
overlay_zstat.inputs.stat_thresh = (3.1,10) #threshold positive and negative
overlay_zstat.inputs.transparency = True
overlay_zstat.inputs.out_file = 'rendered_thresh_zstat.nii.gz'
overlay_zstat.inputs.show_negative_stats = True
overlay_zstat.inputs.background_image = MNI_1mm

#==========================================================================================================================================================
#generate pics thresh_zstat1

slicer_zstat = Node(fsl.Slicer(), name='slicer')
slicer_zstat.inputs.sample_axial = 2
slicer_zstat.inputs.image_width = 2000
slicer_zstat.inputs.out_file = 'rendered_thresh_zstat.png'





proc_3rd_level.connect([


              (infosource, selectfiles, [('tasks','tasks'),
                                         ('zstats','zstats')]),


              (selectfiles, smooth_est, [('zstat','zstat')]),


              (selectfiles, cluster_zstats, [('zstat','zstat')]), #I need the original file to get the number and then i mask it inside the function
              (smooth_est, cluster_zstats, [('volume','volume'),
                                            ('dlh','dlh')]),

              (cluster_zstats, unthresh_2_MNI, [('masked_zstat','input_image')]),

              (cluster_zstats, thresh_2_MNI, [('threshold_file','input_image')]),


              (thresh_2_MNI, overlay_zstat, [('output_image','stat_image')]),

              (overlay_zstat, slicer_zstat, [('out_file','in_file')]),

              (unthresh_2_MNI, datasink, [('output_image','unthreshold_file')]),
              (thresh_2_MNI, datasink, [('output_image','threshold_file')]),
              (slicer_zstat, datasink, [('out_file','activation_pic')]),



              ])

proc_3rd_level.write_graph(graph2use='colored', format='png', simple_form=True)

proc_3rd_level.run('MultiProc', plugin_args={'n_procs': 8})
