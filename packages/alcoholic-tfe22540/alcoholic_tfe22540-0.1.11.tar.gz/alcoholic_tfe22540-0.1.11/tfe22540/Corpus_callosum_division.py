"""
Created on Fri Apr  1 09:30:33 2022

@author: Fauston
"""

import numpy as np
import nibabel as nib

from tfe22540.perso_path import perso_path_string


perso_path, excel_path, subjects_path, patients_path, plot_path, atlas_path = perso_path_string() 


# =============================================================================
# corpus CALLOSUM DIVISION
# =============================================================================
def CC_division(folder_path, patient_path):
    
    """
        Parameters
        ----------
        folder_path : String 
            Link of the file in which we are. 
        patient_path : List of strings
            Number of all patients in string ["sub#_E1"] for example.
    
        Returns
        -------
        None. Save a .nii.gz file of the each sub areas of the corpus Callosum.
    """
    
    name = str(patient_path)
    if ("sub" in name):
        name = name.replace('sub', '')
    
    patient_id = name.replace('_E1', '').replace('_E2', '').replace('_E3', '')
           
        
    CC_path = patients_path + "#" + patient_id + "/Atlas/CC/Corpus_callosum_hand_drawn_morpho_reg_on_sub" + name + ".nii.gz"
    
    corpus_callosum_load = nib.load(CC_path)
    corpus_callosum = corpus_callosum_load.get_fdata()
    
    corpus_callosum_genu = np.zeros(corpus_callosum.shape)
    corpus_callosum_anterior_midbody = np.zeros(corpus_callosum.shape)
    corpus_callosum_posterior_midbody = np.zeros(corpus_callosum.shape)
    corpus_callosum_isthmus = np.zeros(corpus_callosum.shape)
    corpus_callosum_splenium = np.zeros(corpus_callosum.shape)

    # Coordonnées de divisons
    ymin = 1000
    ymax = 0
    slice_cut = corpus_callosum[int(corpus_callosum.shape[0]/2),:,:]
    
    for j in range(corpus_callosum.shape[1]-1):
        for k in range(corpus_callosum.shape[2]): 
            
            if(slice_cut[j+1,k]-slice_cut[j,k] < 0):
                ystop = j
                ymax = max(ystop,ymax)
                
            if(slice_cut[j+1,k]-slice_cut[j,k] > 0):
                ystart = j+1
                ymin = min(ystart,ymin)

    # max_min_vect[0] = ymin
    # max_min_vect[1] = ymax
    
    len_CC = ymax - ymin
    
    print("ymax =", ymax)
    print("ymin =", ymin)
    
    # Coordonnées de début et de fin
    max_min_vect = np.zeros((corpus_callosum.shape[0],2)) 
    
    for i in range(corpus_callosum.shape[0]):
        
        ymin_tot = 1000
        ymax_tot = 0
        slice_cut = corpus_callosum[i,:,:]
        
        for j in range(corpus_callosum.shape[1]-1):
            for k in range(corpus_callosum.shape[2]):  
                
                if(slice_cut[j+1,k]-slice_cut[j,k] < 0):
                    ystop = j
                    ymax_tot = max(ystop,ymax_tot)
                    
                if(slice_cut[j+1,k]-slice_cut[j,k] > 0):
                    ystart = j+1
                    ymin_tot = min(ystart,ymin_tot)
    
        max_min_vect[i,0] = ymin_tot
        max_min_vect[i,1] = ymax_tot
    
    ymin_tot = min(max_min_vect[:,0][max_min_vect[:,0] != 0])
    ymax_tot = max(max_min_vect[:,1][max_min_vect[:,1] != 1000])

    for i in range(corpus_callosum.shape[0]):
        
        if(ymin_tot!=1000 and ymax_tot!=ymin_tot):
            coord2_splenium = round(ymin_tot)
            coord1_splenium = round(ymin + len_CC/4)
            coord2_isthmus = round(coord1_splenium)
            coord1_isthmus = round(ymin + len_CC/3)
            coord2_posterior = round(coord1_isthmus)
            coord1_posterior = round(ymin + len_CC/2)
            coord2_anterior = round(coord1_posterior)
            coord1_anterior = round(ymin + 5*len_CC/6) 
            coord2_genu = round(ymin + 5*len_CC/6)
            coord1_genu = round(ymax_tot)
            
            corpus_callosum_genu[i,coord2_genu:coord1_genu,:] = corpus_callosum[i,coord2_genu:coord1_genu,:]
    
            corpus_callosum_anterior_midbody[i,coord2_anterior:coord1_anterior,:] = corpus_callosum[i,coord2_anterior:coord1_anterior,:]
            
            corpus_callosum_posterior_midbody[i,coord2_posterior:coord1_posterior,:] = corpus_callosum[i,coord2_posterior:coord1_posterior,:]
            
            corpus_callosum_isthmus[i,coord2_isthmus:coord1_isthmus,:] = corpus_callosum[i,coord2_isthmus:coord1_isthmus,:]
           
            corpus_callosum_splenium[i,coord2_splenium:coord1_splenium,:] = corpus_callosum[i,coord2_splenium:coord1_splenium,:]


    out1 = nib.Nifti1Image(corpus_callosum_genu, affine = corpus_callosum_load.affine, header = corpus_callosum_load.header)
    out1.to_filename(patients_path + "#" + patient_id + "/Atlas/CC/Corpus_callosum_genu_reg_on_sub" + name + ".nii.gz")
    
    out2 = nib.Nifti1Image(corpus_callosum_anterior_midbody, corpus_callosum_load.affine, header = corpus_callosum_load.header)
    out2.to_filename(patients_path + "#" + patient_id + "/Atlas/CC/Corpus_callosum_anterior_midbody_reg_on_sub" + name + ".nii.gz")
    
    out3 = nib.Nifti1Image(corpus_callosum_isthmus, corpus_callosum_load.affine, header = corpus_callosum_load.header)
    out3.to_filename(patients_path + "#" + patient_id + "/Atlas/CC/Corpus_callosum_isthmus_reg_on_sub" + name + ".nii.gz")
    
    out4 = nib.Nifti1Image(corpus_callosum_posterior_midbody, corpus_callosum_load.affine, header = corpus_callosum_load.header)
    out4.to_filename(patients_path + "#" + patient_id + "/Atlas/CC/Corpus_callosum_posterior_midbody_reg_on_sub" + name + ".nii.gz")
    
    out5 = nib.Nifti1Image(corpus_callosum_splenium, corpus_callosum_load.affine, header = corpus_callosum_load.header)
    out5.to_filename(patients_path + "#" + patient_id + "/Atlas/CC/Corpus_callosum_splenium_reg_on_sub" + name + ".nii.gz")

