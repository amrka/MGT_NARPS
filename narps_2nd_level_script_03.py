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

experiment_dir = '/home/in/aeed/NARPS/' 

subject_list = [
                 'sub-001', 'sub-002', 'sub-003', 'sub-004', 'sub-005', 'sub-006', 'sub-008', 'sub-009', 
                 'sub-010', 'sub-011', 'sub-013', 'sub-014', 'sub-015', 'sub-016', 'sub-017', 'sub-018',
                 'sub-019', 'sub-020', 'sub-021', 'sub-022', 'sub-024', 'sub-025', 'sub-026', 'sub-027', 
                 'sub-029', 'sub-030', 'sub-032', 'sub-033', 'sub-035', 'sub-036', 'sub-037', 'sub-038', 
                 'sub-039', 'sub-040', 'sub-041', 'sub-043', 'sub-044', 'sub-045', 'sub-046', 'sub-047', 
                 'sub-049', 'sub-050', 'sub-051', 'sub-052', 'sub-053', 'sub-054', 'sub-055', 'sub-056', 
                 'sub-057', 'sub-058', 'sub-059', 'sub-060', 'sub-061', 'sub-062', 'sub-063', 'sub-064', 
                 'sub-066', 'sub-067', 'sub-068', 'sub-069', 'sub-070', 'sub-071', 'sub-072', 'sub-073', 
                 'sub-074', 'sub-075', 'sub-076', 'sub-077', 'sub-079', 'sub-080', 'sub-081', 'sub-082', 
                 'sub-083', 'sub-084', 'sub-085', 'sub-087', 'sub-088', 'sub-089', 'sub-090', 'sub-092', 
                 'sub-093', 'sub-094', 'sub-095', 'sub-096', 'sub-098', 'sub-099', 'sub-100', 'sub-102', 
                 'sub-103', 'sub-104', 'sub-105', 'sub-106', 'sub-107', 'sub-108', 'sub-109', 'sub-110', 
                 'sub-112', 'sub-113', 'sub-114', 'sub-115', 'sub-116', 'sub-117', 'sub-118', 'sub-119', 
                 'sub-120', 'sub-121', 'sub-123', 'sub-124'
 ]

                





                
output_dir  = '/home/in/aeed/NARPS/output_narps_proc_2nd_level'
working_dir = '/home/in/aeed/NARPS/workingdir_narps_proc_2nd_level'


no_runs = 4

proc_2nd_level = Workflow (name = 'proc_2nd_level')
proc_2nd_level.base_dir = opj(experiment_dir, working_dir)


#==========================================================================================================================================================
# In[3]:
#to prevent nipype from iterating over the anat image with each func run-, you need seperate
#nodes to select the files
#and this will solve the problem I have for almost 6 months
#but notice that in the sessions, you have to iterate also over subject_id to get the {subject_id} var



# Infosource - a function free node to iterate over the list of subject names

infosource = Node(IdentityInterface(fields=['subject_id']),
                  name="infosource")
infosource.iterables = [('subject_id', subject_list)]


#==========================================================================================================================================================
# In[4]:
# sub-001_task-MGT_run--02_bold.nii.gz, sub-001_task-MGT_run--02_sbref.nii.gz
#/preproc_img/run--04sub-119/smoothed_all_maths_filt_maths.nii.gz
#functional run-s

out_1st = '/home/in/aeed/NARPS/output_narps_proc_1st_level'
out_pre = '/home/in/aeed/NARPS/output_narps_preproc_preproc'
study_template = '/home/in/aeed/NARPS/narps_templateBrainExtractionBrain.nii.gz'

templates = {


          'anat_brain'           :  '/home/in/aeed/NARPS/output_narps_preproc_preproc/anat_brain/{subject_id}/highres001_BrainExtractionBrain.nii.gz',
          'mask_brain'           :  '/home/in/aeed/NARPS/output_narps_preproc_preproc/anat_mask/{subject_id}/highres001_BrainExtractionMask.nii.gz',

          'func_2_anat_trans_r1' :  '/home/in/aeed/NARPS/output_narps_preproc_preproc/func_2_anat_trans/run-01{subject_id}/sbref_2_anat_{subject_id}0GenericAffine.mat',
          'func_2_anat_trans_r2' :  '/home/in/aeed/NARPS/output_narps_preproc_preproc/func_2_anat_trans/run-02{subject_id}/sbref_2_anat_{subject_id}0GenericAffine.mat',
          'func_2_anat_trans_r3' :  '/home/in/aeed/NARPS/output_narps_preproc_preproc/func_2_anat_trans/run-03{subject_id}/sbref_2_anat_{subject_id}0GenericAffine.mat',
          'func_2_anat_trans_r4' :  '/home/in/aeed/NARPS/output_narps_preproc_preproc/func_2_anat_trans/run-04{subject_id}/sbref_2_anat_{subject_id}0GenericAffine.mat',

	  'func_2_template'      :  '/home/in/aeed/NARPS/output_narps_preproc_preproc/anat_2_temp_trans/{subject_id}/transformComposite.h5',


#==========================================================================================================================================================

          'cope1_r1'             : '/home/in/aeed/NARPS/output_narps_proc_1st_level/copes/run-01{subject_id}/cope1.nii.gz',
          'cope1_r2'             : '/home/in/aeed/NARPS/output_narps_proc_1st_level/copes/run-02{subject_id}/cope1.nii.gz',
          'cope1_r3'             : '/home/in/aeed/NARPS/output_narps_proc_1st_level/copes/run-03{subject_id}/cope1.nii.gz',
          'cope1_r4'             : '/home/in/aeed/NARPS/output_narps_proc_1st_level/copes/run-04{subject_id}/cope1.nii.gz',
      

          'varcope1_r1'          : '/home/in/aeed/NARPS/output_narps_proc_1st_level/varcopes/run-01{subject_id}/varcope1.nii.gz',
          'varcope1_r2'          : '/home/in/aeed/NARPS/output_narps_proc_1st_level/varcopes/run-02{subject_id}/varcope1.nii.gz',
          'varcope1_r3'          : '/home/in/aeed/NARPS/output_narps_proc_1st_level/varcopes/run-03{subject_id}/varcope1.nii.gz',
          'varcope1_r4'          : '/home/in/aeed/NARPS/output_narps_proc_1st_level/varcopes/run-04{subject_id}/varcope1.nii.gz',
#==========================================================================================================================================================
          'cope2_r1'             : '/home/in/aeed/NARPS/output_narps_proc_1st_level/copes/run-01{subject_id}/cope2.nii.gz',
          'cope2_r2'             : '/home/in/aeed/NARPS/output_narps_proc_1st_level/copes/run-02{subject_id}/cope2.nii.gz',
          'cope2_r3'             : '/home/in/aeed/NARPS/output_narps_proc_1st_level/copes/run-03{subject_id}/cope2.nii.gz',
          'cope2_r4'             : '/home/in/aeed/NARPS/output_narps_proc_1st_level/copes/run-04{subject_id}/cope2.nii.gz',
      

          'varcope2_r1'          : '/home/in/aeed/NARPS/output_narps_proc_1st_level/varcopes/run-01{subject_id}/varcope2.nii.gz',
          'varcope2_r2'          : '/home/in/aeed/NARPS/output_narps_proc_1st_level/varcopes/run-02{subject_id}/varcope2.nii.gz',
          'varcope2_r3'          : '/home/in/aeed/NARPS/output_narps_proc_1st_level/varcopes/run-03{subject_id}/varcope2.nii.gz',
          'varcope2_r4'          : '/home/in/aeed/NARPS/output_narps_proc_1st_level/varcopes/run-04{subject_id}/varcope2.nii.gz',
#==========================================================================================================================================================

        }



selectfiles = Node(SelectFiles(templates,
                              base_directory=experiment_dir),
                              name="selectfiles")
#==========================================================================================================================================================
# In[5]:

datasink = Node(DataSink(), name = 'datasink')
datasink.inputs.container = output_dir
datasink.inputs.base_directory = experiment_dir

substitutions = [('_subject_id_', ''),('_contrast_id_', '')]

datasink.inputs.substitutions = substitutions

#==========================================================================================================================================================
#Create a desing for 2snd level

l2model = Node(fsl.model.L2Model(), name='create_2nd_level_desing')


#==========================================================================================================================================================
#Apply transformations to each cope

def copes1_2_anat_func(fixed, cope1_r1, cope1_r2, cope1_r3, cope1_r4, func_2_anat_trans_r1, func_2_anat_trans_r2, func_2_anat_trans_r3, func_2_anat_trans_r4, mask_brain):
        import os, re
        import nipype.interfaces.ants as ants
        import nipype.interfaces.fsl as fsl

        cwd = os.getcwd()


        copes1 = [cope1_r1,cope1_r2,cope1_r3,cope1_r4]
        trans  = [func_2_anat_trans_r1, func_2_anat_trans_r2, func_2_anat_trans_r3, func_2_anat_trans_r4]

        copes1_2_anat = []
        FEtdof_t1_2_anat = []
        for i in range(len(copes1)):
              moving = copes1[i]
              transform = trans[i]
              ants_apply = ants.ApplyTransforms()
              ants_apply.inputs.dimension = 3
              ants_apply.inputs.input_image = moving
              ants_apply.inputs.reference_image = fixed
              ants_apply.inputs.transforms = transform
              ants_apply.inputs.output_image = 'cope1_2_anat_r{0}.nii.gz'.format(i+1)
              

              ants_apply.run()

              copes1_2_anat.append(os.path.abspath('cope1_2_anat_r{0}.nii.gz'.format(i+1)))

              dof = fsl.ImageMaths()
              dof.inputs.in_file = 'cope1_2_anat_r{0}.nii.gz'.format(i+1)
              dof.inputs.op_string = '-mul 0 -add 448 -mas'
              dof.inputs.in_file2 = mask_brain
              dof.inputs.out_file = 'FEtdof_t1_2_anat_r{0}.nii.gz'.format(i+1)

              dof.run()
              
              FEtdof_t1_2_anat.append(os.path.abspath('FEtdof_t1_2_anat_r{0}.nii.gz'.format(i+1)))


        merge = fsl.Merge()
        merge.inputs.dimension = 't'
        merge.inputs.in_files = copes1_2_anat
        merge.inputs.merged_file = 'copes1_2_anat.nii.gz'
        merge.run() 

        merge.inputs.in_files = FEtdof_t1_2_anat
        merge.inputs.merged_file = 'dofs_t1_2_anat.nii.gz'
        merge.run()

        copes1_2_anat = os.path.abspath('copes1_2_anat.nii.gz')
        dofs_t1_2_anat = os.path.abspath('dofs_t1_2_anat.nii.gz')
        
        return copes1_2_anat, dofs_t1_2_anat


copes1_2_anat_func = Node(name = 'copes1_2_anat_func',
                          interface = Function(input_names = 
                                              ['fixed', 
                                               'cope1_r1', 
                                               'cope1_r2', 
                                               'cope1_r3', 
                                               'cope1_r4', 
                                               'func_2_anat_trans_r1', 
                                               'func_2_anat_trans_r2', 
                                               'func_2_anat_trans_r3', 
                                               'func_2_anat_trans_r4',
                                               'mask_brain'],
                           output_names = ['copes1_2_anat', 'dofs_t1_2_anat'],
                           function = copes1_2_anat_func))


#==========================================================================================================================================================

def varcopes1_2_anat_func(fixed, varcope1_r1, varcope1_r2, varcope1_r3, varcope1_r4, func_2_anat_trans_r1, func_2_anat_trans_r2, func_2_anat_trans_r3, func_2_anat_trans_r4):
        import os, re
        import nipype.interfaces.ants as ants
        import nipype.interfaces.fsl as fsl

        cwd = os.getcwd()


        varcopes1 = [varcope1_r1,varcope1_r2,varcope1_r3,varcope1_r4]
        trans  = [func_2_anat_trans_r1, func_2_anat_trans_r2, func_2_anat_trans_r3, func_2_anat_trans_r4]

        varcopes1_2_anat = []

        for i in range(len(varcopes1)):
              moving = varcopes1[i]
              transform = trans[i]
              ants_apply = ants.ApplyTransforms()
              ants_apply.inputs.dimension = 3
              ants_apply.inputs.input_image = moving
              ants_apply.inputs.reference_image = fixed
              ants_apply.inputs.transforms = transform
              ants_apply.inputs.output_image = 'varcope1_2_anat_r{0}.nii.gz'.format(i+1)
              
              ants_apply.run()

              varcopes1_2_anat.append(os.path.abspath('varcope1_2_anat_r{0}.nii.gz'.format(i+1)))

        merge = fsl.Merge()
        merge.inputs.dimension = 't'
        merge.inputs.in_files = varcopes1_2_anat
        merge.inputs.merged_file = 'varcopes1_2_anat.nii.gz'
        merge.run() 

        varcopes1_2_anat = os.path.abspath('varcopes1_2_anat.nii.gz')
      


        return varcopes1_2_anat


varcopes1_2_anat_func = Node(name = 'varcopes1_2_anat_func',
                          interface = Function(input_names = 
                                              ['fixed', 
                                               'varcope1_r1', 
                                               'varcope1_r2', 
                                               'varcope1_r3', 
                                               'varcope1_r4', 
                                               'func_2_anat_trans_r1', 
                                               'func_2_anat_trans_r2', 
                                               'func_2_anat_trans_r3', 
                                               'func_2_anat_trans_r4'],
                           output_names = ['varcopes1_2_anat'],
                           function = varcopes1_2_anat_func))

#==========================================================================================================================================================

#==========================================================================================================================================================
#Create desing
create_l2_design = Node(fsl.model.L2Model(), name='create_l2_design')
create_l2_design.inputs.num_copes = no_runs


#==========================================================================================================================================================
#perform higher level model fits

flameo_fit_copes1 = Node(fsl.model.FLAMEO(), name='flameo_fit_copes1')
flameo_fit_copes1.inputs.run_mode = 'fe'

#==========================================================================================================================================================
smooth_est_copes1 = Node(fsl.SmoothEstimate(), name = 'smooth_estimation_copes1')
smooth_est_copes1.inputs.dof = 3 #453-5 volumes 

#==========================================================================================================================================================
#mask zstat1

mask_zstat1 = Node(fsl.ApplyMask(), name='mask_zstat1')
mask_zstat1.inputs.out_file = 'thresh_zstat1.nii.gz'


#==========================================================================================================================================================
#cluster copes1
cluster_copes1 = Node(fsl.model.Cluster(), name='cluster_copes1')

cluster_copes1.inputs.threshold = 2.3
cluster_copes1.inputs.pthreshold = 0.05
cluster_copes1.inputs.connectivity = 26

cluster_copes1.inputs.out_threshold_file = 'thresh_zstat1.nii.gz'
cluster_copes1.inputs.out_index_file = 'cluster_mask_zstat1'
cluster_copes1.inputs.out_localmax_txt_file = 'lmax_zstat1_std.txt'
cluster_copes1.inputs.use_mm = True

#==========================================================================================================================================================
#overlay thresh_zstat1

overlay_cope1 = Node(fsl.Overlay(), name='overlay_cope1')
overlay_cope1.inputs.auto_thresh_bg = True
overlay_cope1.inputs.stat_thresh = (2.300302,14)
overlay_cope1.inputs.transparency = True
overlay_cope1.inputs.out_file = 'rendered_thresh_zstat1.nii.gz'
overlay_cope1.inputs.show_negative_stats = True

#==========================================================================================================================================================
#generate pics thresh_zstat1

slicer_cope1 = Node(fsl.Slicer(), name='slicer_cope1')
slicer_cope1.inputs.sample_axial = 2
slicer_cope1.inputs.image_width = 2000
slicer_cope1.inputs.out_file = 'rendered_thresh_zstat1.png'

#===========================================================================================================================================================
#trasnform copes from 2nd level to template space to be ready fro 3rd level

cope1_2ndlevel_2_template = Node(ants.ApplyTransforms(), name='cope1_2ndlevel_2_template')
cope1_2ndlevel_2_template.inputs.dimension = 3
cope1_2ndlevel_2_template.inputs.reference_image = study_template
cope1_2ndlevel_2_template.inputs.output_image = 'cope1_2ndlevel_2_study_template.nii.gz'



varcope1_2ndlevel_2_template = Node(ants.ApplyTransforms(), name='varcope1_2ndlevel_2_template')
varcope1_2ndlevel_2_template.inputs.dimension = 3
varcope1_2ndlevel_2_template.inputs.reference_image = study_template
varcope1_2ndlevel_2_template.inputs.output_image = 'varcope1_2ndlevel_2_study_template.nii.gz'




#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$     cope2    $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


def copes2_2_anat_func(fixed, cope2_r1, cope2_r2, cope2_r3, cope2_r4, func_2_anat_trans_r1, func_2_anat_trans_r2, func_2_anat_trans_r3, func_2_anat_trans_r4, mask_brain):
        import os, re
        import nipype.interfaces.ants as ants
        import nipype.interfaces.fsl as fsl

        cwd = os.getcwd()


        copes2 = [cope2_r1,cope2_r2,cope2_r3,cope2_r4]
        trans  = [func_2_anat_trans_r1, func_2_anat_trans_r2, func_2_anat_trans_r3, func_2_anat_trans_r4]

        copes2_2_anat = []
        FEtdof_t2_2_anat = []
        for i in range(len(copes2)):
              moving = copes2[i]
              transform = trans[i]
              ants_apply = ants.ApplyTransforms()
              ants_apply.inputs.dimension = 3
              ants_apply.inputs.input_image = moving
              ants_apply.inputs.reference_image = fixed
              ants_apply.inputs.transforms = transform
              ants_apply.inputs.output_image = 'cope2_2_anat_r{0}.nii.gz'.format(i+1)
              

              ants_apply.run()

              copes2_2_anat.append(os.path.abspath('cope2_2_anat_r{0}.nii.gz'.format(i+1)))

              dof = fsl.ImageMaths()
              dof.inputs.in_file = 'cope2_2_anat_r{0}.nii.gz'.format(i+1)
              dof.inputs.op_string = '-mul 0 -add 448 -mas'
              dof.inputs.in_file2 = mask_brain
              dof.inputs.out_file = 'FEtdof_t2_2_anat_r{0}.nii.gz'.format(i+1)

              dof.run()
              
              FEtdof_t2_2_anat.append(os.path.abspath('FEtdof_t2_2_anat_r{0}.nii.gz'.format(i+1)))


        merge = fsl.Merge()
        merge.inputs.dimension = 't'
        merge.inputs.in_files = copes2_2_anat
        merge.inputs.merged_file = 'copes2_2_anat.nii.gz'
        merge.run() 

        merge.inputs.in_files = FEtdof_t2_2_anat
        merge.inputs.merged_file = 'dofs_t2_2_anat.nii.gz'
        merge.run()

        copes2_2_anat = os.path.abspath('copes2_2_anat.nii.gz')
        dofs_t2_2_anat = os.path.abspath('dofs_t2_2_anat.nii.gz')
        
        return copes2_2_anat, dofs_t2_2_anat


copes2_2_anat_func = Node(name = 'copes2_2_anat_func',
                          interface = Function(input_names = 
                                              ['fixed', 
                                               'cope2_r1', 
                                               'cope2_r2', 
                                               'cope2_r3', 
                                               'cope2_r4', 
                                               'func_2_anat_trans_r1', 
                                               'func_2_anat_trans_r2', 
                                               'func_2_anat_trans_r3', 
                                               'func_2_anat_trans_r4',
                                               'mask_brain'],
                           output_names = ['copes2_2_anat', 'dofs_t2_2_anat'],
                           function = copes2_2_anat_func))


#==========================================================================================================================================================

def varcopes2_2_anat_func(fixed, varcope2_r1, varcope2_r2, varcope2_r3, varcope2_r4, func_2_anat_trans_r1, func_2_anat_trans_r2, func_2_anat_trans_r3, func_2_anat_trans_r4):
        import os, re
        import nipype.interfaces.ants as ants
        import nipype.interfaces.fsl as fsl

        cwd = os.getcwd()


        varcopes2 = [varcope2_r1,varcope2_r2,varcope2_r3,varcope2_r4]
        trans  = [func_2_anat_trans_r1, func_2_anat_trans_r2, func_2_anat_trans_r3, func_2_anat_trans_r4]

        varcopes2_2_anat = []

        for i in range(len(varcopes2)):
              moving = varcopes2[i]
              transform = trans[i]
              ants_apply = ants.ApplyTransforms()
              ants_apply.inputs.dimension = 3
              ants_apply.inputs.input_image = moving
              ants_apply.inputs.reference_image = fixed
              ants_apply.inputs.transforms = transform
              ants_apply.inputs.output_image = 'varcope2_2_anat_r{0}.nii.gz'.format(i+1)
              
              ants_apply.run()

              varcopes2_2_anat.append(os.path.abspath('varcope2_2_anat_r{0}.nii.gz'.format(i+1)))

        merge = fsl.Merge()
        merge.inputs.dimension = 't'
        merge.inputs.in_files = varcopes2_2_anat
        merge.inputs.merged_file = 'varcopes2_2_anat.nii.gz'
        merge.run() 

        varcopes2_2_anat = os.path.abspath('varcopes2_2_anat.nii.gz')
      


        return varcopes2_2_anat


varcopes2_2_anat_func = Node(name = 'varcopes2_2_anat_func',
                          interface = Function(input_names = 
                                              ['fixed', 
                                               'varcope2_r1', 
                                               'varcope2_r2', 
                                               'varcope2_r3', 
                                               'varcope2_r4', 
                                               'func_2_anat_trans_r1', 
                                               'func_2_anat_trans_r2', 
                                               'func_2_anat_trans_r3', 
                                               'func_2_anat_trans_r4'],
                           output_names = ['varcopes2_2_anat'],
                           function = varcopes2_2_anat_func))



#perform higher level model fits

flameo_fit_copes2 = Node(fsl.model.FLAMEO(), name='flameo_fit_copes2')
flameo_fit_copes2.inputs.run_mode = 'fe'

#==========================================================================================================================================================
smooth_est_copes2 = Node(fsl.SmoothEstimate(), name = 'smooth_estimation_copes2')
smooth_est_copes2.inputs.dof = 3 #453-5 volumes 

#==========================================================================================================================================================
#mask zstat2

mask_zstat2 = Node(fsl.ApplyMask(), name='mask_zstat2')
mask_zstat2.inputs.out_file = 'thresh_zstat2.nii.gz'


#==========================================================================================================================================================
#cluster copes2
cluster_copes2 = Node(fsl.model.Cluster(), name='cluster_copes2')

cluster_copes2.inputs.threshold = 2.3
cluster_copes2.inputs.pthreshold = 0.05
cluster_copes2.inputs.connectivity = 26

cluster_copes2.inputs.out_threshold_file = 'thresh_zstat2.nii.gz'
cluster_copes2.inputs.out_index_file = 'cluster_mask_zstat2'
cluster_copes2.inputs.out_localmax_txt_file = 'lmax_zstat2_std.txt'
cluster_copes2.inputs.use_mm = True

#==========================================================================================================================================================
#overlay thresh_zstat2

overlay_cope2 = Node(fsl.Overlay(), name='overlay_cope2')
overlay_cope2.inputs.auto_thresh_bg = True
overlay_cope2.inputs.stat_thresh = (2.300302,14)
overlay_cope2.inputs.transparency = True
overlay_cope2.inputs.out_file = 'rendered_thresh_zstat2.nii.gz'
overlay_cope2.inputs.show_negative_stats = True

#==========================================================================================================================================================
#generate pics thresh_zstat2

slicer_cope2 = Node(fsl.Slicer(), name='slicer_cope2')
slicer_cope2.inputs.sample_axial = 2
slicer_cope2.inputs.image_width = 2000
slicer_cope2.inputs.out_file = 'rendered_thresh_zstat2.png'


#===========================================================================================================================================================
#trasnform copes from 2nd level to template space to be ready fro 3rd level

cope2_2ndlevel_2_template = Node(ants.ApplyTransforms(), name='cope2_2ndlevel_2_template')
cope2_2ndlevel_2_template.inputs.dimension = 3
cope2_2ndlevel_2_template.inputs.reference_image = study_template
cope2_2ndlevel_2_template.inputs.output_image = 'cope2_2ndlevel_2_study_template.nii.gz'


varcope2_2ndlevel_2_template = Node(ants.ApplyTransforms(), name='varcope2_2ndlevel_2_template')
varcope2_2ndlevel_2_template.inputs.dimension = 3
varcope2_2ndlevel_2_template.inputs.reference_image = study_template
varcope2_2ndlevel_2_template.inputs.output_image = 'varcope2_2ndlevel_2_study_template.nii.gz'









#==========================================================================================================================================================


proc_2nd_level.connect([


              (infosource, selectfiles, [('subject_id','subject_id')]),


              (selectfiles, copes1_2_anat_func,[('anat_brain','fixed'),
                                                ('cope1_r1','cope1_r1'),
                                                ('cope1_r2','cope1_r2'),
                                                ('cope1_r3','cope1_r3'),
                                                ('cope1_r4','cope1_r4'),
                                                ('func_2_anat_trans_r1','func_2_anat_trans_r1'),
                                                ('func_2_anat_trans_r2','func_2_anat_trans_r2'),
                                                ('func_2_anat_trans_r3','func_2_anat_trans_r3'),
                                                ('func_2_anat_trans_r4','func_2_anat_trans_r4'),
                                                ('mask_brain','mask_brain')]),

              (selectfiles, varcopes1_2_anat_func,[('anat_brain','fixed'),
                                                ('varcope1_r1','varcope1_r1'),
                                                ('varcope1_r2','varcope1_r2'),
                                                ('varcope1_r3','varcope1_r3'),
                                                ('varcope1_r4','varcope1_r4'),
                                                ('func_2_anat_trans_r1','func_2_anat_trans_r1'),
                                                ('func_2_anat_trans_r2','func_2_anat_trans_r2'),
                                                ('func_2_anat_trans_r3','func_2_anat_trans_r3'),
                                                ('func_2_anat_trans_r4','func_2_anat_trans_r4')]),




              (create_l2_design,flameo_fit_copes1, [('design_mat','design_file'),
                                                    ('design_con','t_con_file'),
                                                    ('design_grp','cov_split_file')]),

              (copes1_2_anat_func, flameo_fit_copes1, [('copes1_2_anat','cope_file'),
                                                       ('dofs_t1_2_anat','dof_var_cope_file')]),

              (varcopes1_2_anat_func, flameo_fit_copes1, [('varcopes1_2_anat','var_cope_file')]),

              (selectfiles, flameo_fit_copes1, [('mask_brain','mask_file')]),

              (selectfiles, smooth_est_copes1, [('mask_brain','mask_file')]),
              (flameo_fit_copes1, smooth_est_copes1, [('res4d','residual_fit_file')]),

              (selectfiles, mask_zstat1, [('mask_brain','mask_file')]),
              (flameo_fit_copes1, mask_zstat1, [('zstats','in_file')]),


              (mask_zstat1, cluster_copes1, [('out_file','in_file')]),
              (smooth_est_copes1, cluster_copes1, [('volume','volume'),
                                                   ('dlh','dlh')]),

              (flameo_fit_copes1, cluster_copes1, [('copes','cope_file')]),

              (selectfiles, overlay_cope1, [('anat_brain','background_image')]),

              (cluster_copes1, overlay_cope1, [('threshold_file','stat_image')]),

              (overlay_cope1, slicer_cope1, [('out_file','in_file')]),

              (flameo_fit_copes1, cope1_2ndlevel_2_template, [('copes','input_image')]),
              (selectfiles, cope1_2ndlevel_2_template, [('func_2_template','transforms')]),

              (flameo_fit_copes1, varcope1_2ndlevel_2_template, [('var_copes','input_image')]),
              (selectfiles, varcope1_2ndlevel_2_template, [('func_2_template','transforms')]),




              (flameo_fit_copes1, datasink, [('copes','copes1'),
                                             ('var_copes', 'varcopes1')]),

              (slicer_cope1, datasink, [('out_file','cope1_activation_pic')]),

              (cope1_2ndlevel_2_template, datasink, [('output_image','cope1_2ndlevel_2_template')]),
              (varcope1_2ndlevel_2_template, datasink, [('output_image','varcope1_2ndlevel_2_template')]),


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$     cope2    $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

              (selectfiles, copes2_2_anat_func,[('anat_brain','fixed'),
                                                ('cope2_r1','cope2_r1'),
                                                ('cope2_r2','cope2_r2'),
                                                ('cope2_r3','cope2_r3'),
                                                ('cope2_r4','cope2_r4'),
                                                ('func_2_anat_trans_r1','func_2_anat_trans_r1'),
                                                ('func_2_anat_trans_r2','func_2_anat_trans_r2'),
                                                ('func_2_anat_trans_r3','func_2_anat_trans_r3'),
                                                ('func_2_anat_trans_r4','func_2_anat_trans_r4'),
                                                ('mask_brain','mask_brain')]),

              (selectfiles, varcopes2_2_anat_func,[('anat_brain','fixed'),
                                                ('varcope2_r1','varcope2_r1'),
                                                ('varcope2_r2','varcope2_r2'),
                                                ('varcope2_r3','varcope2_r3'),
                                                ('varcope2_r4','varcope2_r4'),
                                                ('func_2_anat_trans_r1','func_2_anat_trans_r1'),
                                                ('func_2_anat_trans_r2','func_2_anat_trans_r2'),
                                                ('func_2_anat_trans_r3','func_2_anat_trans_r3'),
                                                ('func_2_anat_trans_r4','func_2_anat_trans_r4')]),


              (create_l2_design,flameo_fit_copes2, [('design_mat','design_file'),
                                                    ('design_con','t_con_file'),
                                                    ('design_grp','cov_split_file')]),

              (copes2_2_anat_func, flameo_fit_copes2, [('copes2_2_anat','cope_file'),
                                                       ('dofs_t2_2_anat','dof_var_cope_file')]),

              (varcopes2_2_anat_func, flameo_fit_copes2, [('varcopes2_2_anat','var_cope_file')]),

              (selectfiles, flameo_fit_copes2, [('mask_brain','mask_file')]),

              (selectfiles, smooth_est_copes2, [('mask_brain','mask_file')]),
              (flameo_fit_copes2, smooth_est_copes2, [('res4d','residual_fit_file')]),

              (selectfiles, mask_zstat2, [('mask_brain','mask_file')]),
              (flameo_fit_copes2, mask_zstat2, [('zstats','in_file')]),


              (mask_zstat2, cluster_copes2, [('out_file','in_file')]),
              (smooth_est_copes2, cluster_copes2, [('volume','volume'),
                                                   ('dlh','dlh')]),

              (flameo_fit_copes2, cluster_copes2, [('copes','cope_file')]),

              (selectfiles, overlay_cope2, [('anat_brain','background_image')]),

              (cluster_copes2, overlay_cope2, [('threshold_file','stat_image')]),

              (overlay_cope2, slicer_cope2, [('out_file','in_file')]),


              (flameo_fit_copes2, cope2_2ndlevel_2_template, [('copes','input_image')]),
              (selectfiles, cope2_2ndlevel_2_template, [('func_2_template','transforms')]),

              (flameo_fit_copes2, varcope2_2ndlevel_2_template, [('var_copes','input_image')]),
              (selectfiles, varcope2_2ndlevel_2_template, [('func_2_template','transforms')]),



              (flameo_fit_copes2, datasink, [('copes','copes2'),
                                             ('var_copes', 'varcopes2')]),

              (slicer_cope2, datasink, [('out_file','cope2_activation_pic')]),



              (cope2_2ndlevel_2_template, datasink, [('output_image','cope2_2ndlevel_2_template')]),
              (varcope2_2ndlevel_2_template, datasink, [('output_image','varcope2_2ndlevel_2_template')]),








              ])

proc_2nd_level.write_graph(graph2use='colored', format='png', simple_form=True)

proc_2nd_level.run(plugin='SLURM',plugin_args={'dont_resubmit_completed_jobs': True, 'max_jobs':50})

#need number for l2model

