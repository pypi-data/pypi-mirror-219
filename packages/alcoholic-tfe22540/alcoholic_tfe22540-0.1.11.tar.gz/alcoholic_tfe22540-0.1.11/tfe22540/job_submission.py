"""
Created on Thu Jul  7 10:39:41 2022

@author: Manon
"""

import elikopy 
import elikopy.utils
from elikopy.individual_subject_processing import report_solo

from tfe22540.atlas_registration import registration_atlas
from tfe22540.Corpus_callosum_reg import registration_CC_on_perfect, reg_CC_on_sub
from tfe22540.DMD_before_reg import get_fractions
from tfe22540.Corpus_callosum_division import CC_division
from tfe22540.f0_f1_to_ftot import f0_f1_to_ftot
#from moyenne_par_ROI import moyenne_par_roi 
from tfe22540.FA_DMD import get_cMetrics, get_FA_DIAMOND
from tfe22540.opening_closing import closing_opening

f_path = "/CECI/proj/pilab/PermeableAccess/alcooliques_copie/alcoholic_study/"
dic_path = "/home/users/q/d/qdessain/Script_python/fixed_rad_dist.mat"

patient_list = ["sub41_E1", "sub27_E1", "sub32_E1", "sub09_E1", "sub45_E1", "sub48_E1", "sub21_E1", "sub05_E1", "sub15_E1", "sub11_E1", "sub46_E1", "sub31_E1", "sub16_E1", "sub26_E1", "sub50_E1", "sub22_E1", "sub47_E1", "sub44_E1", "sub02_E1", "sub53_E1", "sub18_E1", "sub01_E1", "sub34_E1", "sub35_E1", "sub51_E1", "sub23_E1", "sub04_E1", "sub38_E1", "sub19_E1", "sub28_E1", "sub24_E1", "sub33_E1", "sub37_E1", "sub29_E1", "sub14_E1", "sub13_E1", "sub36_E1", "sub12_E1", "sub06_E1", "sub43_E1", "sub40_E1", "sub45_E3", "sub20_E1", "sub39_E1", "sub17_E1", "sub52_E1", "sub42_E1", "sub08_E1", "sub10_E1", "sub30_E1", "sub32_E2", "sub29_E2", "sub53_E2", "sub31_E2", "sub39_E2", "sub07_E2", "sub45_E2", "sub13_E2", "sub24_E2", "sub42_E2", "sub11_E2", "sub25_E2", "sub21_E2", "sub08_E2", "sub01_E2", "sub09_E2", "sub50_E2", "sub22_E2", "sub34_E2", "sub30_E2", "sub37_E2", "sub12_E2", "sub20_E2", "sub17_E2", "sub14_E2", "sub04_E2", "sub05_E2", "sub06_E2", "sub33_E2", "sub35_E2", "sub43_E2", "sub27_E2", "sub28_E2", "sub19_E2", "sub15_E2", "sub26_E2", "sub02_E2", "sub40_E2", "sub18_E2", "sub52_E2", "sub51_E2", "sub36_E2", "sub48_E2", "sub46_E2", "sub03_E2", "sub41_E2", "sub27_E3", "sub34_E3", "sub09_E3", "sub02_E3", "sub30_E3", "sub17_E3", "sub36_E3", "sub22_E3", "sub20_E3", "sub39_E3", "sub03_E3"]

#list_subE1 = ['sub41_E1', 'sub27_E1', 'sub32_E1', 'sub09_E1', 'sub45_E1', 'sub48_E1', 'sub21_E1', 'sub05_E1', 'sub15_E1', 'sub11_E1', 'sub46_E1', 'sub31_E1', 'sub16_E1', 'sub26_E1', 'sub50_E1', 'sub22_E1', 'sub47_E1', 'sub44_E1', 'sub02_E1', 'sub53_E1', 'sub18_E1', 'sub01_E1', 'sub34_E1', 'sub35_E1', 'sub51_E1', 'sub23_E1', 'sub04_E1', 'sub38_E1', 'sub19_E1', 'sub28_E1', 'sub24_E1', 'sub33_E1', 'sub37_E1', 'sub29_E1', 'sub14_E1', 'sub13_E1', 'sub36_E1', 'sub12_E1', 'sub06_E1', 'sub43_E1', 'sub40_E1', 'sub20_E1', 'sub39_E1', 'sub17_E1', 'sub52_E1', 'sub42_E1', 'sub08_E1', 'sub10_E1', 'sub30_E1']
                               
study = elikopy.core.Elikopy(f_path, slurm = True, slurm_email = 'manon.dausort@uclouvain.be', cuda = False)

# study.patientlist_wrapper(registration_atlas, {}, folder_path = f_path, patient_list_m = patient_list, filename = "atlas_registration", function_name = "registration_atlas", slurm = True, slurm_timeout = "00:40:00", cpus = 4, slurm_mem = 1096)

# study.patientlist_wrapper(reg_CC_on_sub, {}, folder_path = f_path, patient_list_m = patient_list, filename = "Corpus_callosum_reg", function_name = "reg_CC_on_sub", slurm = True, slurm_timeout = "00:40:00", cpus = 4, slurm_mem = 1096)

# study.patientlist_wrapper(closing_opening, {}, folder_path = f_path, patient_list_m = patient_list, filename = "opening_closing", function_name = "closing_opening", slurm = True, slurm_timeout = "00:40:00", cpus = 4, slurm_mem = 1096) 

# study.patientlist_wrapper(CC_division, {}, folder_path = f_path, patient_list_m = patient_list, filename = "Corpus_callosum_division", function_name = "CC_division", slurm = True, slurm_timeout = "00:40:00", cpus = 4, slurm_mem = 1096)

# study.patientlist_wrapper(get_fractions, {}, folder_path = f_path, patient_list_m = patient_list, filename = "DMD_before_reg", function_name = "get_fractions", slurm = False, slurm_timeout = "00:40:00", cpus = 4, slurm_mem = 1096)

# study.patientlist_wrapper(f0_f1_to_ftot, {}, folder_path = f_path, patient_list_m = patient_list, filename = "f0_f1_to_ftot", function_name = "f0_f1_to_ftot", slurm = True, slurm_timeout = "00:40:00", cpus = 4, slurm_mem = 1096)

# study.patientlist_wrapper(get_FA_DIAMOND, {}, folder_path = f_path, patient_list_m = patient_list, filename = "FA_DMD", function_name = "get_FA_DIAMOND", slurm = True, slurm_timeout = "00:40:00", cpus = 4, slurm_mem = 1096)

# study.patientlist_wrapper(get_cMetrics, {}, folder_path = f_path, patient_list_m = patient_list, filename = "FA_DMD", function_name = "get_cMetrics", slurm = False, slurm_timeout = "00:40:00", cpus = 4, slurm_mem = 1096)

# If patient_list_m = "sub02_E1" then FA, 
#                   = "sub04_E1" then MD, 
#                   = "sub05_E1" then AD, 
#                   = "sub08_E1" then RD, 
#                   = "sub09_E1" then fbundle,
#                   = "sub11_E1" then fextra, 
#                   = "sub12_E1" then fintra, 
#                   = "sub13_E1" then fiso,
#                   = "sub14_E1" then icvf,
#                   = "sub15_E1" then odi,
#                   = "sub17_E1" then diamond_fractions_ftot,
#                   = "sub19_E1" then diamond_fractions_csf,
#                   = "sub20_E1" then wFA,
#                   = "sub21_E1" then wMD,
#                   = "sub22_E1" then wAD,
#                   = "sub24_E1" then wRD, 
#                   = "sub26_E1" then mf_frac_csf, 
#                   = "sub27_E1" then mf_frac_ftot,
#                   = "sub28_E1" then mf_wfvf,
#                   = "sub30_E1" then mf_fvf_tot"
 
 ###study.patientlist_wrapper(moyenne_par_roi,{}, folder_path = f_path, patient_list_m = patient_list, filename = "moyenne_par_ROI", function_name = "moyenne_par_roi", slurm = True, slurm_timeout = "01:00:00", cpus = 8, slurm_mem = 1096)