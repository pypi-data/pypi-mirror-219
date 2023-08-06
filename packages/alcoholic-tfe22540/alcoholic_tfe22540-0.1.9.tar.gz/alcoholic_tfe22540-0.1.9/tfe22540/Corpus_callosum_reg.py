"""
Created on Fri Apr  8 10:41:42 2022

@author: Fauston
"""

import numpy as np
from CN2 import getTransform, applyTransform
import nibabel as nib

from tfe22540.perso_path import perso_path_string

# Transformation of the Corpus Callosum coming from Natbrainlab to fit it with the perfect patient.
# Then will be registered on each patient (E1 and E2) thanks to the atlas_registration script.

perso_path, excel_path, subjects_path, patients_path, plot_path, atlas_path = perso_path_string() 


# =============================================================================
# REGISTRATION
# =============================================================================
def registration_CC_on_perfect(folder_path, patient_path):
    
    """
        Parameters
        ----------
        folder_path : String 
            Link of the file in which we are. 
        patient_path : List of strings
            Number of all patients in string ["sub#_E1"] for example.
            
        Returns
        -------
        None. Save a .nii.gz file of the transformation of the CC.
    """
    
    Patient = [atlas_path + "00Average_Brain.nii",
               atlas_path + "FSL_HCP1065_FA_1mm.nii.gz",
               atlas_path + "CC/Corpus_Callosum.nii.gz"]

    transform1 = getTransform(Patient[1], Patient[0], onlyAffine = False, diffeomorph = True, sanity_check = False)
    applyTransform(Patient[2], transform1, Patient[1], atlas_path + "CC/Corpus_Callosum_reg.nii.gz",binary = False)
    
def reg_CC_on_sub(folder_path, patient_path):

    """
        Parameters
        ----------
        folder_path : String 
            Link of the file in which we are. 
    
        patient_path : List of strings
            Number of all patients in string ["sub#_E1"] for example.
            
        Returns
        -------
        None. Save a .nii.gz file of the transformation of the considered atlas.
    """
    
    name = str(patient_path)
    if ("sub" in name):
        name = name.replace('sub', '')
        
    patient_id = name.replace('_E1','').replace('_E2','').replace('_E3','')
           
    Patient = [atlas_path + "FSL_HCP1065_FA_1mm.nii.gz",
               subjects_path + "sub" + name + "/dMRI/microstructure/dti/sub" + name + "_FA.nii.gz",
               atlas_path + "CC/Corpus_callosum_hand_drawn.nii.gz"]
               
    transform = getTransform(Patient[1], Patient[0], onlyAffine=False, diffeomorph=True, sanity_check=False)
    
    applyTransform(Patient[2], transform, Patient[1], patients_path + "#" + patient_id + "/Atlas/CC/Corpus_callosum_hand_drawn_reg_on_sub" + name + ".nii.gz",binary = False)



# =============================================================================
# MASK FA
# =============================================================================
def mask_wm_FA(FA):
    """
        Parameters
        ----------
        FA : File path (already load by nibabel) of the FA map of the perfect patient. 
        
        Returns
        -------
        a : Matrix of int
            Map of FA corresponding to a mask of FA so characterizing only the white matter.
    """
    
    FA_bis = FA.get_fdata()
    a = np.copy(FA_bis)
    a[a <= 0.34] = 0
    a[a > 0.34] = 1

    return a
    
# Corpus_callosum = nib.load(atlas_path + "CC/Corpus_Callosum_reg.nii.gz").get_fdata()
# perfect_path = nib.load(atlas_path + "FSL_HCP1065_FA_1mm.nii.gz")

# Creation of a mask of Corpus Callosum area 
# CC_mask = Corpus_callosum.copy()
# CC_mask[CC_mask <= 0.14] = 0

# FA_mask = mask_wm_FA(perfect_path)
# mask_final_CC = FA_mask*CC_mask

# out1 = nib.Nifti1Image(mask_final_CC, perfect_path.affine, header = perfect_path.header)
# out1.to_filename(atlas_path + "CC/Corpus_callosum_apres_FA_et_seuil_CC.nii.gz")

