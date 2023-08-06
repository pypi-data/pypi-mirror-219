# Install in local 
If you want to download the lastest version directly from GitHub, you can close this repository

```git clone https://github.com/mdausort/TFE22-540```


# TFE22-540
The different steps to follow in order to obtain our results : 
  
  1) The first thing to do when receiving the data is to anonymise it and convert it with MRIcron. A naming convention is adopted "sub#_E1" or "sub#_E2" representing respectively the first and the second diffusion scan for each patient. While "sub#_T1_E." stands for the anatomical scan. 
  
  2) Those files have to be downloaded on the clusters in **alcoholic_study** to be preprocessed by [Elikopy](https://elikopy.readthedocs.io/en/latest/): 
      - data_1 file containing all "_E1";
      - data_2 file containing all "_E2";
      - reverse_encoding (respectivelly in the two previous files) containing the so-called corrected diffusion scans with the same naming convention than for the diffusion scan. If the DICOM files are corrupted, you can use [`reverse_corr.py`]() to obtain the right files and have a correct conversion in NIFTI;
      - T1 file containing all the anatomical scans (E1 and E2).
  
  3) [`useful_fct.py`](https://github.com/PiLAB-Medical-Imaging/TFE22-540_Alcohol/blob/main/Codes/useful_fct.py): Creation of the needed directories (already done for this study but have to be repeated if new patients → only thing to change is the **patient_numbers** variable).
  
  4) [`preprocessing.py`](https://github.com/PiLAB-Medical-Imaging/TFE22-540_Alcohol/blob/main/Codes/preprocessing.py): 
      - 4.1) Submit only the **Patient list** job.
      - 4.2) Submit only the **Preprocessing** job. 
      - 4.3) Submit only the **Mask de matière blanche** job.
      - 4.4) Submit the **Microstructural model** one at the time. 
      - Rest of this file can be used but was not necessary for us. 

  5) [`perso_path.py`](https://github.com/PiLAB-Medical-Imaging/TFE22-540_Alcohol/blob/main/Codes/perso_path.py): Before doing the following steps, you have to adapt the parameter of the **perso_path_string** function, **on_cluster**. If you put it at False, you have to change also the **perso_path** variable. And finally, you can also adapt the **patient_numbers** variable.
  
  6) [`atlas_registration.py`](https://github.com/PiLAB-Medical-Imaging/TFE22-540_Alcohol/blob/main/Codes/atlas_registration.py): Now that all patients have been pre-processed, we can perform an analysis by region. Thus, all the regions used are accessible through a list built with the [`atlas_modif_name.py`](https://github.com/PiLAB-Medical-Imaging/TFE22-540_Alcohol/blob/main/Codes/atlas_modif_name.py) file and called by other files. They are divided into "WM", "GM", "Lobes", "Subcortical" and "Cerebellum" areas. However, all those regions are not in the proper space so they need to be transformed to fit to each patient space and we used [`atlas_registration.py`](https://github.com/PiLAB-Medical-Imaging/TFE22-540_Alcohol/blob/main/Codes/atlas_registration.py) code in order to do that.\
→ To lauch this, use [`job_submission.py`](https://github.com/PiLAB-Medical-Imaging/TFE22-540_Alcohol/blob/main/Codes/job_submission.py) first line of **patientlist_wrapper** command only. 
  
  7) [`Corpus_callosum_reg.py`](https://github.com/PiLAB-Medical-Imaging/TFE22-540_Alcohol/blob/main/Codes/Corpus_callosum_reg.py): This is the code corresponding to the creation of our CC. As we can see on the following image, the downloaded Corpus Callosum was not of good quality (Fig A.) so we drew it ourselves (thanks to MRIcron) as depicted in Fig B. and its 3D representation (Fig C.). However, you don't need the **registration_CC_on_perfect** function and the last part of this file (MASK FA). You will only need to resubmit the **reg_CC_on_sub** if you have new patients.\
  → To lauch this, use [`job_submission.py`](https://github.com/PiLAB-Medical-Imaging/TFE22-540_Alcohol/blob/main/Codes/job_submission.py) thrid line of **patientlist_wrapper** command only. 
  
  <p align="center">
    <img src="https://user-images.githubusercontent.com/60848397/207355987-73e02c4a-b28d-4e19-b97f-bc9222023795.png" width="800" style="display: block; margin: 0 auto"/>
  </p>
  
  
  8) [`opening_closing.py`](https://github.com/PiLAB-Medical-Imaging/TFE22-540_Alcohol/blob/main/Codes/opening_closing.py): Just run this code to get a really smooth and good CC for each patient by applying some morphological operations. The upper part of the following image represents the drawn Corpus Callosum registered on one patient and the bottom part represents it after two morphological operations.
 
  <p align="center">
    <img src="https://user-images.githubusercontent.com/60848397/207364700-48d4efaa-07fc-4ee7-9457-903d163ba628.png" width="500" style="display: block; margin: 0 auto"/>
  </p>
  
  
  9) [`Corpus_callosum_division.py`](https://github.com/PiLAB-Medical-Imaging/TFE22-540_Alcohol/blob/main/Codes/Corpus_callosum_division.py): Code to obtained a subdivision of the CC.\
  → To lauch this, use [`job_submission.py`](https://github.com/PiLAB-Medical-Imaging/TFE22-540_Alcohol/blob/main/Codes/job_submission.py) fourth line of patientlist_wrapper command only. 
  
  <p align="center">
    <img src="https://user-images.githubusercontent.com/60848397/207373761-9a6f19c5-2238-4e03-b986-3d859a727d6c.png" width="800" style="display: block; margin: 0 auto"/>
  </p>

  10) [`f0_f1_to_ftot.py`](https://github.com/PiLAB-Medical-Imaging/TFE22-540_Alcohol/blob/main/Codes/f0_f1_to_ftot.py): Creation of some files for DIAMOND and MF models.
  
  11) [`FA_DMD.py`](https://github.com/PiLAB-Medical-Imaging/TFE22-540_Alcohol/blob/main/Codes/FA_DMD.py): Creation of weigthed version of the DTI metric for DIAMOND model.\
  → To lauch this, use [`job_submission.py`](https://github.com/PiLAB-Medical-Imaging/TFE22-540_Alcohol/blob/main/Codes/job_submission.py) fifth line of patientlist_wrapper command only and after the sixth line only.
  
  12) [`moyenne_par_ROI.py`](https://github.com/PiLAB-Medical-Imaging/TFE22-540_Alcohol/blob/main/Codes/moyenne_ROI_v2.py): Creation of different excels containing the different metric evolution.\
  → To lauch this, use [`job_submission.py`](https://github.com/PiLAB-Medical-Imaging/TFE22-540_Alcohol/blob/main/Codes/job_submission.py) seventh line of patientlist_wrapper command only.
  
  13) [`clustering.py`](https://github.com/PiLAB-Medical-Imaging/TFE22-540_Alcohol/blob/main/Codes/clustering.py): Creation of the clusters based on the method inplemented in [`DTI_kmeans_clustering.py`](https://github.com/PiLAB-Medical-Imaging/TFE22-540_Alcohol/blob/main/Codes/DTI_kmeans_clustering.py), then creation of excel called **Result_ttest**. The second code [`clustering_v2.py`](https://github.com/PiLAB-Medical-Imaging/TFE22-540_Alcohol/blob/main/Codes/clustering_v2.py) is another method of clustering.
  
  14) [`analyse_ttest.py`](https://github.com/PiLAB-Medical-Imaging/TFE22-540_Alcohol/blob/main/Codes/analyse_ttest.py): Creation of all the plots concerning the analysis of each model separately (they are saved in the file **Plots** in [Analyse](https://github.com/PiLAB-Medical-Imaging/TFE22-540_Alcohol/tree/main/Analyse)). Then, creation of excel called **Cluster_ROI** used to do the coherence analysis.
  
  15) [`DTI_tissue_classification.py`](https://github.com/PiLAB-Medical-Imaging/TFE22-540_Alcohol/blob/main/Codes/DTI_tissue_classification.py): To analyse change in volume for WM, GM and CSF. 
  
  16) [`volume_zones.py`](https://github.com/PiLAB-Medical-Imaging/TFE22-540_Alcohol/blob/main/Codes/volumes_zones.py): To analyse change in volume for certain areas of the brain. 
  
  17) [`comportement.py`](https://github.com/PiLAB-Medical-Imaging/TFE22-540_Alcohol/blob/main/Codes/comportement.py): To analyse the data coming from behavioral information. 
