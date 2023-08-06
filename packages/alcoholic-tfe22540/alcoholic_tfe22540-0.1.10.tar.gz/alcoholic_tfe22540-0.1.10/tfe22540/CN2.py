# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 21:11:14 2021

@author: Nicolas Delinte
"""

import numpy as np
import nibabel as nib
from dipy.io.image import load_nifti
from dipy.align.metrics import CCMetric
from dipy.align.imwarp import SymmetricDiffeomorphicRegistration
from dipy.align.transforms import (TranslationTransform3D, RigidTransform3D, AffineTransform3D)
from dipy.align.imaffine import (transform_centers_of_mass, AffineMap, MutualInformationMetric, AffineRegistration)

def getTransform(static_volume_file, moving_volume_file, onlyAffine=False, 
                 diffeomorph=True, sanity_check=False):
    """
    Parameters
    ----------
    static_volume : 3D array of static volume
    moving_volume : 3D array of moving volume
    diffeomorph : if False then registration is only affine
    sanity_check : if True then prints figures

    Returns
    -------
    mapping : transform operation to send moving_volume to static_volume space
    
    """
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
        
        # regtools.overlay_slices(static, resampled, None, 0,
        #                         "Static", "Moving", "resampled_0.png")
        # regtools.overlay_slices(static, resampled, None, 1,
        #                         "Static", "Moving", "resampled_1.png")
        # regtools.overlay_slices(static, resampled, None, 2,
        #                         "Static", "Moving", "resampled_2.png")
    
    if onlyAffine:
    
        return affine_map
    
    c_of_mass = transform_centers_of_mass(static, static_grid2world, moving, moving_grid2world)
    
    nbins = 32
    sampling_prop = None
    metric = MutualInformationMetric(nbins, sampling_prop)
    
    level_iters = [1000, 100, 10]
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
    
        level_iters = [1000, 100, 10]
        sdr = SymmetricDiffeomorphicRegistration(metric, level_iters)
        
        mapping = sdr.optimize(static, moving, static_affine, moving_affine, affine.affine)
    
    else:
        mapping = affine
    
    if sanity_check:
        
        transformed = mapping.transform(moving)
        # transformed_static = mapping.transform_inverse(static)
    
        # regtools.overlay_slices(static, transformed, None, 0,
        #                         "Static", "Transformed", "transformed.png")
        # regtools.overlay_slices(static, transformed, None, 1,
        #                         "Static", "Transformed", "transformed.png")
        # regtools.overlay_slices(static, transformed, None, 2,
        #                         "Static", "Transformed", "transformed.png")
    
    return mapping

def applyTransform(file_path,mapping,static_volume_file,output_path,binary=False):

    moving=nib.load(file_path)
    moving_data=moving.get_fdata()
    
    transformed=mapping.transform(moving_data)
    
    if binary:
        transformed[transformed>.5]=1
        transformed[transformed<=.5]=0
    
    static = nib.load(static_volume_file)
    
    out=nib.Nifti1Image(transformed,static.affine,header=static.header)
    out.to_filename(output_path)