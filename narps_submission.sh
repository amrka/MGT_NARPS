#!/bin/bash

#Move thresholded maps
imcp /media/amr/Amr_4TB/NARPS/workingdir_narps_proc_3rd_level_post_fitting/proc_3rd_level/_contrasts_cope3_tasks_gain/cluster/thresh_zstat.nii.gz \
/media/amr/Amr_4TB/NARPS/submission/thresholded_zstat/hypo1_thresh.nii.gz

imcp /media/amr/Amr_4TB/NARPS/workingdir_narps_proc_3rd_level_post_fitting/proc_3rd_level/_contrasts_cope3_tasks_gain/cluster/thresh_zstat.nii.gz \
/media/amr/Amr_4TB/NARPS/submission/thresholded_zstat/hypo3_thresh.nii.gz

imcp /media/amr/Amr_4TB/NARPS/workingdir_narps_proc_3rd_level_post_fitting/proc_3rd_level/_contrasts_cope3_tasks_loss/cluster/thresh_zstat.nii.gz \
/media/amr/Amr_4TB/NARPS/submission/thresholded_zstat/hypo5_thresh.nii.gz

imcp /media/amr/Amr_4TB/NARPS/workingdir_narps_proc_3rd_level_post_fitting/proc_3rd_level/_contrasts_cope3_tasks_loss/cluster/thresh_zstat.nii.gz \
/media/amr/Amr_4TB/NARPS/submission/thresholded_zstat/hypo7_thresh.nii.gz





imcp /media/amr/Amr_4TB/NARPS/workingdir_narps_proc_3rd_level_post_fitting/proc_3rd_level/_contrasts_cope4_tasks_gain/cluster/thresh_zstat.nii.gz \
/media/amr/Amr_4TB/NARPS/submission/thresholded_zstat/hypo2_thresh.nii.gz

imcp /media/amr/Amr_4TB/NARPS/workingdir_narps_proc_3rd_level_post_fitting/proc_3rd_level/_contrasts_cope4_tasks_gain/cluster/thresh_zstat.nii.gz \
/media/amr/Amr_4TB/NARPS/submission/thresholded_zstat/hypo4_thresh.nii.gz

imcp /media/amr/Amr_4TB/NARPS/workingdir_narps_proc_3rd_level_post_fitting/proc_3rd_level/_contrasts_cope4_tasks_loss/cluster/thresh_zstat.nii.gz \
/media/amr/Amr_4TB/NARPS/submission/thresholded_zstat/hypo6_thresh.nii.gz

imcp /media/amr/Amr_4TB/NARPS/workingdir_narps_proc_3rd_level_post_fitting/proc_3rd_level/_contrasts_cope4_tasks_loss/cluster/thresh_zstat.nii.gz \
/media/amr/Amr_4TB/NARPS/submission/thresholded_zstat/hypo8_thresh.nii.gz

imcp /media/amr/Amr_4TB/NARPS/workingdir_narps_proc_3rd_level_post_fitting/proc_3rd_level/_contrasts_cope2_tasks_loss/cluster/thresh_zstat.nii.gz \
/media/amr/Amr_4TB/NARPS/submission/thresholded_zstat/hypo9_thresh.nii.gz

#=====================================================================================================================================================================
#unthresholded maps
imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/gain_stat_flameo/zstat3.nii.gz \
/media/amr/Amr_4TB/NARPS/submission/unthresholded_zstat/hypo1_unthresh.nii.gz

imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/gain_stat_flameo/zstat3.nii.gz \
/media/amr/Amr_4TB/NARPS/submission/unthresholded_zstat/hypo3_unthresh.nii.gz

imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/loss_stat_flameo/zstat3.nii.gz \
/media/amr/Amr_4TB/NARPS/submission/unthresholded_zstat/hypo5_unthresh.nii.gz

imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/loss_stat_flameo/zstat3.nii.gz \
/media/amr/Amr_4TB/NARPS/submission/unthresholded_zstat/hypo7_unthresh.nii.gz



imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/gain_stat_flameo/zstat4.nii.gz \
/media/amr/Amr_4TB/NARPS/submission/unthresholded_zstat/hypo2_unthresh.nii.gz

imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/gain_stat_flameo/zstat4.nii.gz \
/media/amr/Amr_4TB/NARPS/submission/unthresholded_zstat/hypo4_unthresh.nii.gz

imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/loss_stat_flameo/zstat4.nii.gz \
/media/amr/Amr_4TB/NARPS/submission/unthresholded_zstat/hypo6_unthresh.nii.gz

imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/loss_stat_flameo/zstat4.nii.gz \
/media/amr/Amr_4TB/NARPS/submission/unthresholded_zstat/hypo8_unthresh.nii.gz

imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/loss_stat_flameo/zstat2.nii.gz \
/media/amr/Amr_4TB/NARPS/submission/unthresholded_zstat/hypo9_unthresh.nii.gz

#====================================================================================================================================================================
#copes
imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/gain_stat_flameo/cope3.nii.gz \
/media/amr/Amr_4TB/NARPS/submission/copes/hypo1_cope.nii.gz

imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/gain_stat_flameo/cope3.nii.gz \
/media/amr/Amr_4TB/NARPS/submission/copes/hypo3_cope.nii.gz

imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/loss_stat_flameo/cope3.nii.gz \
/media/amr/Amr_4TB/NARPS/submission/copes/hypo5_cope.nii.gz

imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/loss_stat_flameo/cope3.nii.gz \
/media/amr/Amr_4TB/NARPS/submission/copes/hypo7_cope.nii.gz



imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/gain_stat_flameo/cope4.nii.gz \
/media/amr/Amr_4TB/NARPS/submission/copes/hypo2_cope.nii.gz

imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/gain_stat_flameo/cope4.nii.gz \
/media/amr/Amr_4TB/NARPS/submission/copes/hypo4_cope.nii.gz

imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/loss_stat_flameo/cope4.nii.gz \
/media/amr/Amr_4TB/NARPS/submission/copes/hypo6_cope.nii.gz

imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/loss_stat_flameo/cope4.nii.gz \
/media/amr/Amr_4TB/NARPS/submission/copes/hypo8_cope.nii.gz

imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/loss_stat_flameo/cope2.nii.gz \
/media/amr/Amr_4TB/NARPS/submission/copes/hypo9_cope.nii.gz

#====================================================================================================================================================================
#varcopes
imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/gain_stat_flameo/varcope3.nii.gz \
/media/amr/Amr_4TB/NARPS/submission/varcopes/hypo1_varcope.nii.gz

imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/gain_stat_flameo/varcope3.nii.gz \
/media/amr/Amr_4TB/NARPS/submission/varcopes/hypo3_varcope.nii.gz

imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/loss_stat_flameo/varcope3.nii.gz \
/media/amr/Amr_4TB/NARPS/submission/varcopes/hypo5_varcope.nii.gz

imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/loss_stat_flameo/varcope3.nii.gz \
/media/amr/Amr_4TB/NARPS/submission/varcopes/hypo7_varcope.nii.gz



imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/gain_stat_flameo/varcope4.nii.gz \
/media/amr/Amr_4TB/NARPS/submission/varcopes/hypo2_varcope.nii.gz

imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/gain_stat_flameo/varcope4.nii.gz \
/media/amr/Amr_4TB/NARPS/submission/varcopes/hypo4_varcope.nii.gz

imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/loss_stat_flameo/varcope4.nii.gz \
/media/amr/Amr_4TB/NARPS/submission/varcopes/hypo6_varcope.nii.gz

imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/loss_stat_flameo/varcope4.nii.gz \
/media/amr/Amr_4TB/NARPS/submission/varcopes/hypo8_varcope.nii.gz

imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/loss_stat_flameo/varcope2.nii.gz \
/media/amr/Amr_4TB/NARPS/submission/varcopes/hypo9_varcope.nii.gz


#======================================================================================================================================================================
#Transform to MNI space

antsRegistrationSyN.sh \
-m /Volumes/Amr_1TB_NARPS/narps_template_brain.nii.gz \
-f /usr/local/fsl/data/standard/MNI152_T1_1mm_brain.nii.gz \
-n 8 -o /Volumes/Amr_1TB_NARPS/narps_to_MNI_1mm_




#Now move all previous images to MNI space
for img in /media/amr/Amr_4TB/NARPS/submission/*/*.nii.gz;do
	img_no_ext=`remove_ext $img`
	# animal_no=`echo ${img_no_ext:end-2}`

	antsApplyTransforms \
	-d 3 \
	-i $img \
	-r /usr/local/fsl/data/standard/MNI152_T1_1mm_brain.nii.gz \
	-o ${img_no_ext}_MNI.nii.gz \
	-t /Volumes/Amr_1TB/NARPS/narps_to_MNI_1mm_Composite.h5 

done







