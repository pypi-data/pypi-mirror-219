import xlsxwriter
import nibabel as nib
import os
import numpy as np
import math
from itertools import repeat
from multiprocessing import Pool, freeze_support

from tfe22540.perso_path import perso_path_string
from tfe22540.atlas_modif_name import get_corr_atlas_list, get_atlas_list

def genWorkbook(metric_name, metric_data, folder_path, post_proc_folder, excel_path):

    patient_list = ["sub41_E1", "sub27_E1", "sub32_E1", "sub09_E1", "sub45_E1", "sub48_E1", "sub21_E1", "sub05_E1", "sub15_E1", "sub11_E1", "sub46_E1", "sub31_E1", "sub16_E1", "sub26_E1", "sub50_E1", "sub22_E1", "sub47_E1", "sub44_E1", "sub02_E1", "sub53_E1", "sub18_E1", "sub01_E1", "sub34_E1", "sub35_E1", "sub51_E1", "sub23_E1", "sub04_E1", "sub38_E1", "sub19_E1", "sub28_E1", "sub24_E1", "sub33_E1", "sub37_E1", "sub29_E1", "sub14_E1", "sub13_E1", "sub36_E1", "sub12_E1", "sub43_E1", "sub40_E1", "sub20_E1", "sub39_E1", "sub17_E1", "sub52_E1", "sub42_E1", "sub08_E1", "sub10_E1", "sub30_E1", "sub32_E2", "sub29_E2", "sub53_E2", "sub31_E2", "sub39_E2", "sub07_E2", "sub45_E2", "sub13_E2", "sub24_E2", "sub42_E2", "sub11_E2", "sub25_E2", "sub21_E2", "sub08_E2", "sub01_E2", "sub09_E2", "sub50_E2", "sub22_E2", "sub34_E2", "sub30_E2", "sub37_E2", "sub12_E2", "sub20_E2", "sub17_E2", "sub14_E2", "sub04_E2", "sub05_E2", "sub06_E2", "sub33_E2", "sub35_E2", "sub43_E2", "sub27_E2", "sub28_E2", "sub19_E2", "sub15_E2", "sub26_E2", "sub02_E2", "sub40_E2", "sub18_E2", "sub52_E2", "sub51_E2", "sub36_E2", "sub48_E2", "sub46_E2", "sub03_E2", "sub41_E2", "sub27_E3", "sub34_E3", "sub09_E3", "sub02_E3", "sub30_E3", "sub17_E3", "sub36_E3", "sub22_E3", "sub20_E3", "sub03_E3"]
    patient_list = np.sort(patient_list)
         
    workbook = xlsxwriter.Workbook(excel_path + 'Mean_ROI_' + metric_name + '.xlsx')
    worksheets = {}
    atlas_list = get_atlas_list(onlywhite = metric_data[1])
    atlas_list_name = get_corr_atlas_list(atlas_list)

    print("Excel generation for metric ", metric_name)
    for p in patient_list:

        p_name = p[:-3]
        p_time_point = p[-1]
        p_id = p[3:-3]

        if p_id in worksheets.keys():
            curr_worksheet = worksheets[p_id]
        else:
            curr_worksheet = workbook.add_worksheet(p_id)
            worksheets[p_id] = curr_worksheet

        brain_mask = nib.load(os.path.join(folder_path, "subjects",p,"masks", p + "_brain_mask.nii.gz")).get_fdata()
        brain_mask[:, :, 0] = 0
        brain_mask[:, :, -1] = 0

        wm_mask = nib.load(os.path.join(folder_path, "subjects",p,"masks", p + "_wm_mask_FSL_T1.nii.gz")).get_fdata()
        wm_mask[:, :, 0] = 0
        wm_mask[:, :, -1] = 0
        
        patient_data = nib.load(os.path.join(folder_path, "subjects", p, "dMRI", "microstructure", metric_data[2], p + metric_data[0] + ".nii.gz")).get_fdata()
        patient_data[np.isnan(patient_data) == True] = 0.0

        rowsel = 2

        for atlas_path in atlas_list_name:
            atlas_name = str(atlas_path[1])
            if ('.nii.gz' in atlas_name):
                atlas_name = atlas_name.replace('.nii.gz','')

            atlas_data= nib.load(
                post_proc_folder  + "/#" + p_name.replace('sub','') + "/Atlas/" + atlas_name + "_reg_on_" + p + ".nii.gz").get_fdata()

            mask_zone = np.zeros(patient_data.shape)
            mask_zone[atlas_data > float(atlas_path[2])] = 1

            if (atlas_path[3] == "0" or atlas_path[3] == "2" or atlas_path[3] == "4" or atlas_path[3] == "5" or
                    atlas_path[3] == "6"):
                mask_zone = mask_zone * brain_mask
            elif (atlas_path[3] == "1" or atlas_path[3] == "3"):  # WHITE MATTER
                mask_zone = mask_zone * wm_mask
            else:
                print('Not ok again')
            
            mask_zone[patient_data == 0] = 0

            interm = patient_data * mask_zone
            moyenne = np.mean(interm[interm != 0])

            if (math.isnan(moyenne) == True or math.isnan(moyenne) == True):
                moyenne = 0

            curr_worksheet.write('A1', "Atlas names")
            curr_worksheet.write('B1', "Mean at E1")
            curr_worksheet.write('C1', "Mean at E2")
            curr_worksheet.write('D1', "Mean at E3")
            curr_worksheet.write('E1', "Percentage change bewteen E2 and E1")
            curr_worksheet.write('F1', "Percentage change bewteen E3 and E1")
            curr_worksheet.write('G1', "Percentage change bewteen E3 and E2")
            
            curr_worksheet.write('A' + str(rowsel), atlas_path[0])
            if p_time_point == "1":
                curr_worksheet.write('B' + str(rowsel), moyenne)
            elif p_time_point == "2":
                curr_worksheet.write('C' + str(rowsel), moyenne)
            elif p_time_point == "3":
                curr_worksheet.write('D' + str(rowsel), moyenne)

            curr_worksheet.write_formula('E' + str(rowsel),
                                         '= (C' + str(rowsel) + '-B' + str(rowsel) + ') * 100/B' + str(rowsel))
            curr_worksheet.write_formula('F' + str(rowsel),
                                         '= (D' + str(rowsel) + '-C' + str(rowsel) + ') * 100/C' + str(rowsel))
            curr_worksheet.write_formula('G' + str(rowsel),
                                         '= (D' + str(rowsel) + '-B' + str(rowsel) + ') * 100/B' + str(rowsel))

            rowsel += 1
        print("patient ", p, " processed for metric ", metric_name)


    workbook.close()
    print("Succesfully processed all patient for metric", metric_name)
    
    return metric_name

if __name__ == '__main__':
    metrics = {'FA':["_FA",False, "dti"], 'MD':["_MD",False, "dti"], 'AD':["_AD",False, "dti"], 'RD':["_RD",False, "dti"],
               'noddi_fbundle':["_noddi_fbundle",True, "noddi"], 'noddi_fextra':["_noddi_fextra",True, "noddi"], 'noddi_fintra':["_noddi_fintra",True, "noddi"], 'noddi_fiso':["_noddi_fiso",True, "noddi"], 'noddi_icvf':["_noddi_icvf",True, "noddi"], 'noddi_odi':["_noddi_odi",True, "noddi"],
               'diamond_fractions_ftot':["_diamond_fractions_ftot",True, "diamond"], 'diamond_fractions_csf':["_diamond_fractions_csf",True, "diamond"], 'wFA':["_wFA",True, "diamond"], 'wMD':["_wMD",True, "diamond"], 'wAD':["_wAD",True, "diamond"], 'wRD':["_wRD",True, "diamond"],
               'mf_frac_csf':["_mf_frac_csf",True, "mf"], 'mf_frac_ftot':["_mf_frac_ftot",True, "mf"], 'mf_wfvf':["_mf_wfvf",True, "mf"], 'mf_fvf_tot':["_mf_fvf_tot",True, "mf"]}

    perso_path, excel_path, subjects_path, patients_path, plot_path, atlas_path = perso_path_string() 
    
    post_proc_folder = patients_path
    excel_path = excel_path
    patient_list = []

    print("Atlas mask generation...")
    
    for p in patient_list:
        atlas_list = get_atlas_list(onlywhite = False)
        atlas_list_name = get_corr_atlas_list(atlas_list)
        
        brain_mask = nib.load(os.path.join(subjects_path + p, "masks", p + "_brain_mask.nii.gz")).get_fdata()
        brain_mask[:, :, 0] = 0
        brain_mask[:, :, -1] = 0

        wm_mask = nib.load(os.path.join(subjects_path + p, "masks", p + "_wm_mask_FSL_T1.nii.gz")).get_fdata()
        wm_mask[:, :, 0] = 0
        wm_mask[:, :, -1] = 0

        p_name = p[:-3]
        p_time_point = p[-1]
        
        img = nib.load(os.path.join(subjects_path + p, "dMRI", "microstructure", "dti", p + "_FA.nii.gz"))
                                             
        img_data = img.get_fdata()

        img_data[np.isnan(img_data) == True] = 0.0
        
        for atlas_path in atlas_list_name:
            atlas_name = str(atlas_path[1])
            if ('.nii.gz' in atlas_name):
                atlas_name = atlas_name.replace('.nii.gz', '')

            atlas_name1 = str(atlas_path[1])
            if ('.nii.gz' in atlas_name1):
                atlas_name1 = atlas_name1.replace('.nii.gz', '')
            if ("Cerebellar/" in atlas_name1):
                atlas_name1 = atlas_name1.replace('Cerebellar/', '')
            if ("Cerebelar" in atlas_name1):
                atlas_name1 = atlas_name1.replace('Cerebelar', 'Cerebellar')
            if ("Cerebellum/" in atlas_name1):
                atlas_name1 = atlas_name1.replace('Cerebellum/', '')
            if ("Harvard/" in atlas_name1):
                atlas_name1 = atlas_name1.replace('Harvard/', '')
            if ("Harvard_cortex/" in atlas_name1):
                atlas_name1 = atlas_name1.replace('Harvard_cortex/', '')
            if ("Lobes/" in atlas_name1):
                atlas_name1 = atlas_name1.replace('Lobes/', '')
            if ("XTRACT/" in atlas_name1):
                atlas_name1 = atlas_name1.replace('XTRACT/', '')
            if ("CC/" in atlas_name1):
                atlas_name1 = atlas_name1.replace('CC/', '')

            atlas_data = nib.load(
                post_proc_folder + "/#" + p_name.replace('sub','') + "/Atlas/" + atlas_name + "_reg_on_" + p + ".nii.gz").get_fdata()

            mask_zone = np.zeros(img_data.shape)
            mask_zone[atlas_data > float(atlas_path[2])] = 1

            if (atlas_path[3] == "0" or atlas_path[3] == "2" or atlas_path[3] == "4" or atlas_path[3] == "5" or
                    atlas_path[3] == "6"):
                mask_zone = mask_zone * brain_mask
            elif (atlas_path[3] == "1" or atlas_path[3] == "3"):  # WHITE MATTER
                mask_zone = mask_zone * wm_mask
            else:
                print('Not ok again')
            mask_zone[img_data == 0] = 0

            out = nib.Nifti1Image(mask_zone, affine=img.affine, header=img.header)
            out.to_filename(post_proc_folder  + "/#" + p_name.replace('sub','') + "/Mask/" + p_name + "_" + atlas_name1 + "_mask_E" + p_time_point + ".nii.gz")
            
        print("patient ", p, " processed.")

    print("Excel generation...")
    multithreading = True
    
    # Create workbook and add worksheets
    if multithreading:
        res = []
        metric_name = list(metrics.keys())
        metric_data = list(metrics.values())
        
        with Pool(processes=4) as pool:
            res = pool.starmap(genWorkbook, zip(metric_name,metric_data, repeat(perso_path + "alcoholic_study/"), repeat(post_proc_folder), repeat(excel_path)))   
        print(res)
    else:
        for metric_name, metric_data in metrics.items():
            genWorkbook(metric_name,metric_data, perso_path + "alcoholic_study/", post_proc_folder, excel_path)
        
        
