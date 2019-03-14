#Build a study-based template using anatomical images
buildtemplateparallel.sh \
-d 3 \
-o narps_template \
-c 1 \
-j 50 \
-r 1 \
/home/in/aeed/NARPS/ds001205/sub-*/anat/*


#Remove the skull from the study_based_template
antsBrainExtraction.sh \
-d 3 \
-a sub-035_T1w.nii.gz \
-e /usr/local/fsl/data/standard/MNI152_T1_1mm.nii.gz  \
-m /usr/local/fsl/data/standard/MNI152_T1_2mm_brain_mask.nii.gz  \
-o narps_template
