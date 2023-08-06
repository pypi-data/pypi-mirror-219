import os
import sys
import numpy as np
import nibabel as nib
from dipy.segment.mask import median_otsu
from dipy.io.image import load_nifti, load_nifti_data
from dipy.align.imaffine import (transform_centers_of_mass,
                                 AffineMap,
                                 MutualInformationMetric,
                                 AffineRegistration)
from dipy.align.transforms import (TranslationTransform3D,
                                   RigidTransform3D,
                                   AffineTransform3D)
from dipy.align.imwarp import SymmetricDiffeomorphicRegistration
from dipy.align.metrics import CCMetric


# Functions

def getTransform(static_volume_file,moving_volume_file,onlyAffine=False,
                 diffeomorph=True,sanity_check=False):
    
    static, static_affine = load_nifti(static_volume_file)
    static_grid2world = static_affine
    
    moving, moving_affine = load_nifti(moving_volume_file)
    moving_grid2world = moving_affine
    
    # Affine registration -----------------------------------------------------
    
    if sanity_check or onlyAffine:
        
        identity = np.eye(4)
        affine_map = AffineMap(identity,
                               static.shape, static_grid2world,
                               moving.shape, moving_grid2world)
        resampled = affine_map.transform(moving)

        if onlyAffine:
            
            return affine_map
    
    c_of_mass = transform_centers_of_mass(static, static_grid2world,
                                          moving, moving_grid2world)
    
    nbins = 32
    sampling_prop = None
    metric = MutualInformationMetric(nbins, sampling_prop)
    
    #!!!
    level_iters = [10000, 1000, 100]
    #level_iters = [1000, 100, 10]
    sigmas = [3.0, 1.0, 0.0]
    factors = [4, 2, 1]
    affreg = AffineRegistration(metric=metric,
                                level_iters=level_iters,
                                sigmas=sigmas,
                                factors=factors)
    
    transform = TranslationTransform3D()
    params0 = None
    translation = affreg.optimize(static, moving, transform, params0,
                                  static_grid2world, moving_grid2world,
                                  starting_affine=c_of_mass.affine)
    
    transform = RigidTransform3D()
    rigid = affreg.optimize(static, moving, transform, params0,
                            static_grid2world, moving_grid2world,
                            starting_affine=translation.affine)
    
    transform = AffineTransform3D()
    affine = affreg.optimize(static, moving, transform, params0,
                             static_grid2world, moving_grid2world,
                             starting_affine=rigid.affine)
    
    # Diffeomorphic registration --------------------------
    
    if diffeomorph:
    
        metric = CCMetric(3)
        
        level_iters = [10000, 1000, 100]
        sdr = SymmetricDiffeomorphicRegistration(metric, level_iters)
        
        mapping = sdr.optimize(static, moving, static_affine, moving_affine,
                               affine.affine)
        
    else:
        
        mapping = affine
        
    if sanity_check:
        
        transformed = mapping.transform(moving)
        #transformed_static = mapping.transform_inverse(static)
    
    return mapping

def applyTransform(file_path,mapping,static_file='',output_path='',binary=False,inverse=False):
    
    moving=nib.load(file_path)
    moving_data=moving.get_fdata()
    
    if inverse:
        transformed=mapping.transform_inverse(moving_data)
    else:
        transformed=mapping.transform(moving_data)
    
    if binary:
        transformed[transformed>.5]=1
        transformed[transformed<=.5]=0
    
    print(output_path)
    if len(output_path)>0:        
        
        static=nib.load(static_file)
                
        out=nib.Nifti1Image(transformed,static.affine,header=static.header)
        out.to_filename(output_path)
        
    else:
        return transformed

def reg_all_patient_on_perfect(pE1):    
    
    methods = ["dti", "noddi", "diamond", "mf_CSD"] 
    metric_name_DTI = ["FA", "MD", "AD", "RD"]
    metric_name_NODDI = ["fintra","fextra", "fiso", "odi"]
    metric_name_DIAMOND = ["wFA", "wMD", "wAD", "wRD", "diamond_fractions_ftot","diamond_fractions_csf"]
    metric_name_MF = ["frac_csf", "fvf_tot"]
    
    path1 = '/CECI/proj/pilab/PermeableAccess/alcoolique_TnB32xGDr7h/alcoholic_study_v2/subjects/'
    path2 = '/dMRI/microstructure/'
    path3 = '.nii.gz'
    parfait_vol = '/CECI/proj/pilab/PermeableAccess/alcoolique_TnB32xGDr7h/Nifti/FSL_HCP1065_FA_1mm.nii.gz'
    

    patient_vol = path1 + pE1 + path2 + 'dti' + '/' + pE1 + '_FA' + path3
    transform = getTransform(parfait_vol, patient_vol, onlyAffine=False, diffeomorph=True, sanity_check=False)
    for method in methods : 
        if method == "dti" : 
            lst = metric_name_DTI
        if method == "noddi" : 
            lst = metric_name_NODDI
        if method == "diamond" : 
            lst = metric_name_DIAMOND
        if method == "mf_CSD" : 
            lst = metric_name_MF
        for metric in lst:
            if method == "dti" or method == 'diamond': 
                actual_vol = path1 + pE1 + path2 + method + '/' + pE1 + '_' + metric + path3
            if method == "noddi": 
                actual_vol = path1 + pE1 + path2 + method + '/' + pE1 + '_' + method + '_' + metric + path3
            if method == "mf_CSD" : 
                actual_vol = path1 + pE1 + path2 + method + '/' + pE1 + '_mf' + '_' + metric + path3
            out = '/CECI/proj/pilab/PermeableAccess/alcoolique_TnB32xGDr7h/Nifti/' + pE1 + '_' + method + '_' + metric + path3
            #print(patient_vol)
            #print(out)
            applyTransform(actual_vol, transform, parfait_vol, out, binary=False, inverse=False)
    return
    
reg_all_patient_on_perfect(sys.argv[1])