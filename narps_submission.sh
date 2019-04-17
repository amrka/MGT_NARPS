#!/bin/bash


mkdir -p /media/amr/Amr_4TB/NARPS/submission_2/{thresholded_zstat,unthresholded_zstat,copes,varcopes}

#Move thresholded maps
imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level_post_fitting/threshold_file/gain_zstat3/threshold_file_MNI.nii.gz \
/media/amr/Amr_4TB/NARPS/submission_2/thresholded_zstat/hypo1_thresh.nii.gz


imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level_post_fitting/threshold_file/gain_zstat4/threshold_file_MNI.nii.gz \
/media/amr/Amr_4TB/NARPS/submission_2/thresholded_zstat/hypo2_thresh.nii.gz


imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level_post_fitting/threshold_file/gain_zstat3/threshold_file_MNI.nii.gz \
/media/amr/Amr_4TB/NARPS/submission_2/thresholded_zstat/hypo3_thresh.nii.gz


imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level_post_fitting/threshold_file/gain_zstat4/threshold_file_MNI.nii.gz \
/media/amr/Amr_4TB/NARPS/submission_2/thresholded_zstat/hypo4_thresh.nii.gz


imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level_post_fitting/threshold_file/loss_zstat5/threshold_file_MNI.nii.gz \
/media/amr/Amr_4TB/NARPS/submission_2/thresholded_zstat/hypo5_thresh.nii.gz


imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level_post_fitting/threshold_file/loss_zstat6/threshold_file_MNI.nii.gz \
/media/amr/Amr_4TB/NARPS/submission_2/thresholded_zstat/hypo6_thresh.nii.gz


imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level_post_fitting/threshold_file/loss_zstat3/threshold_file_MNI.nii.gz \
/media/amr/Amr_4TB/NARPS/submission_2/thresholded_zstat/hypo7_thresh.nii.gz


imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level_post_fitting/threshold_file/loss_zstat4/threshold_file_MNI.nii.gz \
/media/amr/Amr_4TB/NARPS/submission_2/thresholded_zstat/hypo8_thresh.nii.gz


imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level_post_fitting/threshold_file/loss_zstat2/threshold_file_MNI.nii.gz \
/media/amr/Amr_4TB/NARPS/submission_2/thresholded_zstat/hypo9_thresh.nii.gz

#=====================================================================================================================================================================
#unthresholded maps
imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level_post_fitting/unthreshold_file/gain_zstat3/unthreshold_file_MNI.nii.gz \
/media/amr/Amr_4TB/NARPS/submission_2/unthresholded_zstat/hypo1_unthresh.nii.gz


imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level_post_fitting/unthreshold_file/gain_zstat4/unthreshold_file_MNI.nii.gz \
/media/amr/Amr_4TB/NARPS/submission_2/unthresholded_zstat/hypo2_unthresh.nii.gz


imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level_post_fitting/unthreshold_file/gain_zstat3/unthreshold_file_MNI.nii.gz \
/media/amr/Amr_4TB/NARPS/submission_2/unthresholded_zstat/hypo3_unthresh.nii.gz


imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level_post_fitting/unthreshold_file/gain_zstat4/unthreshold_file_MNI.nii.gz \
/media/amr/Amr_4TB/NARPS/submission_2/unthresholded_zstat/hypo4_unthresh.nii.gz


imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level_post_fitting/unthreshold_file/loss_zstat5/unthreshold_file_MNI.nii.gz \
/media/amr/Amr_4TB/NARPS/submission_2/unthresholded_zstat/hypo5_unthresh.nii.gz


imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level_post_fitting/unthreshold_file/loss_zstat6/unthreshold_file_MNI.nii.gz \
/media/amr/Amr_4TB/NARPS/submission_2/unthresholded_zstat/hypo6_unthresh.nii.gz


imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level_post_fitting/unthreshold_file/loss_zstat3/unthreshold_file_MNI.nii.gz \
/media/amr/Amr_4TB/NARPS/submission_2/unthresholded_zstat/hypo7_unthresh.nii.gz


imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level_post_fitting/unthreshold_file/loss_zstat4/unthreshold_file_MNI.nii.gz \
/media/amr/Amr_4TB/NARPS/submission_2/unthresholded_zstat/hypo8_unthresh.nii.gz


imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level_post_fitting/unthreshold_file/loss_zstat2/unthreshold_file_MNI.nii.gz \
/media/amr/Amr_4TB/NARPS/submission_2/unthresholded_zstat/hypo9_unthresh.nii.gz

#====================================================================================================================================================================
#copes
imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/gain_stat_flameo_neg/+/cope3.nii.gz \
/media/amr/Amr_4TB/NARPS/submission_2/copes/hypo1_cope.nii.gz

imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/gain_stat_flameo_neg/+/cope4.nii.gz \
/media/amr/Amr_4TB/NARPS/submission_2/copes/hypo2_cope.nii.gz

imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/gain_stat_flameo_neg/+/cope3.nii.gz \
/media/amr/Amr_4TB/NARPS/submission_2/copes/hypo3_cope.nii.gz

imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/gain_stat_flameo_neg/+/cope4.nii.gz \
/media/amr/Amr_4TB/NARPS/submission_2/copes/hypo4_cope.nii.gz

imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/loss_stat_flameo_neg/+/cope5.nii.gz \
/media/amr/Amr_4TB/NARPS/submission_2/copes/hypo5_cope.nii.gz

imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/loss_stat_flameo_neg/+/cope6.nii.gz \
/media/amr/Amr_4TB/NARPS/submission_2/copes/hypo6_cope.nii.gz

imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/loss_stat_flameo_neg/+/cope3.nii.gz \
/media/amr/Amr_4TB/NARPS/submission_2/copes/hypo7_cope.nii.gz

imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/loss_stat_flameo_neg/+/cope4.nii.gz \
/media/amr/Amr_4TB/NARPS/submission_2/copes/hypo8_cope.nii.gz

imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/loss_stat_flameo_neg/+/cope2.nii.gz \
/media/amr/Amr_4TB/NARPS/submission_2/copes/hypo9_cope.nii.gz

#====================================================================================================================================================================
#varcopes
imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/gain_stat_flameo_neg/+/varcope3.nii.gz \
/media/amr/Amr_4TB/NARPS/submission_2/varcopes/hypo1_varcope.nii.gz

imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/gain_stat_flameo_neg/+/varcope4.nii.gz \
/media/amr/Amr_4TB/NARPS/submission_2/varcopes/hypo2_varcope.nii.gz

imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/gain_stat_flameo_neg/+/varcope3.nii.gz \
/media/amr/Amr_4TB/NARPS/submission_2/varcopes/hypo3_varcope.nii.gz

imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/gain_stat_flameo_neg/+/varcope4.nii.gz \
/media/amr/Amr_4TB/NARPS/submission_2/varcopes/hypo4_varcope.nii.gz

imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/loss_stat_flameo_neg/+/varcope5.nii.gz \
/media/amr/Amr_4TB/NARPS/submission_2/varcopes/hypo5_varcope.nii.gz

imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/loss_stat_flameo_neg/+/varcope6.nii.gz \
/media/amr/Amr_4TB/NARPS/submission_2/varcopes/hypo6_varcope.nii.gz

imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/loss_stat_flameo_neg/+/varcope3.nii.gz \
/media/amr/Amr_4TB/NARPS/submission_2/varcopes/hypo7_varcope.nii.gz

imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/loss_stat_flameo_neg/+/varcope4.nii.gz \
/media/amr/Amr_4TB/NARPS/submission_2/varcopes/hypo8_varcope.nii.gz

imcp /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/loss_stat_flameo_neg/+/varcope2.nii.gz \
/media/amr/Amr_4TB/NARPS/submission_2/varcopes/hypo9_varcope.nii.gz


#======================================================================================================================================================================
#Transform to MNI space only copes and varcopes, the thresh and unthresh maps are taken care of courtesy of post_fitting_script



#Now move all previous images to MNI space
for img in /media/amr/Amr_4TB/NARPS/submission_2/*opes/*.nii.gz;do
	img_no_ext=`remove_ext $img`
	# animal_no=`echo ${img_no_ext:end-2}`

	antsApplyTransforms \
	-d 3 \
	-i $img \
	-r /usr/local/fsl/data/standard/MNI152_T1_1mm_brain.nii.gz \
	-o ${img_no_ext}_MNI.nii.gz \
	-t /Volumes/Amr_1TB/NARPS/narps_to_MNI_1mm_Composite.h5 

done



#delete copes and varcopes in template space to make uploading folders easier

rm /media/amr/Amr_4TB/NARPS/submission_2/*opes/*cope.nii.gz


#remove _MNI from the names to make things even easier

for img in /media/amr/Amr_4TB/NARPS/submission_2/*opes/*.nii.gz;do
	name_wo_MNI=`echo $img | sed 's/_MNI/''/g'`
	immv $img ${name_wo_MNI}

done



