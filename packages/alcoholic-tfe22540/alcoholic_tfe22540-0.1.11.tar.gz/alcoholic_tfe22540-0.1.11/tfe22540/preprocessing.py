import elikopy 
import elikopy.utils
from elikopy.individual_subject_processing import report_solo

f_path="/CECI/proj/pilab/PermeableAccess/alcoolique_TnB32xGDr7h/alcoholic_study/" 
dic_path="/home/users/q/d/qdessain/Script_python/fixed_rad_dist.mat"

patient_list = None
                                   
study = elikopy.core.Elikopy(f_path, slurm=True, slurm_email='manon.dausort@uclouvain.be', cuda=False)

# =============================================================================
# Patient list
# =============================================================================
study.patient_list()

# =============================================================================
# Preprocessing
# =============================================================================
# study.preproc(eddy=True,
# 	            topup=True,
#               denoising=True, 
#               mppca_legacy_denoising=True, 
#               reslice=True, 
#               gibbs=False, 
#               biasfield=False,
# 	            patient_list_m=patient_list, 
#               qc_reg=True,
# 	            starting_state="post_report", 
#               report=True)

# =============================================================================
# Mask of white matter
# =============================================================================
# study.white_mask(patient_list_m=patient_list, corr_gibbs=True, cpus=2, debug=False) 
   
# =============================================================================
# Microstructural models
# =============================================================================
# study.dti(patient_list_m=patient_list)
# study.noddi(use_wm_mask=False, patient_list_m=patient_list, cpus=4)
# study.fingerprinting(dic_path, patient_list_m=patient_list, cpus=8, CSD_bvalue=6000)
# study.diamond(patient_list_m=patient_list,slurm_timeout="30:00:00",cpus=8)

# =============================================================================
# Stats
# =============================================================================
# grp1=[1]
# grp2=[2]

# study.regall_FA(grp1=grp1,grp2=grp2, registration_type="-T", postreg_type="-S", prestats_treshold=0.2, cpus=8)

# metrics={'_noddi_odi':'noddi','_mf_fvf_tot':'mf'}
# study.regall(grp1=grp1,grp2=grp2, metrics_dic=metrics)
# study.randomise_all(randomise_numberofpermutation=0,skeletonised=True,metrics_dic=metrics,regionWiseMean=True,cpus=1,slurm_timeout="1:00:00")

# =============================================================================
# Export
# =============================================================================
# study.export(tractography=True, raw=False, preprocessing=False, dti=True, noddi=False, diamond=False, mf=False, wm_mask=False, report=False, preprocessed_first_b0=False, patient_list_m=None)
# elikopy.utils.merge_all_reports(f_path)
