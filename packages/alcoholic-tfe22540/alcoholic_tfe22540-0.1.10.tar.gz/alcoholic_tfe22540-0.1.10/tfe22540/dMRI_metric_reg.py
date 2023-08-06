"""
Created on Fri Mar  4 09:40:49 2022

@author: Fauston
"""

import numpy as np

from tfe22540.CN2 import getTransform, applyTransform
from tfe22540.perso_path import perso_path_string, patient_number_list


perso_path, excel_path, subjects_path, patients_path, plot_path, atlas_path = perso_path_string() 

patient_numbers = patient_number_list("string_nb")


# =============================================================================
# PATIENTS FA
# =============================================================================
FA_all = np.array(["FA_E1","FA_E2"])
for patient_nb in patient_numbers :
    paths = np.array([subjects_path + "sub" + patient_nb + "_E1/dMRI/microstructure/dti/sub" + patient_nb + "_E1_FA.nii.gz",
                      subjects_path + "sub" + patient_nb + "_E2/dMRI/microstructure/dti/sub" + patient_nb + "_E2_FA.nii.gz"])
    FA_all = np.append(FA_all,paths,axis=0)
FA_all = np.reshape(FA_all,((len(patient_numbers)+1),2))
FA_all = np.delete(FA_all, (0), axis=0)


# =============================================================================
# PATIENTS MD
# =============================================================================
MD_all = np.array(["MD_E1", "MD_E2"])
for patient_nb in patient_numbers:
    paths = np.array([subjects_path + "sub" + patient_nb + "_E1/dMRI/microstructure/dti/sub" + patient_nb + "_E1_MD.nii.gz",
                      subjects_path + "sub" + patient_nb + "_E2/dMRI/microstructure/dti/sub" + patient_nb + "_E2_MD.nii.gz"])
    MD_all = np.append(MD_all, paths, axis=0)
MD_all = np.reshape(MD_all, ((len(patient_numbers)+1), 2))
MD_all = np.delete(MD_all, (0), axis=0)


# =============================================================================
# PATIENTS AD
# =============================================================================
AD_all = np.array(["AD_E1", "AD_E2"])
for patient_nb in patient_numbers:
    paths = np.array([subjects_path + "sub" + patient_nb + "_E1/dMRI/microstructure/dti/sub" + patient_nb + "_E1_AD.nii.gz",
                      subjects_path + "sub" + patient_nb + "_E2/dMRI/microstructure/dti/sub" + patient_nb + "_E2_AD.nii.gz"])
    AD_all = np.append(AD_all, paths, axis=0)
AD_all = np.reshape(AD_all, ((len(patient_numbers)+1), 2))
AD_all = np.delete(AD_all, (0), axis=0)


# =============================================================================
# PATIENTS RD
# =============================================================================
RD_all = np.array(["RD_E1", "RD_E2",])
for patient_nb in patient_numbers:
    paths = np.array([subjects_path + "sub" + patient_nb + "_E1/dMRI/microstructure/dti/sub" + patient_nb + "_E1_RD.nii.gz",
                      subjects_path + "sub" + patient_nb + "_E2/dMRI/microstructure/dti/sub" + patient_nb + "_E2_RD.nii.gz"])
    RD_all = np.append(RD_all, paths, axis=0)
RD_all = np.reshape(RD_all, ((len(patient_numbers)+1), 2))
RD_all = np.delete(RD_all, (0), axis=0)


# =============================================================================
# METRIC REGISTRATION 
# =============================================================================
def register_metric(metric_all, metric_name):
    
    """
    Parameters
    ----------
    metric_all : List of file path of the metric of one patient at E1 and E2.
    metric_name : List of string
        Containing all the metrics of DTI.

    Returns
    -------
    None. Save a .nii.gz file of the registered metric
    """
    
    to_register = patient_numbers
    
    for Patient,patient_nb in zip(metric_all,to_register):
        transform1 = getTransform(Patient[0], Patient[1], onlyAffine = False, diffeomorph = True, sanity_check = False)
        applyTransform(Patient[1], transform1, 
                       Patient[0], patients_path + "#" + patient_nb + "/Registration/microstructure/dti/sub" + patient_nb + "_" + metric_name + "_E2_reg_on_E1.nii.gz",
                       binary = False)  

metric_name = ["FA","AD","RD","MD"]
register_metric(FA_all,metric_name[0])
register_metric(AD_all,metric_name[1])
register_metric(RD_all,metric_name[2])
register_metric(MD_all,metric_name[3])


# =============================================================================
# PATIENTS FA - wFA
# =============================================================================
wFA_all = np.array(["wFA_E1", "wFA_E2"])
for patient_nb in patient_numbers :
    paths = np.array([subjects_path + "sub" + patient_nb + "_E1/dMRI/microstructure/diamond/sub" + patient_nb + "_E1_wFA.nii.gz",
                      subjects_path + "sub" + patient_nb + "_E2/dMRI/microstructure/diamond/sub" + patient_nb + "_E2_wFA.nii.gz"])
    wFA_all = np.append(wFA_all,paths, axis = 0)
wFA_all = np.reshape(wFA_all, ((len(patient_numbers)+1), 2))
wFA_all = np.delete(wFA_all, (0), axis = 0)


# =============================================================================
# PATIENTS MD - wMD
# =============================================================================
wMD_all = np.array(["wMD_E1", "wMD_E2"])
for patient_nb in patient_numbers :
    paths = np.array([subjects_path + "sub" + patient_nb + "_E1/dMRI/microstructure/diamond/sub" + patient_nb + "_E1_wMD.nii.gz",
                      subjects_path + "sub" + patient_nb + "_E2/dMRI/microstructure/diamond/sub" + patient_nb + "_E2_wMD.nii.gz"])
    wMD_all = np.append(wMD_all,paths, axis = 0)
wMD_all = np.reshape(wMD_all, ((len(patient_numbers)+1), 2))
wMD_all = np.delete(wMD_all, (0), axis = 0)


# =============================================================================
# PATIENTS AD - wAD
# =============================================================================
wAD_all = np.array(["wAD_E1", "wAD_E2"])
for patient_nb in patient_numbers :
    paths = np.array([subjects_path + "sub" + patient_nb + "_E1/dMRI/microstructure/diamond/sub" + patient_nb + "_E1_wAD.nii.gz",
                      subjects_path + "sub" + patient_nb + "_E2/dMRI/microstructure/diamond/sub" + patient_nb + "_E2_wAD.nii.gz"])
    wAD_all = np.append(wAD_all,paths, axis = 0)
wAD_all = np.reshape(wAD_all, ((len(patient_numbers)+1), 2))
wAD_all = np.delete(wAD_all, (0), axis = 0)


# =============================================================================
# PATIENTS RD - wRD
# =============================================================================
wRD_all = np.array(["wRD_E1", "wRD_E2"])
for patient_nb in patient_numbers :
    paths = np.array([subjects_path + "sub" + patient_nb + "_E1/dMRI/microstructure/diamond/sub" + patient_nb + "_E1_wRD.nii.gz",
                      subjects_path + "sub" + patient_nb + "_E2/dMRI/microstructure/diamond/sub" + patient_nb + "_E2_wRD.nii.gz"])
    wRD_all = np.append(wRD_all,paths, axis = 0)
wRD_all = np.reshape(wRD_all, ((len(patient_numbers)+1), 2))
wRD_all = np.delete(wRD_all, (0), axis = 0)


# =============================================================================
# REGISTRATION 
# =============================================================================
def registration(to_register, tenseur):
  
  if (tenseur == False):
      for Patient, patient_nb in zip(fractions_all_bis, to_register):
          transform1 = getTransform(Patient[0], Patient[3], onlyAffine=False, diffeomorph=True, sanity_check=False)
          applyTransform(Patient[3], transform1, Patient[0], 
                         patients_path + "#" + patient_nb + "/Registration/microstructure/diamond/sub" + patient_nb + "_diamond_fractions_f0_E2_reg_on_E1.nii.gz",
                         binary = False) 
          applyTransform(Patient[4], transform1, Patient[1], 
                         patients_path + "#" + patient_nb + "/Registration/microstructure/diamond/sub" + patient_nb + "_diamond_fractions_f1_E2_reg_on_E1.nii.gz",
                         binary = False)  
          applyTransform(Patient[5], transform1, Patient[2], 
                         patients_path + "#" + patient_nb + "/Registration/microstructure/diamond/sub" + patient_nb + "_diamond_fractions_csf_E2_reg_on_E1.nii.gz",
                         binary = False)  
          
  else:
      for Patient, MD_Patient, AD_Patient, RD_Patient, patient_nb in zip(wFA_all, wMD_all, wAD_all, wRD_all, to_register):
          print("-----------------------------")
          print("Patient n°",patient_nb)
          print("-----------------------------")
          transform1 = getTransform(Patient[0], Patient[1], onlyAffine=False, diffeomorph=True, sanity_check=False)
          applyTransform(Patient[1], transform1, Patient[0], 
                         patients_path + "#" + patient_nb + "/Registration/microstructure/diamond/sub" + patient_nb + "_wFA_E2_reg_on_E1.nii.gz",
                         binary = False) 
          applyTransform(MD_Patient[1], transform1, MD_Patient[0], 
                         patients_path + "#" + patient_nb + "/Registration/microstructure/diamond/sub" + patient_nb + "_wMD_E2_reg_on_E1.nii.gz",
                         binary = False)  
          applyTransform(AD_Patient[1], transform1, AD_Patient[0], 
                         patients_path + "#" + patient_nb + "/Registration/microstructure/diamond/sub" + patient_nb + "_wAD_E2_reg_on_E1.nii.gz",
                         binary = False)  
          applyTransform(RD_Patient[1], transform1, RD_Patient[0], 
                         patients_path + "#" + patient_nb + "/Registration/microstructure/diamond/sub" + patient_nb + "_wRD_E2_reg_on_E1.nii.gz",
                         binary = False)  

to_register = patient_numbers
# registration(to_register, False)
# registration(to_register, True)








