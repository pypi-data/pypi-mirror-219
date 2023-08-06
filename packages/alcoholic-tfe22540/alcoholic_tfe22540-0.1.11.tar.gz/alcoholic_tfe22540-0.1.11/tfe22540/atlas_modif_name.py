"""
Created on Thu Mar 17 12:15:10 2022

@author: Fauston
"""

import os
import numpy as np

from tfe22540.perso_path import perso_path_string

def get_atlas_list(onlywhite=False, with_CC=True):
    
    """
        Parameters
        ----------
        onlywhite : Boolean, optional
            To choose the type of matter: true for white matter atlases only and false for all atlases. The default is False.
    
        Returns
        -------
        atlas_list : List of tuples. 
            The latter contains the path of the atlas, its threshold and a number used to descriminate the different areas.
    """
    
    perso_path, excel_path, subjects_path, patients_path, plot_path, atlas_path = perso_path_string()
    
    folder = atlas_path
    
    atlas_list = []
    
    seuil_cerebellar = 0.2
    seuil_cerebellum = 50
    seuil_xtract = 30
    seuil_harvard = 30
    seuil_lobes = 30
    seuil_cortex = 30
    seuil_CC = 0
    
    CC_count = 0
    
    for filename in os.listdir(folder):
        if (filename=="FSL_HCP1065_FA_1mm.nii.gz" or filename=="00Average_Brain.nii"):
            continue
        else:
            subfile_name = folder + "/" + filename
            
            for atlas_name in os.listdir(subfile_name):
                atlas_path = filename + "/" + atlas_name
                if (onlywhite==False):
                    if("Cerebellar" in atlas_path):
                        atlas_list.append([atlas_path, seuil_cerebellar, 3])
                    elif("Cerebellum" in atlas_path):
                        atlas_list.append([atlas_path, seuil_cerebellum, 4])
                    elif("harvardoxford-subcortical" in atlas_path):
                        atlas_list.append([atlas_path, seuil_harvard, 2])
                    elif("harvardoxford-cortical" in atlas_path):
                        atlas_list.append([atlas_path, seuil_cortex, 0])
                    elif("mni_prob" in atlas_path):
                        atlas_list.append([atlas_path, seuil_lobes, 5])
                    elif("xtract_prob" in atlas_path):
                        atlas_list.append([atlas_path, seuil_xtract, 1])
                else:
                    if("Cerebellar" in atlas_path):
                        atlas_list.append([atlas_path, seuil_cerebellar, 3])
                    elif("Cerebellum" in atlas_path):
                        atlas_list.append([atlas_path, seuil_cerebellum, 4])
                    elif("harvardoxford-subcortical" in atlas_path):
                        atlas_list.append([atlas_path, seuil_harvard, 2])
                    elif("xtract_prob" in atlas_path):
                        atlas_list.append([atlas_path, seuil_xtract, 1])
            
    if(with_CC==True):   
        corpus_callosum = "CC/Corpus_callosum_hand_drawn_morpho.nii.gz"
        atlas_list.append([corpus_callosum, seuil_CC, 6])
        corpus_callosum_genu = "CC/Corpus_callosum_genu.nii.gz"
        atlas_list.append([corpus_callosum_genu, seuil_CC, 6])
        corpus_callosum_anterior_midbody = "CC/Corpus_callosum_anterior_midbody.nii.gz"
        atlas_list.append([corpus_callosum_anterior_midbody, seuil_CC, 6])
        corpus_callosum_posterior_midbody = "CC/Corpus_callosum_posterior_midbody.nii.gz"
        atlas_list.append([corpus_callosum_posterior_midbody, seuil_CC, 6])
        corpus_callosum_isthmus = "CC/Corpus_callosum_isthmus.nii.gz"
        atlas_list.append([corpus_callosum_isthmus, seuil_CC, 6])
        corpus_callosum_splenium = "CC/Corpus_callosum_splenium.nii.gz"
        atlas_list.append([corpus_callosum_splenium, seuil_CC, 6])
                    
                    
    return atlas_list

def get_corr_atlas_list(atlas_list):

    """
        Parameters
        ----------
        atlas_list : List of tuples. 
            List of tuples coming from get_atlas_list() function.
    
        Returns
        -------
        atlas_name : List of tuples.
            Same list of tuples of atlas list but with an extra component in the tuple corresponding to a corrected name of the atlas.
    """
    
    atlas_name = np.array(["altas_corr","atlas", 0, 0])

    for i in range(len(atlas_list)):
        name = (atlas_list[i])[0]
        if("xtract" in name):
            name = name.replace('xtract_prob_', '')
        if("harvardoxford" in name):
            name = name.replace('harvardoxford-subcortical_', '')
            name = name.replace('harvardoxford-cortical_', '')
            name = name.replace('prob_', '')
        if("mni_" in name):
            name = name.replace('mni_prob_', '')
        if("cerebellum_mniflirt_prob_" in name):
            name = name.replace('mniflirt_prob_', '')
        if("Cerebellar/" in name):
            name = name.replace('Cerebellar/', '')
        if("Cerebelar" in name):
            name = name.replace('Cerebelar', 'Cerebellar')
        if("Cerebellum/" in name):
            name = name.replace('Cerebellum/', '')
        if("Harvard/" in name):
            name = name.replace('Harvard/', '')
        if("Harvard_cortex/" in name):
            name = name.replace('Harvard_cortex/', '')
        if("Lobes/" in name):
            name = name.replace('Lobes/', '')
        if("XTRACT/" in name):
            name = name.replace('XTRACT/', '')
        if("CC/" in name): 
            name = name.replace('CC/', '')
        if("Juxtapositional" in name):
            name = name.replace('(formerly_Supplementary_Motor_Cortex)','')
        if("cerebellum" in name):
            name = name.replace('cerebellum','Cerebellum')
        if("Amygdala" in name):
            name = name.replace(' Amygdala','Amygdala')
        if("Thalamus" in name):
            name = name.replace(' Thalamus','Thalamus')
        if("Caudate" in name):
            name = name.replace(' Caudate','Caudate')
        if("Cerebral" in name):
            name = name.replace(' Cerebral','Cerebral')
        if("Hippocampus" in name):
            name = name.replace(' Hippocampus','Hippocampus')
        if('Putamen' in name):
            name = name.replace(' Putamen','Putamen')
        if("Right" in name):
            name = name.replace('Right','')
            name = name + " R"
        if("Left" in name):
            name = name.replace('Left','')
            name = name + " L"
        if("_hand_drawn_morpho" in name):
            name = name.replace('_hand_drawn_morpho', '')
        name = name.replace('.nii.gz', '')
        name = name.replace('_', ' ')
        
        vecteur = np.array([name, (atlas_list[i])[0], (atlas_list[i])[1], (atlas_list[i])[2]])
        atlas_name = np.append(atlas_name, vecteur, axis=0)
    
    atlas_name = np.reshape(atlas_name, ((len(atlas_list)+1),4))
    atlas_name = np.delete(atlas_name, (0), axis=0)
    atlas_name = atlas_name.tolist()
    atlas_name = sorted(atlas_name, key=lambda x:x[0])
    atlas_name = np.array(atlas_name)

    return atlas_name          
                    
# atlas_list = get_atlas_list(onlywhite=False) 
# atlas_name = get_corr_atlas_list(atlas_list)