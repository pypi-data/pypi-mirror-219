"""
Created on Wed Mar 23 15:00:24 2022

@author: Fauston
"""

import numpy as np
import nibabel as nib

from tfe22540.CN2 import getTransform, applyTransform
from tfe22540.perso_path import perso_path_string, patient_number_list



def get_fractions(folder_path, patient_path):
    
    """
        Parameters
        ----------
        patient_nb : String
            Number of patients.
            
        fractions_all : List of file path in string
            File containing the fractions of one patient for E1 and E2.
    
        Returns
        -------
        List of all the subfile contained in input file fractions. Just a function to get the proper files to work. 
    """
    
    fractions_diamond = nib.load(folder_path + "/subjects/" + patient_path + "/dMRI/microstructure/diamond/" + patient_path + "_diamond_fractions.nii.gz")
    
    fractions_diamond_array = fractions_diamond.get_fdata()
    
    fraction_f0 = np.squeeze(fractions_diamond_array[:,:,:,:,0])
    fraction_f1 = np.squeeze(fractions_diamond_array[:,:,:,:,1])
    fraction_csf = np.squeeze(fractions_diamond_array[:,:,:,:,2])
    
    out_f0 = nib.Nifti1Image(fraction_f0, fractions_diamond.affine, header=fractions_diamond.header)
    out_f0.to_filename(folder_path + "/subjects/" + patient_path + "/dMRI/microstructure/diamond/" + patient_path + "_diamond_fractions_f0.nii.gz")
    
    out_f1 = nib.Nifti1Image(fraction_f1, fractions_diamond.affine, header=fractions_diamond.header)
    out_f1.to_filename(folder_path + "/subjects/" + patient_path + "/dMRI/microstructure/diamond/" + patient_path + "_diamond_fractions_f1.nii.gz")
    
    out_csf = nib.Nifti1Image(fraction_csf, fractions_diamond.affine, header=fractions_diamond.header)
    out_csf.to_filename(folder_path + "/subjects/" + patient_path + "/dMRI/microstructure/diamond/" + patient_path + "_diamond_fractions_csf.nii.gz")