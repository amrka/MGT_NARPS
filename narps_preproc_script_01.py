# In[1]:

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

#========================================================================================================
# In[2]:

experiment_dir = '/media/amr/Amr_1TB/NARPS/' 

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

# subject_list = [ 'sub-005', 'sub-123', 'sub-098', 'sub-050']

# subject_list = [ 'sub-001']

session_list = ['run-01',
                'run-02',
                'run-03',
                'run-04',]
                

                
output_dir  = '/media/amr/Amr_4TB/NARPS/output_narps_preproc_preproc'
working_dir = '/media/amr/Amr_4TB/NARPS/workingdir_narps_preproc_preproc'


preproc = Workflow (name = 'preproc')
preproc.base_dir = opj(experiment_dir, working_dir)


#=====================================================================================================
# In[3]:
#to prevent nipype from iterating over the anat image with each func run, you need seperate
#nodes to select the files
#and this will solve the problem I have for almost 6 months
#but notice that in the sessions, you have to iterate also over subject_id to get the {subject_id} var



# Infosource - a function free node to iterate over the list of subject names
infosource_anat = Node(IdentityInterface(fields=['subject_id']),
                  name="infosource_anat")
infosource_anat.iterables = [('subject_id', subject_list)]



infosource_func = Node(IdentityInterface(fields=['subject_id','session_id']),
                  name="infosource_func")
infosource_func.iterables = [('subject_id', subject_list),
                             ('session_id', session_list)]


#========================================================================================================
# In[4]:
# sub-001_task-MGT_run-02_bold.nii.gz, sub-001_task-MGT_run-02_sbref.nii.gz

#anatomical images
templates_anat = {
             'anat'     : 'ds001205/{subject_id}/anat/{subject_id}_T1w.nii.gz'
             }

selectfiles_anat = Node(SelectFiles(templates_anat,
                   base_directory=experiment_dir),
                   name="selectfiles_anat")

#functional runs
templates_func = {      
             'func'     : 'ds001205/{subject_id}/func/{subject_id}_task-MGT_{session_id}_bold.nii.gz',
             'sbref'    : 'ds001205/{subject_id}/func/{subject_id}_task-MGT_{session_id}_sbref.nii.gz',
             }

selectfiles_func = Node(SelectFiles(templates_func,
                   base_directory=experiment_dir),
                   name="selectfiles_func")
#========================================================================================================
# In[5]:

datasink = Node(DataSink(), name = 'datasink')
datasink.inputs.container = output_dir
datasink.inputs.base_directory = experiment_dir

substitutions = [('_subject_id_', ''),('_session_id_', '')]

datasink.inputs.substitutions = substitutions

#========================================================================================================
# In[6]:

study_template = '/media/amr/Amr_1TB/NARPS/narps_template.nii.gz';
study_template_brain = '/media/amr/Amr_1TB/NARPS/narps_templateBrainExtractionBrain.nii.gz';
study_mask = '/media/amr/Amr_1TB/NARPS/narps_templateBrainExtractionMask.nii.gz';

TR = 1.0

#=======================================================================================================
# In[7]:

#Remove skull using antsBrainExtraction.sh, i am using the study-based template that I build and remove
#the skull manually using ITKsnap
brain_extraction_anat = Node(ants.BrainExtraction(), name='brain_extraction_anat')
brain_extraction_anat.inputs.dimension = 3
brain_extraction_anat.inputs.brain_template = study_template
brain_extraction_anat.inputs.brain_probability_mask = study_mask
brain_extraction_anat.inputs.num_threads = 4


#======================================================================================================
# In[8]:


#Remove skull of func using antsBrainExtraction.sh, i am using the study-based template that I build and remove
#the skull manually using ITKsnap
brain_extraction_sbref = Node(fsl.BET(), name='brain_extraction_sbref')
brain_extraction_sbref.inputs.frac = 0.5
brain_extraction_sbref.inputs.vertical_gradient = 0.0
brain_extraction_sbref.inputs.mask = True
brain_extraction_sbref.inputs.surfaces = True
#=======================================================================================================
# In[9]:

#use the mask generated from bet sbref to remove skull from bold
brain_extraction_bold = Node(fsl.ApplyMask(), name='brain_extraction_bold')

#========================================================================================================
# In[10]:

## normalizing the anatomical_bias_corrected image to the common anatomical template
## Here only we are calculating the paramters, we apply them later.

reg_T1_2_temp = Node(ants.Registration(), name = 'reg_T1_2_temp')
reg_T1_2_temp.inputs.args='--float'
reg_T1_2_temp.inputs.collapse_output_transforms=True
reg_T1_2_temp.inputs.fixed_image=study_template_brain
reg_T1_2_temp.inputs.initial_moving_transform_com=True
reg_T1_2_temp.inputs.num_threads=4
reg_T1_2_temp.inputs.output_inverse_warped_image=True
reg_T1_2_temp.inputs.output_warped_image=True
reg_T1_2_temp.inputs.sigma_units=['vox']*3
reg_T1_2_temp.inputs.transforms= ['Rigid', 'Affine', 'SyN']
reg_T1_2_temp.inputs.winsorize_lower_quantile=0.005
reg_T1_2_temp.inputs.winsorize_upper_quantile=0.995
reg_T1_2_temp.inputs.convergence_threshold=[1e-06]
reg_T1_2_temp.inputs.convergence_window_size=[10]
reg_T1_2_temp.inputs.metric=['MI', 'MI', 'CC']
reg_T1_2_temp.inputs.metric_weight=[1.0]*3
reg_T1_2_temp.inputs.number_of_iterations=[[1000, 500, 250, 100],
                                                 [1000, 500, 250, 100],
                                                 [100, 70, 50, 20]]
reg_T1_2_temp.inputs.radius_or_number_of_bins=[32, 32, 4]
reg_T1_2_temp.inputs.sampling_percentage=[0.25, 0.25, 1]
reg_T1_2_temp.inputs.sampling_strategy=['Regular',
                                              'Regular',
                                              'None']
reg_T1_2_temp.inputs.shrink_factors=[[8, 4, 2, 1]]*3
reg_T1_2_temp.inputs.smoothing_sigmas=[[3, 2, 1, 0]]*3
reg_T1_2_temp.inputs.transform_parameters=[(0.1,),
                                                 (0.1,),
                                                 (0.1, 3.0, 0.0)]
reg_T1_2_temp.inputs.use_histogram_matching=True
reg_T1_2_temp.inputs.write_composite_transform=True
reg_T1_2_temp.inputs.verbose=True
reg_T1_2_temp.inputs.output_warped_image=True
reg_T1_2_temp.inputs.float=True

#========================================================================================================
# In[11]:
#If you do it like this, the pipeline will coregister sbref of each session to all the anats of all subjs
# coreg = reg_T1_2_temp.clone(name = 'coreg')
# coreg.inputs.transforms=['Rigid']
# /media/amr/Amr_1TB/NARPS/workingdir_narps_preproc_preproc/preproc/_subject_id_sub-005/brain_extraction_anat/highres001_BrainExtractionBrain.nii.gz

def coreg(sbref_image):
  #take brain extracted anat as an input, but do not use it
  #only to force the pipeline to run brain extraction first
    import ants, os, re
    #the trick is to get the anat image without the solicit from the pipeline
    cwd = os.getcwd()
    subj_no = re.findall('\d+',cwd)[-1]

    img = '/media/amr/Amr_4TB/NARPS/workingdir_narps_preproc_preproc/preproc/_subject_id_sub-{0}/brain_extraction_anat/highres001_BrainExtractionBrain.nii.gz'.format(subj_no)


    fixed = ants.image_read(img)
    moving = ants.image_read(sbref_image)
    #you have to setup the outprefix, otherwise it will send the output to tmp folder 

    mytx = ants.registration(fixed=fixed , moving=moving, type_of_transform='Rigid', outprefix = 'sbref_2_anat_sub-{0}'.format(subj_no))

    mywarpedimage = ants.apply_transforms(fixed=fixed, moving=moving,
                                          transformlist=mytx['fwdtransforms'])

    ants.image_write(image=mywarpedimage, filename='sbref_2_anat_sub-{0}.nii.gz'.format(subj_no))

    composite_transform = os.path.abspath('sbref_2_anat_sub-{0}0GenericAffine.mat'.format(subj_no))

    warped_image = os.path.abspath('sbref_2_anat_sub-{0}.nii.gz'.format(subj_no))

    return composite_transform, warped_image #always you need return


coreg = Node(name = 'coreg',
                  interface = Function(input_names = ['sbref_image', 'anat_brain'],
                               output_names = ['composite_transform', 'warped_image'],
                  function = coreg))




#========================================================================================================
# In[12]:

# mcflirt -in ${folder} -out ${folder}_mcf  -refvol example_func -plots -mats  -report;

McFlirt = Node(fsl.MCFLIRT(), name = 'McFlirt')
McFlirt.inputs.save_plots = True
McFlirt.inputs.save_mats = True
McFlirt.inputs.save_rms = True

#========================================================================================================
# In[13]:

#Getting motion parameters from Mcflirt and plotting them

def Plot_Motion(motion_par, rms_files):

    import numpy as np
    import matplotlib
    import matplotlib.pyplot as plt
    matplotlib.use('Agg') 

    movement = np.loadtxt(motion_par)
    abs_disp = np.loadtxt(rms_files[0])
    rel_disp = np.loadtxt(rms_files[1])
    plt.figure(figsize=(8,10), dpi=300)

    plt.subplot(311)
    plt.title('Translations in mm')
    plt.plot(movement[:,:3])
    plt.legend(['x','y','z'])

    plt.subplot(312)
    plt.title('Rotations in radians')
    plt.plot(movement[:,3:])
    plt.legend(['x','y','z'])
    
    plt.subplot(313)
    plt.title('Displacement in mm')
    plt.plot(abs_disp)
    plt.plot(rel_disp)
    plt.legend(['abs', 'rel'])

    plt.savefig('Motion')


Plot_Motion = Node(name = 'Plot_Motion',
                  interface = Function(input_names = ['motion_par','rms_files'],
                  function = Plot_Motion))



#========================================================================================================
# In[14]:

# apply the trasnfromation to all the EPI volumes

func_2_template = Node(ants.ApplyTransforms(), name = 'func_2_template')
func_2_template.inputs.dimension = 3

func_2_template.inputs.input_image_type = 3
func_2_template.inputs.num_threads = 1
func_2_template.inputs.float = True


#========================================================================================================
# In[15]:

#Use nilearn smoothin, because, as you know, fsl does not support anisotropic smoothing
def nilearn_smoothing(image):
    import nilearn 
    from nilearn.image import smooth_img

    import numpy as np
    import os

    kernel = [4,4,4]



    smoothed_img = smooth_img(image, kernel)
    smoothed_img.to_filename('smoothed_all.nii.gz')

    smoothed_output = os.path.abspath('smoothed_all.nii.gz')
    return  smoothed_output



nilearn_smoothing = Node(name = 'nilearn_smoothing',
                  interface = Function(input_names = ['image'],
                               output_names = ['smoothed_output'],
                  function = nilearn_smoothing))


#========================================================================================================
# In[16]:

#Getting median intensity
Median_Intensity = Node(fsl.ImageStats(), name = 'Median_Intensity')
#Put -k before -p 50
Median_Intensity.inputs.op_string = '-k %s -p 50'

#Scale median intensity 
def Scale_Median_Intensity (median_intensity):
    scaling = 10000/median_intensity
    return scaling

Scale_Median_Intensity = Node(name = 'Scale_Median_Intensity',
                      interface = Function(input_names = ['median_intensity'],
                                           output_names = ['scaling'],
                                           function = Scale_Median_Intensity))
#========================================================================================================
# In[17]:

#Global Intensity Normalization by multiplying by the scaling value
#the grand-mean intensity normalisation factor ( to give a median brain intensity of 10000 )
#grand mean scaling
Intensity_Normalization = Node(fsl.BinaryMaths(), name = 'Intensity_Normalization')
Intensity_Normalization.inputs.operation = 'mul'

#========================================================================================================
# In[18]:

#   fslmaths ${folder}_mcf_2highres_intnorm -bptf 25 -1 -add tempMean ${folder}_mcf_2highres_tempfilt;
high_pass_filter = Node(fsl.TemporalFilter(), name = 'high_pass_filter')
high_pass_filter.inputs.highpass_sigma = 45.0
#========================================================================================================
# In[19]

#Get the mean image
Get_Mean_Image = Node(fsl.MeanImage(), name = 'Get_Mean_Image')
Get_Mean_Image.inputs.dimension = 'T'

#Add the mean image to the filtered image
Add_Mean_Image = Node(fsl.BinaryMaths(), name = 'Add_Mean_Image')
Add_Mean_Image.inputs.operation = 'add'



#========================================================================================================
# In[20]:

melodic = Node(fsl.MELODIC(), name = 'Melodic')
melodic.inputs.approach = 'concat'
melodic.inputs.no_bet = True
melodic.inputs.bg_threshold = 10.0
melodic.inputs.tr_sec = 2.00
melodic.inputs.mm_thresh = 0.5
melodic.inputs.out_all = True
melodic.inputs.report = True
melodic.iterables = ('dim', [15,20,25])


#========================================================================================================
# In[21]:


preproc.connect([


              (infosource_anat, selectfiles_anat,[('subject_id','subject_id')]),

              (infosource_func, selectfiles_func, [('subject_id','subject_id'),
                                                   ('session_id','session_id')]),

              (selectfiles_anat, brain_extraction_anat, [('anat','anatomical_image')]),

              (brain_extraction_anat, reg_T1_2_temp, [('BrainExtractionBrain','moving_image')]),


              (selectfiles_func, McFlirt, [('func','in_file'), 
                                           ('sbref','ref_file')]),

              (McFlirt, Plot_Motion, [('par_file','motion_par'),
                                      ('rms_files','rms_files')]),

              (selectfiles_func, brain_extraction_sbref, [('sbref','in_file')]),

              (brain_extraction_sbref, brain_extraction_bold, [('mask_file','mask_file')]),
              (selectfiles_func, brain_extraction_bold, [('func','in_file')]),


              # (brain_extraction_anat, coreg, [('BrainExtractionBrain','anat_brain')]),
              (brain_extraction_sbref, coreg, [('out_file','sbref_image')]),

              (brain_extraction_bold, nilearn_smoothing, [('out_file','image')]),


              (brain_extraction_bold, Median_Intensity, [('out_file','in_file')]),
              (brain_extraction_sbref, Median_Intensity, [('mask_file','mask_file')]),

              (Median_Intensity, Scale_Median_Intensity, [('out_stat','median_intensity')]),

              (Scale_Median_Intensity, Intensity_Normalization, [('scaling','operand_value')]),
              (nilearn_smoothing, Intensity_Normalization, [('smoothed_output','in_file')]),


              (Intensity_Normalization, Get_Mean_Image, [('out_file','in_file')]),
              (Intensity_Normalization, high_pass_filter, [('out_file','in_file')]),

              (high_pass_filter, Add_Mean_Image, [('out_file','in_file')]),
              (Get_Mean_Image, Add_Mean_Image, [('out_file','operand_file')]),

              #======================================datasink============================================
              (Add_Mean_Image, datasink, [('out_file','preproc_img')]),
              (brain_extraction_sbref, datasink, [('out_file','sbref_brain'),
                                                  ('mask_file','sbref_mask')]),
              (coreg, datasink, [('composite_transform','func_2_anat_trans')]),
              (brain_extraction_anat, datasink, [('BrainExtractionBrain','anat_brain'),
                                                 ('BrainExtractionMask', 'anat_mask')]),
              (reg_T1_2_temp, datasink, [('composite_transform','anat_2_temp_trans'),
                                         ('warped_image','anat_2_temp_image')]),

              ])

preproc.write_graph(graph2use='colored', format='png', simple_form=True)

preproc.run('MultiProc', plugin_args={'n_procs': 8})

