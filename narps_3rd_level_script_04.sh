#!/bin/bash

# calc(){ awk "BEGIN { print "$*" }"; }

# move to parent directory
cd /media/amr/Amr_4TB/NARPS

#create an output for 3rd level
mkdir output_narps_proc_3rd_level
cd output_narps_proc_3rd_level

#create subfolders for the two groups
mkdir -p equal_indifference_group/{copes1,varcopes1,copes2,varcopes2} 

mkdir -p equal_range_group/{copes1,varcopes1,copes2,varcopes2}


#seperate the files from each group based on whether they are even or odd

for folder in /Volumes/Amr_1TB/NARPS/ds001205/sub-*;do

	no=`echo ${folder:end-3}`

	mod=`expr $no % 2`

	#mod 5%2=1 => odd, 4%2=0 => even 
	if [ $mod -eq 1 ];then
		
		cp /media/amr/Amr_4TB/NARPS/output_narps_proc_2nd_level/cope1_2ndlevel_2_template/sub-${no}/cope1_2ndlevel_2_study_template.nii.gz \
		/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/equal_indifference_group/copes1/cope1_sub-${no}.nii.gz

		cp /media/amr/Amr_4TB/NARPS/output_narps_proc_2nd_level/varcope1_2ndlevel_2_template/sub-${no}/varcope1_2ndlevel_2_study_template.nii.gz \
		/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/equal_indifference_group/varcopes1/varcope1_sub-${no}.nii.gz


		cp /media/amr/Amr_4TB/NARPS/output_narps_proc_2nd_level/cope2_2ndlevel_2_template/sub-${no}/cope2_2ndlevel_2_study_template.nii.gz \
		/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/equal_indifference_group/copes2/cope2_sub-${no}.nii.gz

		cp /media/amr/Amr_4TB/NARPS/output_narps_proc_2nd_level/varcope2_2ndlevel_2_template/sub-${no}/varcope2_2ndlevel_2_study_template.nii.gz \
		/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/equal_indifference_group/varcopes2/varcope2_sub-${no}.nii.gz

	elif [ $mod -eq 0 ];then		

		cp /media/amr/Amr_4TB/NARPS/output_narps_proc_2nd_level/cope1_2ndlevel_2_template/sub-${no}/cope1_2ndlevel_2_study_template.nii.gz \
		/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/equal_range_group/copes1/cope1_sub-${no}.nii.gz

		cp /media/amr/Amr_4TB/NARPS/output_narps_proc_2nd_level/varcope1_2ndlevel_2_template/sub-${no}/varcope1_2ndlevel_2_study_template.nii.gz \
		/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/equal_range_group/varcopes1/varcope1_sub-${no}.nii.gz


		cp /media/amr/Amr_4TB/NARPS/output_narps_proc_2nd_level/cope2_2ndlevel_2_template/sub-${no}/cope2_2ndlevel_2_study_template.nii.gz \
		/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/equal_range_group/copes2/cope2_sub-${no}.nii.gz

		cp /media/amr/Amr_4TB/NARPS/output_narps_proc_2nd_level/varcope2_2ndlevel_2_template/sub-${no}/varcope2_2ndlevel_2_study_template.nii.gz \
		/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/equal_range_group/varcopes2/varcope2_sub-${no}.nii.gz


		
	fi

done

# (Equal_indifference_group- participants with odd numbers, e.g. sub001, sub003, sub005, etc. 
#  Equal_range_group- participants with even numbers, e.g. sub002, sub004, sub006, etc.)


#==============================================================================================================================

#combine cope1&2 and varcope1&2 for equal indifference group
fslmerge -t /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/equal_indifference_group/equal_indifference_group_cope1.nii.gz \
/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/equal_indifference_group/copes1/cope1_sub-*



fslmerge -t /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/equal_indifference_group/equal_indifference_group_varcope1.nii.gz \
/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/equal_indifference_group/varcopes1/varcope1_sub-*


fslmerge -t /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/equal_indifference_group/equal_indifference_group_cope2.nii.gz \
/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/equal_indifference_group/copes2/cope2_sub-*



fslmerge -t /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/equal_indifference_group/equal_indifference_group_varcope2.nii.gz \
/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/equal_indifference_group/varcopes2/varcope2_sub-*


#==============================================================================================================================

#combine cope1&2 and varcope1&2 for equal range group
fslmerge -t /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/equal_range_group/equal_range_group_cope1.nii.gz \
/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/equal_range_group/copes1/cope1_sub-*



fslmerge -t /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/equal_range_group/equal_range_group_varcope1.nii.gz \
/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/equal_range_group/varcopes1/varcope1_sub-*


fslmerge -t /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/equal_range_group/equal_range_group_cope2.nii.gz \
/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/equal_range_group/copes2/cope2_sub-*



fslmerge -t /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/equal_range_group/equal_range_group_varcope2.nii.gz \
/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/equal_range_group/varcopes2/varcope2_sub-*


#=============================================================================================================================


#merge two groups for unpaired_ttest only for cope2
fslmerge -t /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/gain.nii.gz \
/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/equal_indifference_group/equal_indifference_group_cope1.nii.gz \
/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/equal_range_group/equal_range_group_cope1.nii.gz


fslmerge -t /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/gain_varcope.nii.gz \
/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/equal_indifference_group/equal_indifference_group_varcope1.nii.gz \
/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/equal_range_group/equal_range_group_varcope1.nii.gz



fslmerge -t /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/loss.nii.gz \
/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/equal_indifference_group/equal_indifference_group_cope2.nii.gz \
/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/equal_range_group/equal_range_group_cope2.nii.gz



fslmerge -t /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/loss_varcope.nii.gz \
/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/equal_indifference_group/equal_indifference_group_varcope2.nii.gz \
/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/equal_range_group/equal_range_group_varcope2.nii.gz



cd /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/

# mkdir gain_stat_randomise
# mkdir loss_stat_randomise



# randomise_parallel \
# -i /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/gain.nii.gz \
# -o /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/gain_stat_randomise/ \
# -m /Volumes/Amr_1TB/NARPS/narps_templateBrainExtractionMask.nii.gz  \
# -d /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/unpaired_ttest_108_subject.mat \
# -t /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/unpaired_ttest_108_subject.con \
# -e /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/unpaired_ttest_108_subject.grp \
# -n 10000 -T -c 3.1 --uncorrp -x --film



# randomise_parallel \
# -i /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/loss.nii.gz \
# -o /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/loss_stat_randomise/ \
# -m /Volumes/Amr_1TB/NARPS/narps_templateBrainExtractionMask.nii.gz  \
# -d /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/unpaired_ttest_108_subject.mat \
# -t /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/unpaired_ttest_108_subject.con \
# -e /media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/unpaired_ttest_108_subject.grp \
# -n 10000 -T -c 3.1 --uncorrp -x --film





mkdir gain_stat_flameo_neg
mkdir loss_stat_flameo_neg





flameo \
--cope=/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/gain.nii.gz \
--vc=/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/gain_varcope.nii.gz \
--mask=/Volumes/Amr_1TB/NARPS/narps_templateBrainExtractionMask.nii.gz \
--ld=/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/gain_stat_flameo_neg \
--dm=/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/unpaired_ttest_108_subject.mat \
--cs=/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/unpaired_ttest_108_subject.grp \
--tc=/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/unpaired_ttest_108_subject.con \
--runmode=flame1



flameo \
--cope=/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/loss.nii.gz \
--vc=/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/loss_varcope.nii.gz \
--mask=/Volumes/Amr_1TB/NARPS/narps_templateBrainExtractionMask.nii.gz \
--ld=/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/loss_stat_flameo_neg \
--dm=/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/unpaired_ttest_108_subject.mat \
--cs=/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/unpaired_ttest_108_subject.grp \
--tc=/media/amr/Amr_4TB/NARPS/output_narps_proc_3rd_level/unpaired_ttest_108_subject.con \
--runmode=flame1






#Transform to MNI space
#apply them later in the post_fitting script

antsRegistrationSyN.sh \
-m /Volumes/Amr_1TB_NARPS/narps_template_brain.nii.gz \
-f /usr/local/fsl/data/standard/MNI152_T1_1mm_brain.nii.gz \
-n 8 -o /Volumes/Amr_1TB_NARPS/narps_to_MNI_1mm_










