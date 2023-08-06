"""
Created on Wed Mar  9 09:35:09 2022

@author: Fauston
"""

import os
import numpy as np

from tfe22540.CN2 import getTransform, applyTransform
from tfe22540.atlas_modif_name import get_corr_atlas_list, get_atlas_list
from tfe22540.perso_path import perso_path_string

def registration_atlas(folder_path, patient_path):

    perso_path, excel_path, subjects_path, patients_path, plot_path, atlas_path = perso_path_string() 

    # =============================================================================
    # PATIENTS
    # =============================================================================
    perfect = perso_path + "Atlas/FSL_HCP1065_FA_1mm.nii.gz"
    
    # =============================================================================
    # ATLAS
    # =============================================================================
    atlas_list = get_atlas_list(with_CC=False)
    atlas_name = get_corr_atlas_list(atlas_list)
    
    # =============================================================================
    # REGISTRATION 
    # =============================================================================
    # DESCRIPTION : getTransform(static_file, moving_file,...) and applyTransform(moving_file, mapping calculated by getTransform(), static_file).
    #               Mapping here is transform1 which is the transformation |b| E1 (static) of each patient and the perfect patient (moving) on which the atlased are based.
    #               Then we apply this transform1 on the atlas to make it fit to the E1 of each patient. We do the same for E2 as we work in the patient space.
    
    # ATTENTION - pas besoin de registrer le corps calleux (with_CC = False)
    
    name = str(patient_path)
    if ("E1" in name) : 
        name = name.replace('_E1','')  
    if ("E2" in name) : 
        name = name.replace('_E2','')  
    if ("E3" in name) :
        name = name.replace('_E3','')   
    if ("sub" in name):
        name = name.replace('sub','')
        
    p = str(patient_path)
    p = p.replace('sub','')
    

    Patient = np.array([perfect, 
                        perso_path + "alcoholic_study/subjects/sub" + p + "/dMRI/microstructure/dti/sub" + p + "_FA.nii.gz"])
    
    transform1 = getTransform(Patient[1], Patient[0], onlyAffine=False, diffeomorph=True, sanity_check=False)
    for Atlas in atlas_name:
        name_atlas = str(Atlas[1])
        if ('.nii.gz' in name_atlas):
            name_atlas = name_atlas.replace('.nii.gz', '')

        applyTransform(perso_path + "Atlas/" + Atlas[1], transform1, Patient[1], 
                       perso_path + "Patients/#" + name + "/Atlas/" + name_atlas + "_reg_on_sub" + p + ".nii.gz", binary = False)  
    