"""
Created on Wed Mar  9 22:39:41 2022

@author: Fauston
"""

import numpy as np
import nibabel as nib
import xlsxwriter
import time
import math

from tfe22540.atlas_modif_name import get_corr_atlas_list, get_atlas_list
from tfe22540.perso_path import perso_path_string, patient_number_list

# A better version of this code exist (see moyenne_ROI_v2.py) 

perso_path, excel_path, subjects_path, patients_path, plot_path, atlas_path = perso_path_string() 

patient_numbers = patient_number_list("string_nb") # Manon

# =============================================================================
# DTI
# =============================================================================
#----------------------------- PATIENTS FA ------------------------------------
FA_all = np.array(["FA_E1","FA_E2"])
for patient_nb in patient_numbers :
    paths = np.array([subjects_path + "sub" + patient_nb + "_E1/dMRI/microstructure/dti/sub" + patient_nb + "_E1_FA.nii.gz",
                      subjects_path + "sub" + patient_nb + "_E2/dMRI/microstructure/dti/sub" + patient_nb + "_E2_FA.nii.gz"])
    FA_all = np.append(FA_all,paths,axis=0)
FA_all = np.reshape(FA_all,((len(patient_numbers)+1),2))
FA_all = np.delete(FA_all, (0), axis=0)


#----------------------------- PATIENTS MD ------------------------------------
MD_all = np.array(["MD_E1", "MD_E2"])
for patient_nb in patient_numbers:
    paths = np.array([subjects_path + "sub" + patient_nb + "_E1/dMRI/microstructure/dti/sub" + patient_nb + "_E1_MD.nii.gz",
                      subjects_path + "sub" + patient_nb + "_E2/dMRI/microstructure/dti/sub" + patient_nb + "_E2_MD.nii.gz"])
    MD_all = np.append(MD_all, paths, axis=0)
MD_all = np.reshape(MD_all, ((len(patient_numbers)+1), 2))
MD_all = np.delete(MD_all, (0), axis=0)


#----------------------------- PATIENTS AD ------------------------------------
AD_all = np.array(["AD_E1", "AD_E2"])
for patient_nb in patient_numbers:
    paths = np.array([subjects_path + "sub" + patient_nb + "_E1/dMRI/microstructure/dti/sub" + patient_nb + "_E1_AD.nii.gz",
                      subjects_path + "sub" + patient_nb + "_E2/dMRI/microstructure/dti/sub" + patient_nb + "_E2_AD.nii.gz"])
    AD_all = np.append(AD_all, paths, axis=0)
AD_all = np.reshape(AD_all, ((len(patient_numbers)+1), 2))
AD_all = np.delete(AD_all, (0), axis=0)


#----------------------------- PATIENTS RD ------------------------------------
RD_all = np.array(["RD_E1", "RD_E2"])
for patient_nb in patient_numbers:
    paths = np.array([subjects_path + "sub" + patient_nb + "_E1/dMRI/microstructure/dti/sub" + patient_nb + "_E1_RD.nii.gz",
                      subjects_path + "sub" + patient_nb + "_E2/dMRI/microstructure/dti/sub" + patient_nb + "_E2_RD.nii.gz"])
    RD_all = np.append(RD_all, paths, axis=0)
RD_all = np.reshape(RD_all, ((len(patient_numbers)+1), 2))
RD_all = np.delete(RD_all, (0), axis=0)


DTI_metrics = [FA_all,MD_all,AD_all,RD_all]
DTI_names = ["FA","MD","AD","RD"]


# =============================================================================
# NODDI
# =============================================================================
#--------------------------------- FBUNDLE ------------------------------------
fbundle_all = np.array(["fbundle_E1","fbundle_E2"])
for patient_nb in patient_numbers :
    paths = np.array([subjects_path + "sub" + patient_nb + "_E1/dMRI/microstructure/noddi/sub" + patient_nb + "_E1_noddi_fbundle.nii.gz",
                      subjects_path + "sub" + patient_nb + "_E2/dMRI/microstructure/noddi/sub" + patient_nb + "_E2_noddi_fbundle.nii.gz"])
    fbundle_all = np.append(fbundle_all,paths,axis=0)
fbundle_all = np.reshape(fbundle_all,((len(patient_numbers)+1),2))
fbundle_all = np.delete(fbundle_all, (0), axis=0)


#--------------------------------- FEXTRA -------------------------------------
fextra_all = np.array(["fextra_E1","fextra_E2"])
for patient_nb in patient_numbers :
    paths = np.array([subjects_path + "sub" + patient_nb + "_E1/dMRI/microstructure/noddi/sub" + patient_nb + "_E1_noddi_fextra.nii.gz",
                      subjects_path + "sub" + patient_nb + "_E2/dMRI/microstructure/noddi/sub" + patient_nb + "_E2_noddi_fextra.nii.gz"])
    fextra_all = np.append(fextra_all,paths,axis=0)
fextra_all = np.reshape(fextra_all,((len(patient_numbers)+1),2))
fextra_all = np.delete(fextra_all, (0), axis=0)


#--------------------------------- FINTRA -------------------------------------
fintra_all = np.array(["fintra_E1","fintra_E2"])
for patient_nb in patient_numbers :
    paths = np.array([subjects_path + "sub" + patient_nb + "_E1/dMRI/microstructure/noddi/sub" + patient_nb + "_E1_noddi_fintra.nii.gz",
                      subjects_path + "sub" + patient_nb + "_E2/dMRI/microstructure/noddi/sub" + patient_nb + "_E2_noddi_fintra.nii.gz"])
    fintra_all = np.append(fintra_all,paths,axis=0)
fintra_all = np.reshape(fintra_all,((len(patient_numbers)+1),2))
fintra_all = np.delete(fintra_all, (0), axis=0)


#--------------------------------- FISO ---------------------------------------
fiso_all = np.array(["fiso_E1","fiso_E2"])
for patient_nb in patient_numbers :
    paths = np.array([subjects_path + "sub" + patient_nb + "_E1/dMRI/microstructure/noddi/sub" + patient_nb + "_E1_noddi_fiso.nii.gz",
                      subjects_path + "sub" + patient_nb + "_E2/dMRI/microstructure/noddi/sub" + patient_nb + "_E2_noddi_fiso.nii.gz"])
    fiso_all = np.append(fiso_all,paths,axis=0)
fiso_all = np.reshape(fiso_all,((len(patient_numbers)+1),2))
fiso_all = np.delete(fiso_all, (0), axis=0)


#--------------------------------- FICVF --------------------------------------
icvf_all = np.array(["icvf_E1","icvf_E2"])
for patient_nb in patient_numbers :
    paths = np.array([subjects_path + "sub" + patient_nb + "_E1/dMRI/microstructure/noddi/sub" + patient_nb + "_E1_noddi_icvf.nii.gz",
                      subjects_path + "sub" + patient_nb + "_E2/dMRI/microstructure/noddi/sub" + patient_nb + "_E2_noddi_icvf.nii.gz"])
    icvf_all = np.append(icvf_all,paths,axis=0)
icvf_all = np.reshape(icvf_all,((len(patient_numbers)+1),2))
icvf_all = np.delete(icvf_all, (0), axis=0)


#--------------------------------- ODI ----------------------------------------
odi_all = np.array(["odi_E1","odi_E2"])
for patient_nb in patient_numbers :
    paths = np.array([subjects_path + "sub" + patient_nb + "_E1/dMRI/microstructure/noddi/sub" + patient_nb + "_E1_noddi_odi.nii.gz",
                      subjects_path + "sub" + patient_nb + "_E2/dMRI/microstructure/noddi/sub" + patient_nb + "_E2_noddi_odi.nii.gz"])
    odi_all = np.append(odi_all,paths,axis=0)
odi_all = np.reshape(odi_all,((len(patient_numbers)+1),2))
odi_all = np.delete(odi_all, (0), axis=0)


NODDI_metrics = [fbundle_all,fextra_all,fintra_all,fiso_all,icvf_all,odi_all]
NODDI_names = ["noddi_fbundle","noddi_fextra","noddi_fintra","noddi_fiso","noddi_icvf","noddi_odi"]


# =============================================================================
# DIAMOND
# =============================================================================
#---------------------------------  FRAC_FTOT  --------------------------------
fractions_all2 = np.array(["fractions_E1","fractions_E2"])
for patient_nb in patient_numbers :
    paths = np.array([subjects_path + "sub" + patient_nb + "_E1/dMRI/microstructure/diamond/sub" + patient_nb + "_E1_diamond_fractions_ftot.nii.gz",
                      subjects_path + "sub" + patient_nb + "_E2/dMRI/microstructure/diamond/sub" + patient_nb + "_E2_diamond_fractions_ftot.nii.gz"])                      
    fractions_all2 = np.append(fractions_all2, paths, axis=0)
fractions_all2 = np.reshape(fractions_all2,((len(patient_numbers)+1),2))
fractions_all2 = np.delete(fractions_all2, (0), axis=0)


#---------------------------------  FRAC_CSF  ---------------------------------
fractions_all3 = np.array(["fractions_E1","fractions_E2"])
for patient_nb in patient_numbers :
    paths = np.array([subjects_path + "sub" + patient_nb + "_E1/dMRI/microstructure/diamond/sub" + patient_nb + "_E1_diamond_fractions_csf.nii.gz",
                      subjects_path + "sub" + patient_nb + "_E2/dMRI/microstructure/diamond/sub" + patient_nb + "_E2_diamond_fractions_csf.nii.gz"])                      
    fractions_all3 = np.append(fractions_all3, paths, axis=0)
fractions_all3 = np.reshape(fractions_all3,((len(patient_numbers)+1),2))
fractions_all3 = np.delete(fractions_all3, (0), axis=0)


DIAMOND_metrics = [fractions_all2, fractions_all3] 
DIAMOND_names = ["diamond_fractions_ftot", "diamond_fractions_csf"]


#----------------------------- PATIENTS wFA ------------------------------------
wFA_all = np.array(["wFA_E1","wFA_E2"])
for patient_nb in patient_numbers :
    paths = np.array([subjects_path + "sub" + patient_nb + "_E1/dMRI/microstructure/diamond/sub" + patient_nb + "_E1_wFA.nii.gz",
                      subjects_path + "sub" + patient_nb + "_E2/dMRI/microstructure/diamond/sub" + patient_nb + "_E2_wFA.nii.gz"])
    wFA_all = np.append(wFA_all,paths,axis=0)
wFA_all = np.reshape(wFA_all,((len(patient_numbers)+1),2))
wFA_all = np.delete(wFA_all, (0), axis=0)


#----------------------------- PATIENTS wMD ------------------------------------
wMD_all = np.array(["wMD_E1", "wMD_E2"])
for patient_nb in patient_numbers:
    paths = np.array([subjects_path + "sub" + patient_nb + "_E1/dMRI/microstructure/diamond/sub" + patient_nb + "_E1_wMD.nii.gz",
                      subjects_path + "sub" + patient_nb + "_E2/dMRI/microstructure/diamond/sub" + patient_nb + "_E2_wMD.nii.gz"])
    wMD_all = np.append(wMD_all, paths, axis=0)
wMD_all = np.reshape(wMD_all, ((len(patient_numbers)+1), 2))
wMD_all = np.delete(wMD_all, (0), axis=0)


#----------------------------- PATIENTS wAD ------------------------------------
wAD_all = np.array(["wAD_E1", "wAD_E2"])
for patient_nb in patient_numbers:
    paths = np.array([subjects_path + "sub" + patient_nb + "_E1/dMRI/microstructure/diamond/sub" + patient_nb + "_E1_wAD.nii.gz",
                      subjects_path + "sub" + patient_nb + "_E2/dMRI/microstructure/diamond/sub" + patient_nb + "_E2_wAD.nii.gz"])
    wAD_all = np.append(wAD_all, paths, axis=0)
wAD_all = np.reshape(wAD_all, ((len(patient_numbers)+1), 2))
wAD_all = np.delete(wAD_all, (0), axis=0)


#----------------------------- PATIENTS wRD ------------------------------------
wRD_all = np.array(["wRD_E1", "wRD_E2"])
for patient_nb in patient_numbers:
    paths = np.array([subjects_path + "sub" + patient_nb + "_E1/dMRI/microstructure/diamond/sub" + patient_nb + "_E1_wRD.nii.gz",
                      subjects_path + "sub" + patient_nb + "_E2/dMRI/microstructure/diamond/sub" + patient_nb + "_E2_wRD.nii.gz"])
    wRD_all = np.append(wRD_all, paths, axis=0)
wRD_all = np.reshape(wRD_all, ((len(patient_numbers)+1), 2))
wRD_all = np.delete(wRD_all, (0), axis=0)


cDIAMOND_metrics = [wFA_all,wMD_all,wAD_all,wRD_all]
cDIAMOND_names = ["wFA","wMD","wAD","wRD"]


# =============================================================================
# MF
# =============================================================================
#---------------------------------  FRAC_FTOT  --------------------------------
frac_ftot_all = np.array(["frac_f1_E1","frac_f1_E2"])
for patient_nb in patient_numbers :
    paths = np.array([subjects_path + "sub" + patient_nb + "_E1/dMRI/microstructure/mf/sub" + patient_nb + "_E1_mf_frac_ftot.nii.gz",
                      subjects_path + "sub" + patient_nb + "_E2/dMRI/microstructure/mf/sub" + patient_nb + "_E2_mf_frac_ftot.nii.gz"])
    frac_ftot_all = np.append(frac_ftot_all,paths,axis=0) 
frac_ftot_all = np.reshape(frac_ftot_all,((len(patient_numbers)+1),2))
frac_ftot_all = np.delete(frac_ftot_all, (0), axis=0)


#--------------------------------  FRAC_CSF  ----------------------------------
frac_csf_all = np.array(["frac_csf_E1","frac_csf_E2"])
for patient_nb in patient_numbers :
    paths = np.array([subjects_path + "sub" + patient_nb + "_E1/dMRI/microstructure/mf/sub" + patient_nb + "_E1_mf_frac_csf.nii.gz",
                      subjects_path + "sub" + patient_nb + "_E2/dMRI/microstructure/mf/sub" + patient_nb + "_E2_mf_frac_csf.nii.gz"])
    frac_csf_all = np.append(frac_csf_all,paths,axis=0) 
frac_csf_all = np.reshape(frac_csf_all,((len(patient_numbers)+1),2))
frac_csf_all = np.delete(frac_csf_all, (0), axis=0)


#----------------------------------  WFVF  ------------------------------------
wfvf_all = np.array(["fvf_f1_E1","fvf_f1_E2"])
for patient_nb in patient_numbers :                     
    paths = np.array([subjects_path + "sub" + patient_nb + "_E1/dMRI/microstructure/mf/sub" + patient_nb + "_E1_mf_wfvf.nii.gz",
                      subjects_path + "sub" + patient_nb + "_E2/dMRI/microstructure/mf/sub" + patient_nb + "_E2_mf_wfvf.nii.gz"])
    wfvf_all = np.append(wfvf_all,paths,axis=0) 
wfvf_all = np.reshape(wfvf_all,((len(patient_numbers)+1),2))
wfvf_all = np.delete(wfvf_all, (0), axis=0)


#---------------------------------  FVF_TOT  ----------------------------------
fvf_tot_all = np.array(["fvf_tot_E1","fvf_tot_E2"])
for patient_nb in patient_numbers :
    paths = np.array([subjects_path + "sub" + patient_nb + "_E1/dMRI/microstructure/mf/sub" + patient_nb + "_E1_mf_fvf_tot.nii.gz",
                      subjects_path + "sub" + patient_nb + "_E2/dMRI/microstructure/mf/sub" + patient_nb + "_E2_mf_fvf_tot.nii.gz"])
    fvf_tot_all = np.append(fvf_tot_all,paths,axis=0) 
fvf_tot_all = np.reshape(fvf_tot_all,((len(patient_numbers)+1),2))
fvf_tot_all = np.delete(fvf_tot_all, (0), axis=0)


MF_metrics = [frac_csf_all,frac_ftot_all,wfvf_all,fvf_tot_all]
MF_names = ["mf_frac_csf","mf_frac_ftot","mf_wfvf","mf_fvf_tot"]


# =============================================================================
# MASK
# =============================================================================
#---------------------------------  BRAIN  ------------------------------------
brain_mask_all = np.array(["brain_mask_E1", "brain_mask_E2"])
for patient_nb in patient_numbers:
    paths = np.array([subjects_path + "sub" + patient_nb + "_E1/masks/sub" + patient_nb + "_E1_brain_mask.nii.gz",
                      subjects_path + "sub" + patient_nb + "_E2/masks/sub" + patient_nb + "_E2_brain_mask.nii.gz"])
    brain_mask_all = np.append(brain_mask_all, paths, axis=0)
brain_mask_all = np.reshape(brain_mask_all, ((len(patient_numbers)+1), 2))
brain_mask_all = np.delete(brain_mask_all, (0), axis=0)


#---------------------------------  WHITE  ------------------------------------
wm_mask_all = np.array(["wm_mask_E1", "wm_mask_E2"])
for patient_nb in patient_numbers:
    paths = np.array([subjects_path + "sub" + patient_nb + "_E1/masks/sub" + patient_nb + "_E1_wm_mask_FSL_T1.nii.gz",
                      subjects_path + "sub" + patient_nb + "_E2/masks/sub" + patient_nb + "_E2_wm_mask_FSL_T1.nii.gz"])
    wm_mask_all = np.append(wm_mask_all, paths, axis=0)
wm_mask_all = np.reshape(wm_mask_all, ((len(patient_numbers)+1), 2))
wm_mask_all = np.delete(wm_mask_all, (0), axis=0)


metric_list = []
metric_name = []
for i in range(4):
    metric_list.append(DTI_metrics[i])
    metric_name.append(DTI_names[i])
for i in range(6):
    metric_list.append(NODDI_metrics[i])
    metric_name.append(NODDI_names[i])
for i in range(2):
    metric_list.append(DIAMOND_metrics[i])
    metric_name.append(DIAMOND_names[i])
for i in range(4):
    metric_list.append(cDIAMOND_metrics[i])
    metric_name.append(cDIAMOND_names[i])
for i in range(4): 
    metric_list.append(MF_metrics[i])
    metric_name.append(MF_names[i])

# =============================================================================
# MOYENNE PAR ZONE
# =============================================================================
def moyenne_par_roi(folder_path, patient_path):
    
    """
        Parameters
        ----------
        folder_path : String 
            Link of the file in which we are. 
        patient_path : List of strings
            Number of all patients in string ["sub#_E1"] for example.
    
        Returns
        -------
        None. But creation of Excel files for each metric of each model.
    """
    
    analyse_path = excel_path
    
    start_time = time.time()
    
    # DTI
    if (patient_path == "sub02_E1"):
        patient_all = metric_list[0]
        metric = metric_name[0]
        bool_metric = False
    if (patient_path == "sub04_E1"):
        patient_all = metric_list[1]
        metric = metric_name[1]
        bool_metric = False
    if (patient_path == "sub05_E1"):
        patient_all = metric_list[2]
        metric = metric_name[2]
        bool_metric = False
    if (patient_path == "sub08_E1"):
        patient_all = metric_list[3]
        metric = metric_name[3]
        bool_metric = False
    # NODDI
    if (patient_path == "sub09_E1"):
        patient_all = metric_list[4]
        metric = metric_name[4]
        bool_metric = True
    if (patient_path == "sub11_E1"):
        patient_all = metric_list[5]
        metric = metric_name[5]
        bool_metric = True
    if (patient_path == "sub12_E1"):
        patient_all = metric_list[6]
        metric = metric_name[6]
        bool_metric = True
    if (patient_path == "sub13_E1"):
        patient_all = metric_list[7]
        metric = metric_name[7]
        bool_metric = True
    if (patient_path == "sub14_E1"):
        patient_all = metric_list[8]
        metric = metric_name[8]
        bool_metric = True
    if (patient_path == "sub15_E1"):
        patient_all = metric_list[9]
        metric = metric_name[9]
        bool_metric = True
    # DIAMOND
    if (patient_path == "sub17_E1"):
        patient_all = metric_list[10]
        metric = metric_name[10]
        bool_metric = True
    if (patient_path == "sub19_E1"):
        patient_all = metric_list[11]
        metric = metric_name[11]
        bool_metric = True
    if (patient_path == "sub20_E1"):
        patient_all = metric_list[12]
        metric = metric_name[12]
        bool_metric = True
    if (patient_path == "sub21_E1"):
        patient_all = metric_list[13]
        metric = metric_name[13]
        bool_metric = True
    if (patient_path == "sub22_E1"):
        patient_all = metric_list[14]
        metric = metric_name[14]
        bool_metric = True
    if (patient_path == "sub24_E1"):
        patient_all = metric_list[15]
        metric = metric_name[15]
        bool_metric = True
    # MF
    if (patient_path == "sub26_E1"):
        patient_all = metric_list[16]
        metric = metric_name[16]
        bool_metric = True
    if (patient_path == "sub27_E1"):
        patient_all = metric_list[17]
        metric = metric_name[17]
        bool_metric = True
    if (patient_path == "sub28_E1"):
        patient_all = metric_list[18]
        metric = metric_name[18]
        bool_metric = True
    if (patient_path == "sub30_E1"):
        patient_all = metric_list[19]
        metric = metric_name[19]
        bool_metric = True
    
    atlas_list = get_atlas_list(onlywhite = bool_metric) 
    atlas_list_name = get_corr_atlas_list(atlas_list) 
    workbook = xlsxwriter.Workbook(analyse_path + 'Mean_ROI_' + metric + '.xlsx')
    
    for patient, brain_mask, wm_mask, patient_nb in zip(patient_all, brain_mask_all, wm_mask_all, patient_numbers):
        
        img = nib.load(patient[0])
        img1 = nib.load(patient[1])
        
        worksheet = workbook.add_worksheet(patient_nb)
    
        azer = 2
    
        path_atlas_reg = patients_path + "#" + patient_nb 
        
        brain_mask_E1 = nib.load(brain_mask[0]).get_fdata()
        brain_mask_E1[:,:,0] = 0
        brain_mask_E1[:,:,-1] = 0
        brain_mask_E2 = nib.load(brain_mask[1]).get_fdata()
        brain_mask_E2[:,:,0] = 0
        brain_mask_E2[:,:,-1] = 0
        
        wm_mask_E1 = nib.load(wm_mask[0]).get_fdata()
        wm_mask_E1[:,:,0] = 0
        wm_mask_E1[:,:,-1] = 0
        wm_mask_E2 = nib.load(wm_mask[1]).get_fdata()
        wm_mask_E2[:,:,0] = 0
        wm_mask_E2[:,:,-1] = 0
    
        for atlas_path in atlas_list_name:
            atlas_name = str(atlas_path[1])
            if ('.nii.gz' in atlas_name):
                atlas_name = atlas_name.replace('.nii.gz','')

            atlas_file_E1 = nib.load(path_atlas_reg + "/Atlas/" + atlas_name + "_reg_on_sub" + patient_nb + "_E1.nii.gz").get_fdata()
            atlas_file_E2 = nib.load(path_atlas_reg + "/Atlas/" + atlas_name + "_reg_on_sub" + patient_nb + "_E2.nii.gz").get_fdata()
            
            patient_file_E1 = nib.load(patient[0]).get_fdata()
            patient_file_E1[np.isnan(patient_file_E1) == True] = 0.0
            
            patient_file_E2 = nib.load(patient[1]).get_fdata()
            patient_file_E2[np.isnan(patient_file_E2) == True] = 0.0

            mask_zone_E1 = np.zeros(patient_file_E1.shape)
            mask_zone_E2 = np.zeros(patient_file_E2.shape)
            
            mask_zone_E1[atlas_file_E1 > float(atlas_path[2])] = 1
            mask_zone_E2[atlas_file_E2 > float(atlas_path[2])] = 1
            
            if(atlas_path[3] == "0" or atlas_path[3] == "2" or atlas_path[3] == "4" or atlas_path[3] == "5" or atlas_path[3] == "6"):
                mask_zone_E1 = mask_zone_E1 * brain_mask_E1
                mask_zone_E2 = mask_zone_E2 * brain_mask_E2
                
            elif(atlas_path[3] == "1" or atlas_path[3] == "3"): #WHITE MATTER
                mask_zone_E1 = mask_zone_E1 * wm_mask_E1
                mask_zone_E2 = mask_zone_E2 * wm_mask_E2

            else:
                print('Not ok again')

            mask_zone_E1[patient_file_E1 == 0] = 0
            mask_zone_E2[patient_file_E2 == 0] = 0
        
            interm_E1 = patient_file_E1*mask_zone_E1
            moyenne_E1 = np.mean(interm_E1[interm_E1 != 0])
            
            interm_E2 = patient_file_E2*mask_zone_E2
            moyenne_E2 = np.mean(interm_E2[interm_E2 != 0])
            
            percentage_change = (moyenne_E2 - moyenne_E1)*100/moyenne_E1
        
            if (math.isnan(moyenne_E1) == True or math.isnan(moyenne_E2) == True):
                moyenne_E1 = 0
                moyenne_E2 = 0

            if(np.isnan(percentage_change) == True):
                percentage_change = 0
   
            worksheet.write('A1', "Atlas names")
            worksheet.write('B1', "Mean at E1")
            worksheet.write('C1', "Mean at E2")
            worksheet.write('D1', "Percentage change bewteen E2 and E1")
            worksheet.write('A' + str(azer), atlas_path[0])
            worksheet.write('B' + str(azer), moyenne_E1)
            worksheet.write('C' + str(azer), moyenne_E2)
            worksheet.write('D' + str(azer), percentage_change)
    
            azer += 1
            
            #A RUN POUR SEULEMENT UNE METRIQUE
            # atlas_name1 = str(atlas_path[1])
            # if ('.nii.gz' in atlas_name1):
            #     atlas_name1 = atlas_name1.replace('.nii.gz', '')
            # if("Cerebellar/" in atlas_name1):
            #     atlas_name1 = atlas_name1.replace('Cerebellar/', '')
            # if("Cerebelar" in atlas_name1):
            #     atlas_name1 = atlas_name1.replace('Cerebelar', 'Cerebellar')
            # if("Cerebellum/" in atlas_name1):
            #     atlas_name1 = atlas_name1.replace('Cerebellum/', '')
            # if("Harvard/" in atlas_name1):
            #     atlas_name1 = atlas_name1.replace('Harvard/', '')
            # if("Harvard_cortex/" in atlas_name1):
            #     atlas_name1 = atlas_name1.replace('Harvard_cortex/', '')
            # if("Lobes/" in atlas_name1):
            #     atlas_name1 = atlas_name1.replace('Lobes/', '')
            # if("XTRACT/" in atlas_name1):
            #     atlas_name1 = atlas_name1.replace('XTRACT/', '')
            # if("CC/" in atlas_name1): 
            #     atlas_name1 = atlas_name1.replace('CC/', '')
                
            # out = nib.Nifti1Image(mask_zone_E1, affine = img.affine, header = img.header)
            # out.to_filename(path_atlas_reg + "/Mask/" + "sub" + patient_nb + "_" + atlas_name1 + "_mask_E1.nii.gz")

            # out1 = nib.Nifti1Image(mask_zone_E2, affine = img1.affine, header = img1.header)
            # out1.to_filename(path_atlas_reg + "/Mask/" + "sub" + patient_nb + "_" + atlas_name1 + "_mask_E2.nii.gz")
    
    workbook.close()
    print("Temps:", time.time() - start_time)

if __name__ == '__main__':
    list_to_do = ["11"]#,"04","05","08","09","11","12","13","14","15","17","18","19","20","21","22","24","26","27","28","30"]
        
    for i in list_to_do:
        moyenne_par_roi("", "sub" + i + "_E1")