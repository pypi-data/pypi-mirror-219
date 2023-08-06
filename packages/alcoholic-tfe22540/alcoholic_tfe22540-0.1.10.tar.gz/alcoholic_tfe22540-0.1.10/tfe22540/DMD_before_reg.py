"""
Created on Wed Mar 23 15:00:24 2022

@author: Fauston
"""

import numpy as np
import nibabel as nib

from tfe22540.CN2 import getTransform, applyTransform

perso_path = "/CECI/proj/pilab/PermeableAccess/alcoolique_TnB32xGDr7h/alcoholic_study/subjects/"

patient_numbers = ["02", "04", "05", "08", "09", "11", "12", "13", "14", "15", "17", "18", "19", "20", "21", "22", "24","26", "27", "28", "30", "31", "32", "33", "34", "35" , "36", "37", "39", "40", "41", "42", "43", "45", "46"]

def get_fractions(patient_nb, fractions_all):
    
    """
    Parameters
    ----------
    patient_nb : String
        Number of patients.
        
    fractions_all : List of file path in string
        File containing the fractions of one patient for T1 and T2.

    Returns
    -------
    List of all the subfile contained in input file fractions. Just a function to get the proper files to work. 
    """
    
    fraction_T1 = np.squeeze((nib.load(fractions_all[0]).get_fdata())[:,:,:,:,0])
    out_T1 = nib.Nifti1Image(fraction_T1, nib.load(fractions_all[0]).affine, header=nib.load(fractions_all[0]).header)
    out_T1.to_filename(perso_path + "sub" + patient_nb + "_T1/dMRI/microstructure/diamond/sub" + patient_nb + "_T1_diamond_fractions_f0.nii.gz")
    
    fraction1_T1 = np.squeeze((nib.load(fractions_all[0]).get_fdata())[:,:,:,:,1])
    out1_T1 = nib.Nifti1Image(fraction1_T1, nib.load(fractions_all[0]).affine, header=nib.load(fractions_all[0]).header)
    out1_T1.to_filename(perso_path + "sub" + patient_nb + "_T1/dMRI/microstructure/diamond/sub" + patient_nb + "_T1_diamond_fractions_f1.nii.gz")
    
    fraction2_T1 = np.squeeze((nib.load(fractions_all[0]).get_fdata())[:,:,:,:,2])
    out2_T1 = nib.Nifti1Image(fraction2_T1, nib.load(fractions_all[0]).affine, header=nib.load(fractions_all[0]).header)
    out2_T1.to_filename(perso_path + "sub" + patient_nb + "_T1/dMRI/microstructure/diamond/sub" + patient_nb + "_T1_diamond_fractions_csf.nii.gz")
    
    fraction_T2 = np.squeeze((nib.load(fractions_all[1]).get_fdata())[:,:,:,:,0])
    out_T2 = nib.Nifti1Image(fraction_T2, nib.load(fractions_all[1]).affine, header=nib.load(fractions_all[1]).header)
    out_T2.to_filename(perso_path + "sub" + patient_nb + "_T2/dMRI/microstructure/diamond/sub" + patient_nb + "_T2_diamond_fractions_f0.nii.gz")
    
    fraction1_T2 = np.squeeze((nib.load(fractions_all[1]).get_fdata())[:,:,:,:,1])
    out1_T2 = nib.Nifti1Image(fraction1_T2, nib.load(fractions_all[1]).affine, header=nib.load(fractions_all[1]).header)
    out1_T2.to_filename(perso_path + "sub" + patient_nb + "_T2/dMRI/microstructure/diamond/sub" + patient_nb + "_T2_diamond_fractions_f1.nii.gz")
    
    fraction2_T2 = np.squeeze((nib.load(fractions_all[1]).get_fdata())[:,:,:,:,2])
    out2_T2 = nib.Nifti1Image(fraction2_T2, nib.load(fractions_all[1]).affine, header=nib.load(fractions_all[1]).header)
    out2_T2.to_filename(perso_path + "sub" + patient_nb + "_T2/dMRI/microstructure/diamond/sub" + patient_nb + "_T2_diamond_fractions_csf.nii.gz")
    
    return [perso_path + "sub" + patient_nb + "_T1/dMRI/microstructure/diamond/sub" + patient_nb + "_T1_diamond_fractions_f0.nii.gz",
            perso_path + "sub" + patient_nb + "_T1/dMRI/microstructure/diamond/sub" + patient_nb + "_T1_diamond_fractions_f1.nii.gz",
            perso_path + "sub" + patient_nb + "_T1/dMRI/microstructure/diamond/sub" + patient_nb + "_T1_diamond_fractions_csf.nii.gz",
            perso_path + "sub" + patient_nb + "_T2/dMRI/microstructure/diamond/sub" + patient_nb + "_T2_diamond_fractions_f0.nii.gz",
            perso_path + "sub" + patient_nb + "_T2/dMRI/microstructure/diamond/sub" + patient_nb + "_T2_diamond_fractions_f1.nii.gz",
            perso_path + "sub" + patient_nb + "_T2/dMRI/microstructure/diamond/sub" + patient_nb + "_T2_diamond_fractions_csf.nii.gz"]


# =============================================================================
# FRACTIONS
# =============================================================================
fractions_all = np.array(["fractions_T1","fractions_T2"])
for patient_nb in patient_numbers:
    paths = np.array([perso_path + "sub" + patient_nb + "_T1/dMRI/microstructure/diamond/sub" + patient_nb + "_T1_diamond_fractions.nii.gz",
                      perso_path + "sub" + patient_nb + "_T2/dMRI/microstructure/diamond/sub" + patient_nb + "_T2_diamond_fractions.nii.gz"])                  
    fractions_all = np.append(fractions_all, paths, axis=0)
fractions_all = np.reshape(fractions_all,((len(patient_numbers)+1),2))
fractions_all = np.delete(fractions_all, (0), axis=0)

fractions_all_bis = []

for i,j in zip(patient_numbers,range(len(patient_numbers))):
    fractions_all_bis.append(get_fractions(i, fractions_all[j]))


