"""
Created on Sat Apr  9 09:44:36 2022

@author: Fauston
"""

from skimage.morphology import area_opening,area_closing
import nibabel as nib 

from tfe22540.perso_path import perso_path_string


perso_path, excel_path, subjects_path, patients_path, plot_path, atlas_path = perso_path_string() 

def closing_opening(folder_path, patient_path):
    
    """
        Parameters
        ----------
        patient_number : String
            Number of the patient.
    
        Returns
        -------
        None. Save a .nii.gz file after having apply two morphological operations (opening and closing) on the CC.
    """
    
    name = str(patient_path)
    if ("sub" in name):
        name = name.replace('sub', '')
        
    patient_id = name.replace('_E1','').replace('_E2','').replace('_E3','')
    
    path = patients_path + "#" + patient_id + "/Atlas/CC/Corpus_callosum_hand_drawn_reg_on_sub" + name + ".nii.gz"
    
    image = nib.load(path).get_fdata()
    
    opening_mask = area_opening(image, area_threshold = 30, connectivity = 1, parent = None, tree_traverser = None)
    closing_mask = area_closing(opening_mask, area_threshold = 30, connectivity = 1, parent = None, tree_traverser = None) 
    
    out = nib.Nifti1Image(closing_mask, affine = nib.load(path).affine, header = nib.load(path).header)
    out.to_filename(patients_path + "#" + patient_id + "/Atlas/CC/Corpus_callosum_hand_drawn_morpho_reg_on_sub" + name + ".nii.gz")