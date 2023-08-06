"""
Created on Fri Apr 22 22:35:12 2022

@author: Fauston

"""

import numpy as np 
import pandas as pd 
import xlsxwriter

from tfe22540.atlas_modif_name import get_atlas_list, get_corr_atlas_list
from tfe22540.Stat_test import get_ttest
from tfe22540.perso_path import perso_path_string


perso_path, excel_path, subjects_path, patients_path, plot_path, atlas_path = perso_path_string()   


# =============================================================================
# ANALYSE TTEST
# =============================================================================
def cluster_to_df_t1t2(clusters, file_path, type_matter):
    
    """
        Parameters
        ----------
        clusters : List of list 
            List containing the lists of the different clusters.
        file_path : String 
            File path of the concerned metric.
        type_matter : List of string representing the different matter of the brain 
            For DTI ["wm", "gm", "lobes", "subcorticals", "cerebellum"] and for the rest ["wm", "subcorticals", "cerebellum"].
    
        Returns
        -------
        all_clusters_df_E1 : Dataframe
            Table of a metric for the concerned atlases and the concerned patients (from a specific cluster) and containing their means at E1.
        all_clusters_df_E2 : Dataframe
            Table of a metric for the concerned atlases and the concerned patients (from a specific cluster) and containing their means at E2.
    """
    
    all_clusters_df_E1 = []   
    all_clusters_df_E2 = []    
        
    atlas_list = get_corr_atlas_list(get_atlas_list(onlywhite=False))    
    atlas_name = np.array(atlas_list)
    
    number_wm = atlas_name[atlas_name[:,3] == "1"]
    number_wm = np.append(number_wm, atlas_name[atlas_name[:,3] == "3"], axis = 0)
    number_wm = np.append(number_wm, atlas_name[atlas_name[:,3] == "6"], axis = 0)
    number_wm = number_wm[number_wm[:,0].argsort()]
    
    number_gm = atlas_name[atlas_name[:,3] == "0"]
    number_lobes = atlas_name[atlas_name[:,3] == "5"]
    number_subcortical = atlas_name[atlas_name[:,3] == "2"]
    number_cerebellum = atlas_name[atlas_name[:,3] == "4"]
    
    for cluster in clusters :   
        if (type_matter == "wm"):
            E1_list = np.zeros((number_wm.shape[0], len(cluster)))
            E2_list = np.zeros((number_wm.shape[0], len(cluster)))
            
        elif (type_matter == "gm"):
            E1_list = np.zeros((number_gm.shape[0], len(cluster)))
            E2_list = np.zeros((number_gm.shape[0], len(cluster)))
            
        elif (type_matter == "lobes"):
            E1_list = np.zeros((number_lobes.shape[0], len(cluster)))
            E2_list = np.zeros((number_lobes.shape[0], len(cluster)))
        
        elif (type_matter == "subcortical"):
            E1_list = np.zeros((number_subcortical.shape[0], len(cluster)))
            E2_list = np.zeros((number_subcortical.shape[0], len(cluster)))
            
        elif (type_matter == "cerebellum"):
            E1_list = np.zeros((number_cerebellum.shape[0], len(cluster)))
            E2_list = np.zeros((number_cerebellum.shape[0], len(cluster)))
            
        else: 
            E1_list = np.zeros((len(atlas_list), len(cluster)))
            E2_list = np.zeros((len(atlas_list), len(cluster)))

        for patient_nb,i in zip(cluster, range(len(cluster))):
            worksheet = pd.read_excel(file_path, sheet_name=patient_nb)
            worksheet = worksheet.to_numpy()
            
            if (type_matter == "wm"):
                for k in range(worksheet.shape[0]):
                    for l,m in zip(number_wm[:,0],range(number_wm.shape[0])):
                        if (worksheet[k,0] == l):
                            E1_list[m,i] = worksheet[k,1]
                            E2_list[m,i] = worksheet[k,2]
                            
            elif (type_matter == "gm"):
                for k in range(worksheet.shape[0]):
                    for l,m in zip(number_gm[:,0],range(number_gm.shape[0])):
                        if (worksheet[k,0] == l):
                            E1_list[m,i] = worksheet[k,1]
                            E2_list[m,i] = worksheet[k,2]
                            
            elif (type_matter == "lobes"):
                for k in range(worksheet.shape[0]):
                    for l,m in zip(number_lobes[:,0],range(number_lobes.shape[0])):
                        if (worksheet[k,0] == l):
                            E1_list[m,i] = worksheet[k,1]
                            E2_list[m,i] = worksheet[k,2]
            
            elif (type_matter == "subcortical"):
                for k in range(worksheet.shape[0]):
                    for l,m in zip(number_subcortical[:,0],range(number_subcortical.shape[0])):
                        if (worksheet[k,0] == l):
                            E1_list[m,i] = worksheet[k,1]
                            E2_list[m,i] = worksheet[k,2]
                            
            elif (type_matter == "cerebellum"):
                for k in range(worksheet.shape[0]):
                    for l,m in zip(number_cerebellum[:,0],range(number_cerebellum.shape[0])):
                        if (worksheet[k,0] == l):
                            E1_list[m,i] = worksheet[k,1]
                            E2_list[m,i] = worksheet[k,2]
            else: 
                E1_list[:,i] = worksheet[:,1]
                E2_list[:,i] = worksheet[:,2]
                    
        if (type_matter == "wm"):
            cluster_df_E1 = pd.DataFrame(E1_list, index = number_wm[:,0], columns = cluster)
            cluster_df_E2 = pd.DataFrame(E2_list, index = number_wm[:,0], columns = cluster)
            
        elif (type_matter == "gm"):
            cluster_df_E1 = pd.DataFrame(E1_list, index = number_gm[:,0], columns = cluster)
            cluster_df_E2 = pd.DataFrame(E2_list, index = number_gm[:,0], columns = cluster)
            
        elif (type_matter == "lobes"):
            cluster_df_E1 = pd.DataFrame(E1_list, index = number_lobes[:,0], columns = cluster)
            cluster_df_E2 = pd.DataFrame(E2_list, index = number_lobes[:,0], columns = cluster)
            
        elif (type_matter == "subcortical"):
            cluster_df_E1 = pd.DataFrame(E1_list, index = number_subcortical[:,0], columns = cluster)
            cluster_df_E2 = pd.DataFrame(E2_list, index = number_subcortical[:,0], columns = cluster)
            
        elif (type_matter == "cerebellum"):
            cluster_df_E1 = pd.DataFrame(E1_list, index = number_cerebellum[:,0], columns = cluster)
            cluster_df_E2 = pd.DataFrame(E2_list, index = number_cerebellum[:,0], columns = cluster)
            
        else: 
            cluster_df_E1 = pd.DataFrame(E1_list, index = atlas_name[:,0], columns = cluster)
            cluster_df_E2 = pd.DataFrame(E2_list, index = atlas_name[:,0], columns = cluster)

        all_clusters_df_E1.append(cluster_df_E1) 
        all_clusters_df_E2.append(cluster_df_E2) 
        
    return all_clusters_df_E1, all_clusters_df_E2


def get_results_ttest(metric_name, type_matter, clusters, model):     
   
    """
        Parameters
        ----------
        metric_name : List of strings
            Containing the metric names.
        type_matter : List of strings
            Containing the type of matter to be invesigated.
        clusters : List of string
            List representing the clusters.
        model : String
            Name of the model.
    
        Returns
        -------
        E1_bis_**_increase : List of list of string
            List of several lists containing the atlases showing a significant increase for the concerned cluster. For example, if model = "DTI" and the number of clusters is 3, this list will avec 12 sub lists the 3 first reprensents the significant regions when considering FA metric (one for each cluster), then the next 3 are when considering MD metric and so on. Behind each atlas name there is an array with the same name in string and the mean at E1 of the corresponding cluster. 
        E1_bis_**_decrease : List of list of string
            List of several lists containing the atlases showing a significant decreasing for the concerned cluster. For example, if model = "DTI" and the number of clusters is 3, this list will avec 12 sub lists the 3 first reprensents the significant regions when considering FA metric (one for each cluster), then the next 3 are when considering MD metric and so on. Behind each atlas name there is an array with the same name in string and the mean at E1 of the corresponding cluster. 
        E2_bis_**_increase : List of list of string
            List of several lists containing the atlases showing a significant increase for the concerned cluster. For example, if model = "DTI" and the number of clusters is 3, this list will avec 12 sub lists the 3 first reprensents the significant regions when considering FA metric (one for each cluster), then the next 3 are when considering MD metric and so on. Behind each atlas name there is an array with the same name in string and the mean at E2 of the corresponding cluster. 
        E2_bis_**_decrease : List of list of string
            List of several lists containing the atlases showing a significant decreasing for the concerned cluster. For example, if model = "DTI" and the number of clusters is 3, this list will avec 12 sub lists the 3 first reprensents the significant regions when considering FA metric (one for each cluster), then the next 3 are when considering MD metric and so on. Behind each atlas name there is an array with the same name in string and the mean at E2 of the corresponding cluster. 
        --> ** stands for the different types of matter.
    """
    
    ttest_results_wm_decrease = []
    ttest_results_gm_decrease = []
    ttest_results_lobes_decrease = []
    ttest_results_subcortical_decrease = []
    ttest_results_cerebellum_decrease = []
    ttest_results_wm_increase = []
    ttest_results_gm_increase = []
    ttest_results_lobes_increase = []
    ttest_results_subcortical_increase = []
    ttest_results_cerebellum_increase = []
    signifi1_wm_increase = []
    signifi1_gm_increase = []
    signifi1_lobes_increase = []
    signifi1_subcortical_increase = []
    signifi1_cerebellum_increase = []
    signifi1_wm_decrease = []
    signifi1_gm_decrease = []
    signifi1_lobes_decrease = []
    signifi1_subcortical_decrease = []
    signifi1_cerebellum_decrease = []
    
    E1_bis_wm_increase = []
    E1_bis_gm_increase = []
    E1_bis_lobes_increase = []
    E1_bis_subcortical_increase = []
    E1_bis_cerebellum_increase = []
    E1_bis_wm_decrease = []
    E1_bis_gm_decrease = []
    E1_bis_lobes_decrease = []
    E1_bis_subcortical_decrease = []
    E1_bis_cerebellum_decrease = []
    E2_bis_wm_increase = []
    E2_bis_gm_increase = []
    E2_bis_lobes_increase = []
    E2_bis_subcortical_increase = []
    E2_bis_cerebellum_increase = []
    E2_bis_wm_decrease = []
    E2_bis_gm_decrease = []
    E2_bis_lobes_decrease = []
    E2_bis_subcortical_decrease = []
    E2_bis_cerebellum_decrease = []
               
    for matter in type_matter: 
        if (model == "DTI"):         
            E1_df1, E2_df1 = cluster_to_df_t1t2(clusters, excel_path + "Mean_ROI_FA.xlsx", matter)
            E1_df2, E2_df2 = cluster_to_df_t1t2(clusters, excel_path + "Mean_ROI_MD.xlsx", matter)
            E1_df3, E2_df3 = cluster_to_df_t1t2(clusters, excel_path + "Mean_ROI_AD.xlsx", matter)
            E1_df4, E2_df4 = cluster_to_df_t1t2(clusters, excel_path + "Mean_ROI_RD.xlsx", matter)
            
            all_E1_df = [E1_df1, E1_df2, E1_df3, E1_df4]
            all_E2_df = [E2_df1, E2_df2, E2_df3, E2_df4]
        
        elif (model == "NODDI"):  
            E1_df1, E2_df1 = cluster_to_df_t1t2(clusters, excel_path + "Mean_ROI_noddi_fintra.xlsx", matter)
            E1_df2, E2_df2 = cluster_to_df_t1t2(clusters, excel_path + "Mean_ROI_noddi_fextra.xlsx", matter)
            E1_df3, E2_df3 = cluster_to_df_t1t2(clusters, excel_path + "Mean_ROI_noddi_fiso.xlsx", matter)
            E1_df4, E2_df4 = cluster_to_df_t1t2(clusters, excel_path + "Mean_ROI_noddi_odi.xlsx", matter)
            
            all_E1_df = [E1_df1, E1_df2, E1_df3, E1_df4]
            all_E2_df = [E2_df1, E2_df2, E2_df3, E2_df4]
            
        elif (model == "DIAMOND1"):
            E1_df1, E2_df1 = cluster_to_df_t1t2(clusters, excel_path + "Mean_ROI_wFA.xlsx", matter)
            E1_df2, E2_df2 = cluster_to_df_t1t2(clusters, excel_path + "Mean_ROI_wMD.xlsx", matter)
            E1_df3, E2_df3 = cluster_to_df_t1t2(clusters, excel_path + "Mean_ROI_wAD.xlsx", matter)
            E1_df4, E2_df4 = cluster_to_df_t1t2(clusters, excel_path + "Mean_ROI_wRD.xlsx", matter)
            
            all_E1_df = [E1_df1, E1_df2, E1_df3, E1_df4]
            all_E2_df = [E2_df1, E2_df2, E2_df3, E2_df4]
        
        elif (model == "DIAMOND2"):
            E1_df1, E2_df1 = cluster_to_df_t1t2(clusters, excel_path + "Mean_ROI_diamond_fractions_csf.xlsx", matter)
            E1_df2, E2_df2 = cluster_to_df_t1t2(clusters, excel_path + "Mean_ROI_diamond_fractions_ftot.xlsx", matter)
            
            all_E1_df = [E1_df1, E1_df2]
            all_E2_df = [E2_df1, E2_df2]
        
        elif (model == "DIAMOND"):
            E1_df1, E2_df1 = cluster_to_df_t1t2(clusters, excel_path + "Mean_ROI_wFA.xlsx", matter)
            E1_df2, E2_df2 = cluster_to_df_t1t2(clusters, excel_path + "Mean_ROI_wMD.xlsx", matter)
            E1_df3, E2_df3 = cluster_to_df_t1t2(clusters, excel_path + "Mean_ROI_wAD.xlsx", matter)
            E1_df4, E2_df4 = cluster_to_df_t1t2(clusters, excel_path + "Mean_ROI_wRD.xlsx", matter)
            E1_df5, E2_df5 = cluster_to_df_t1t2(clusters, excel_path + "Mean_ROI_fractions_csf.xlsx", matter)
            E1_df6, E2_df6 = cluster_to_df_t1t2(clusters, excel_path + "Mean_ROI_fractions_ftot.xlsx", matter)
            
            all_E1_df = [E1_df1, E1_df2, E1_df3, E1_df4, E1_df5, E1_df6]
            all_E2_df = [E2_df1, E2_df2, E2_df3, E2_df4, E2_df5, E2_df6]
            
        else: #MF
            E1_df1, E2_df1 = cluster_to_df_t1t2(clusters, excel_path + "Mean_ROI_mf_frac_csf.xlsx", matter)
            E1_df2, E2_df2 = cluster_to_df_t1t2(clusters, excel_path + "Mean_ROI_mf_frac_ftot.xlsx", matter)
            E1_df4, E2_df4 = cluster_to_df_t1t2(clusters, excel_path + "Mean_ROI_mf_fvf_tot.xlsx", matter)
            E1_df5, E2_df5 = cluster_to_df_t1t2(clusters, excel_path + "Mean_ROI_mf_wfvf.xlsx", matter)
            
            all_E1_df = [E1_df1, E1_df2, E1_df4, E1_df5]
            all_E2_df = [E2_df1, E2_df2, E2_df4, E2_df5]
            
        for metric1, metric2, name in zip(all_E1_df, all_E2_df, metric_name): 
            
            for cluster1, cluster2, i in zip(metric1, metric2, range(len(metric1))):
                ttest_results_df_decrease, significant_decrease, E1_bis_decrease, E2_bis_decrease = get_ttest(cluster1, cluster2, "greater")
                ttest_results_df_increase, significant_increase, E1_bis_increase, E2_bis_increase = get_ttest(cluster1, cluster2, "less")
                
                if (matter == "wm"):
                    ttest_results_wm_decrease.append(ttest_results_df_decrease)
                    signifi1_wm_decrease.append(significant_decrease)
                    ttest_results_wm_increase.append(ttest_results_df_increase)
                    signifi1_wm_increase.append(significant_increase)
                    E1_bis_wm_decrease.append(E1_bis_decrease)
                    E1_bis_wm_increase.append(E1_bis_increase)
                    E2_bis_wm_decrease.append(E2_bis_decrease)
                    E2_bis_wm_increase.append(E2_bis_increase)
                
                elif (matter == "lobes"):
                    ttest_results_lobes_decrease.append(ttest_results_df_decrease)
                    signifi1_lobes_decrease.append(significant_decrease)
                    ttest_results_lobes_increase.append(ttest_results_df_increase)
                    signifi1_lobes_increase.append(significant_increase)
                    E1_bis_lobes_decrease.append(E1_bis_decrease)
                    E1_bis_lobes_increase.append(E1_bis_increase)
                    E2_bis_lobes_decrease.append(E2_bis_decrease)
                    E2_bis_lobes_increase.append(E2_bis_increase)
                
                elif (matter == "subcortical"):
                    ttest_results_subcortical_decrease.append(ttest_results_df_decrease)
                    signifi1_subcortical_decrease.append(significant_decrease)
                    ttest_results_subcortical_increase.append(ttest_results_df_increase)
                    signifi1_subcortical_increase.append(significant_increase)
                    E1_bis_subcortical_decrease.append(E1_bis_decrease)
                    E1_bis_subcortical_increase.append(E1_bis_increase)
                    E2_bis_subcortical_decrease.append(E2_bis_decrease)
                    E2_bis_subcortical_increase.append(E2_bis_increase)
                
                elif (matter == "cerebellum"):
                    ttest_results_cerebellum_decrease.append(ttest_results_df_decrease)
                    signifi1_cerebellum_decrease.append(significant_decrease)
                    ttest_results_cerebellum_increase.append(ttest_results_df_increase)
                    signifi1_cerebellum_increase.append(significant_increase)
                    E1_bis_cerebellum_decrease.append(E1_bis_decrease)
                    E1_bis_cerebellum_increase.append(E1_bis_increase)
                    E2_bis_cerebellum_decrease.append(E2_bis_decrease)
                    E2_bis_cerebellum_increase.append(E2_bis_increase)
                
                else:#GM
                    ttest_results_gm_decrease.append(ttest_results_df_decrease)
                    signifi1_gm_decrease.append(significant_decrease)
                    ttest_results_gm_increase.append(ttest_results_df_increase)
                    signifi1_gm_increase.append(significant_increase)
                    E1_bis_gm_decrease.append(E1_bis_decrease)
                    E1_bis_gm_increase.append(E1_bis_increase)
                    E2_bis_gm_decrease.append(E2_bis_decrease)
                    E2_bis_gm_increase.append(E2_bis_increase)
        
    return E1_bis_wm_increase, E1_bis_wm_decrease, E2_bis_wm_increase, E2_bis_wm_decrease, E1_bis_gm_increase, E1_bis_gm_decrease, E2_bis_gm_increase, E2_bis_gm_decrease, E1_bis_lobes_increase, E1_bis_lobes_decrease, E2_bis_lobes_increase, E2_bis_lobes_decrease, E1_bis_subcortical_increase, E1_bis_subcortical_decrease, E2_bis_subcortical_increase, E2_bis_subcortical_decrease, E1_bis_cerebellum_increase, E1_bis_cerebellum_decrease, E2_bis_cerebellum_increase, E2_bis_cerebellum_decrease
    

def get_excel_ttest_DTI(E1_bis_wm_increase, E1_bis_wm_decrease, E2_bis_wm_increase, E2_bis_wm_decrease, E1_bis_gm_increase, E1_bis_gm_decrease, E2_bis_gm_increase, E2_bis_gm_decrease, E1_bis_lobes_increase, E1_bis_lobes_decrease, E2_bis_lobes_increase, E2_bis_lobes_decrease, E1_bis_subcortical_increase, E1_bis_subcortical_decrease, E2_bis_subcortical_increase, E2_bis_subcortical_decrease, E1_bis_cerebellum_increase, E1_bis_cerebellum_decrease, E2_bis_cerebellum_increase, E2_bis_cerebellum_decrease):
    
    """
        Parameters
        ----------
        Outputs of get_results_ttest function.
    
        Returns
        -------
        None. Creation of Excel file for DTI. 

    """
    
    cluster_name = ["Cluster 0", "Cluster 1", "Cluster 2"]
    workbook = xlsxwriter.Workbook(excel_path + "Results_ttest_DTI.xlsx")
    
    for cluster, numero_cluster in zip(cluster_name, range(len(cluster_name))):
        worksheet = workbook.add_worksheet(cluster)
        
        worksheet.write('A2', "White Matter")
        worksheet.write('A3', "FA")
        worksheet.write('D3', "FA")
        
        start_FA_wm = 3
        
        if (len(E1_bis_wm_increase[numero_cluster]) == 0 and len(E1_bis_wm_decrease[numero_cluster]) == 0):
            start_FA_wm = start_FA_wm + 1
            
        md_nb_wm_increase = start_FA_wm + len(E1_bis_wm_increase[numero_cluster])
        md_nb_wm_decrease = start_FA_wm + len(E1_bis_wm_decrease[numero_cluster])
        
        if(md_nb_wm_increase > md_nb_wm_decrease):
            worksheet.write('A' + str(md_nb_wm_increase), "MD")
            worksheet.write('D' + str(md_nb_wm_increase), "MD")
            start_MD_wm = md_nb_wm_increase 
        else:
            worksheet.write('A' + str(md_nb_wm_decrease), "MD")
            worksheet.write('D' + str(md_nb_wm_decrease), "MD")
            start_MD_wm = md_nb_wm_decrease
        
        if (len(E1_bis_wm_increase[numero_cluster + 3*1]) == 0 and len(E1_bis_wm_decrease[numero_cluster + 3*1]) == 0):
            start_MD_wm = start_MD_wm + 1
            
        ad_nb_wm_increase = start_MD_wm + len(E1_bis_wm_increase[numero_cluster + 3*1])
        ad_nb_wm_decrease = start_MD_wm + len(E1_bis_wm_decrease[numero_cluster + 3*1])
        if(ad_nb_wm_increase > ad_nb_wm_decrease):
            worksheet.write('A' + str(ad_nb_wm_increase), "AD")
            worksheet.write('D' + str(ad_nb_wm_increase), "AD")
            start_AD_wm = ad_nb_wm_increase
        else:
            worksheet.write('A' + str(ad_nb_wm_decrease), "AD")
            worksheet.write('D' + str(ad_nb_wm_decrease), "AD")
            start_AD_wm = ad_nb_wm_decrease
            
        if (len(E1_bis_wm_increase[numero_cluster + 3*2]) == 0 and len(E1_bis_wm_decrease[numero_cluster + 3*2]) == 0):
            start_AD_wm = start_AD_wm + 1
        
        rd_nb_wm_increase = start_AD_wm + len(E1_bis_wm_increase[numero_cluster + 3*2])
        rd_nb_wm_decrease = start_AD_wm + len(E1_bis_wm_decrease[numero_cluster + 3*2])
        if(rd_nb_wm_increase > rd_nb_wm_decrease):
            worksheet.write('A' + str(rd_nb_wm_increase), "RD")
            worksheet.write('D' + str(rd_nb_wm_increase), "RD")
            start_RD_wm = rd_nb_wm_increase
        else:
            worksheet.write('A' + str(rd_nb_wm_decrease), "RD")
            worksheet.write('D' + str(rd_nb_wm_decrease), "RD")
            start_RD_wm = rd_nb_wm_decrease
        
        if (len(E1_bis_wm_increase[numero_cluster + 3*3]) > len(E1_bis_wm_decrease[numero_cluster + 3*3])):
            len_RD_wm = len(E1_bis_wm_increase[numero_cluster + 3*3])
        else: 
            len_RD_wm = len(E1_bis_wm_decrease[numero_cluster + 3*3])
        
        # GREY MATTER
        if (len_RD_wm == 0):
            grey_matter_nb = 1 + start_RD_wm + 1
        else:
            grey_matter_nb = 1 + start_RD_wm + len_RD_wm
        
        worksheet.write('A'+ str(grey_matter_nb), "Grey Matter")
        worksheet.write('A' + str(grey_matter_nb + 1), "FA")
        worksheet.write('D' + str(grey_matter_nb + 1), "FA")
        start_FA_gm = grey_matter_nb + 1
        
        if (len(E1_bis_gm_increase[numero_cluster]) == 0 and len(E1_bis_gm_decrease[numero_cluster]) == 0):
            start_FA_gm = start_FA_gm + 1
        
        md_nb_gm_increase = start_FA_gm + len(E1_bis_gm_increase[numero_cluster])
        md_nb_gm_decrease = start_FA_gm + len(E1_bis_gm_decrease[numero_cluster])
        if(md_nb_gm_increase > md_nb_gm_decrease):
            worksheet.write('A' + str(md_nb_gm_increase), "MD")
            worksheet.write('D' + str(md_nb_gm_increase), "MD")
            start_MD_gm = md_nb_gm_increase
        else:
            worksheet.write('A' + str(md_nb_gm_decrease), "MD")
            worksheet.write('D' + str(md_nb_gm_decrease), "MD")
            start_MD_gm = md_nb_gm_decrease
            
        if (len(E1_bis_gm_increase[numero_cluster + 3*1]) == 0 and len(E1_bis_gm_decrease[numero_cluster + 3*1]) == 0):
            start_MD_gm = start_MD_gm + 1
            
        ad_nb_gm_increase = start_MD_gm + len(E1_bis_gm_increase[numero_cluster + 3*1])
        ad_nb_gm_decrease = start_MD_gm + len(E1_bis_gm_decrease[numero_cluster + 3*1])
        if(ad_nb_gm_increase > ad_nb_gm_decrease):
            worksheet.write('A' + str(ad_nb_gm_increase), "AD")
            worksheet.write('D' + str(ad_nb_gm_increase), "AD")
            start_AD_gm = ad_nb_gm_increase
        else:
            worksheet.write('A' + str(ad_nb_gm_decrease), "AD")
            worksheet.write('D' + str(ad_nb_gm_decrease), "AD")
            start_AD_gm = ad_nb_gm_decrease
        
        if (len(E1_bis_gm_increase[numero_cluster + 3*2]) == 0 and len(E1_bis_gm_decrease[numero_cluster + 3*2]) == 0):
            start_AD_gm = start_AD_gm + 1
        
        rd_nb_gm_increase = start_AD_gm + len(E1_bis_gm_increase[numero_cluster + 3*2])
        rd_nb_gm_decrease = start_AD_gm + len(E1_bis_gm_decrease[numero_cluster + 3*2])
        if(rd_nb_gm_increase > rd_nb_gm_decrease):
            worksheet.write('A' + str(rd_nb_gm_increase), "RD")
            worksheet.write('D' + str(rd_nb_gm_increase), "RD")
            start_RD_gm = rd_nb_gm_increase
        else:
            worksheet.write('A' + str(rd_nb_gm_decrease), "RD")
            worksheet.write('D' + str(rd_nb_gm_decrease), "RD")
            start_RD_gm = rd_nb_gm_decrease
        
        if (len(E1_bis_gm_increase[numero_cluster + 3*3]) > len(E1_bis_gm_decrease[numero_cluster + 3*3])):
            len_RD_gm = len(E1_bis_gm_increase[numero_cluster + 3*3])
        else:
            len_RD_gm = len(E1_bis_gm_decrease[numero_cluster + 3*3])
            
        # LOBES
        if (len_RD_gm == 0):
            lobes_nb = 1 + start_RD_gm + 1
        else:
            lobes_nb = 1 + start_RD_gm + len_RD_gm
        
        worksheet.write('A'+ str(lobes_nb), "Lobes")
        worksheet.write('A' + str(lobes_nb + 1), "FA")
        worksheet.write('D' + str(lobes_nb + 1), "FA")
        start_FA_lobes = lobes_nb + 1
        
        if (len(E1_bis_lobes_increase[numero_cluster]) == 0 and len(E1_bis_lobes_decrease[numero_cluster]) == 0):
            start_FA_lobes = start_FA_lobes + 1
        
        md_nb_lobes_increase = start_FA_lobes + len(E1_bis_lobes_increase[numero_cluster])
        md_nb_lobes_decrease = start_FA_lobes + len(E1_bis_lobes_decrease[numero_cluster])
        if(md_nb_lobes_increase > md_nb_lobes_decrease):
            worksheet.write('A' + str(md_nb_lobes_increase), "MD")
            worksheet.write('D' + str(md_nb_lobes_increase), "MD")
            start_MD_lobes = md_nb_lobes_increase
        else:
            worksheet.write('A' + str(md_nb_lobes_decrease), "MD")
            worksheet.write('D' + str(md_nb_lobes_decrease), "MD")
            start_MD_lobes = md_nb_lobes_decrease
        
        if (len(E1_bis_lobes_increase[numero_cluster + 3*1]) == 0 and len(E1_bis_lobes_decrease[numero_cluster + 3*1]) == 0):
            start_MD_lobes = start_MD_lobes + 1
        
        ad_nb_lobes_increase = start_MD_lobes + len(E1_bis_lobes_increase[numero_cluster + 3*1])
        ad_nb_lobes_decrease = start_MD_lobes + len(E1_bis_lobes_decrease[numero_cluster + 3*1])
        if(ad_nb_lobes_increase > ad_nb_lobes_decrease):
            worksheet.write('A' + str(ad_nb_lobes_increase), "AD")
            worksheet.write('D' + str(ad_nb_lobes_increase), "AD")
            start_AD_lobes = ad_nb_lobes_increase
        else:
            worksheet.write('A' + str(ad_nb_lobes_decrease), "AD")
            worksheet.write('D' + str(ad_nb_lobes_decrease), "AD")
            start_AD_lobes = ad_nb_lobes_decrease
        
        if (len(E1_bis_lobes_increase[numero_cluster + 3*2]) == 0 and len(E1_bis_lobes_decrease[numero_cluster + 3*2]) == 0):
            start_AD_lobes = start_AD_lobes + 1
        
        rd_nb_lobes_increase = start_AD_lobes + len(E1_bis_lobes_increase[numero_cluster + 3*2])
        rd_nb_lobes_decrease = start_AD_lobes + len(E1_bis_lobes_decrease[numero_cluster + 3*2])
        if(rd_nb_lobes_increase > rd_nb_lobes_decrease):
            worksheet.write('A' + str(rd_nb_lobes_increase), "RD")
            worksheet.write('D' + str(rd_nb_lobes_increase), "RD")
            start_RD_lobes = rd_nb_lobes_increase
        else:
            worksheet.write('A' + str(rd_nb_lobes_decrease), "RD")
            worksheet.write('D' + str(rd_nb_lobes_decrease), "RD")
            start_RD_lobes = rd_nb_lobes_decrease
        
        if (len(E1_bis_lobes_increase[numero_cluster + 3*3]) > len(E1_bis_lobes_decrease[numero_cluster + 3*3])):
            len_RD_lobes = len(E1_bis_lobes_increase[numero_cluster + 3*3])
        else:
            len_RD_lobes = len(E1_bis_lobes_decrease[numero_cluster + 3*3])
        
        # SUBCORTICAL
        if (len_RD_lobes == 0):
            subcortical_nb = 1 + start_RD_lobes + 1
        else:
            subcortical_nb = 1 + start_RD_lobes + len_RD_lobes
        
        worksheet.write('A'+ str(subcortical_nb), "Subcortical")
        worksheet.write('A' + str(subcortical_nb + 1), "FA")
        worksheet.write('D' + str(subcortical_nb + 1), "FA")
        start_FA_subcortical = subcortical_nb + 1
        
        if (len(E1_bis_subcortical_increase[numero_cluster]) == 0 and len(E1_bis_subcortical_decrease[numero_cluster]) == 0):
            start_FA_subcortical = start_FA_subcortical + 1
        
        md_nb_subcortical_increase = start_FA_subcortical + len(E1_bis_subcortical_increase[numero_cluster])
        md_nb_subcortical_decrease = start_FA_subcortical + len(E1_bis_subcortical_decrease[numero_cluster])
        if(md_nb_subcortical_increase > md_nb_subcortical_decrease):
            worksheet.write('A' + str(md_nb_subcortical_increase), "MD")
            worksheet.write('D' + str(md_nb_subcortical_increase), "MD")
            start_MD_subcortical = md_nb_subcortical_increase
        else:
            worksheet.write('A' + str(md_nb_subcortical_decrease), "MD")
            worksheet.write('D' + str(md_nb_subcortical_decrease), "MD")
            start_MD_subcortical = md_nb_subcortical_decrease
        
        if (len(E1_bis_subcortical_increase[numero_cluster + 3*1]) == 0 and len(E1_bis_subcortical_decrease[numero_cluster + 3*1]) == 0):
            start_MD_subcortical = start_MD_subcortical + 1
        
        ad_nb_subcortical_increase = start_MD_subcortical + len(E1_bis_subcortical_increase[numero_cluster + 3*1])
        ad_nb_subcortical_decrease = start_MD_subcortical + len(E1_bis_subcortical_decrease[numero_cluster + 3*1])
        if(ad_nb_subcortical_increase > ad_nb_subcortical_decrease):
            worksheet.write('A' + str(ad_nb_subcortical_increase), "AD")
            worksheet.write('D' + str(ad_nb_subcortical_increase), "AD")
            start_AD_subcortical = ad_nb_subcortical_increase
        else:
            worksheet.write('A' + str(ad_nb_subcortical_decrease), "AD")
            worksheet.write('D' + str(ad_nb_subcortical_decrease), "AD")
            start_AD_subcortical = ad_nb_subcortical_decrease
        
        if (len(E1_bis_subcortical_increase[numero_cluster + 3*2]) == 0 and len(E1_bis_subcortical_decrease[numero_cluster + 3*2]) == 0):
            start_AD_subcortical = start_AD_subcortical + 1
        
        rd_nb_subcortical_increase = start_AD_subcortical + len(E1_bis_subcortical_increase[numero_cluster + 3*2])
        rd_nb_subcortical_decrease = start_AD_subcortical + len(E1_bis_subcortical_decrease[numero_cluster + 3*2])
        if(rd_nb_subcortical_increase > rd_nb_subcortical_decrease):
            worksheet.write('A' + str(rd_nb_subcortical_increase), "RD")
            worksheet.write('D' + str(rd_nb_subcortical_increase), "RD")
            start_RD_subcortical = rd_nb_subcortical_increase
        else:
            worksheet.write('A' + str(rd_nb_subcortical_decrease), "RD")
            worksheet.write('D' + str(rd_nb_subcortical_decrease), "RD")
            start_RD_subcortical = rd_nb_subcortical_decrease
        
        if (len(E1_bis_subcortical_increase[numero_cluster + 3*3]) > len(E1_bis_subcortical_decrease[numero_cluster + 3*3])):
            len_RD_subcortical = len(E1_bis_subcortical_increase[numero_cluster + 3*3])
        else:
            len_RD_subcortical = len(E1_bis_subcortical_decrease[numero_cluster + 3*3])
        
        # CEREBELLUM
        if (len_RD_subcortical == 0):
            cerebellum_nb = 1 + start_RD_subcortical + 1
        else:
            cerebellum_nb = 1 + start_RD_subcortical + len_RD_subcortical
        
        worksheet.write('A'+ str(cerebellum_nb), "Cerebellum")
        worksheet.write('A' + str(cerebellum_nb + 1), "FA")
        worksheet.write('D' + str(cerebellum_nb + 1), "FA")
        start_FA_cerebellum = cerebellum_nb + 1
        
        if (len(E1_bis_cerebellum_increase[numero_cluster]) == 0 and len(E1_bis_cerebellum_decrease[numero_cluster]) == 0):
            start_FA_cerebellum = start_FA_cerebellum + 1
        
        md_nb_cerebellum_increase = start_FA_cerebellum + len(E1_bis_cerebellum_increase[numero_cluster])
        md_nb_cerebellum_decrease = start_FA_cerebellum + len(E1_bis_cerebellum_decrease[numero_cluster])
        if(md_nb_cerebellum_increase > md_nb_cerebellum_decrease):
            worksheet.write('A' + str(md_nb_cerebellum_increase), "MD")
            worksheet.write('D' + str(md_nb_cerebellum_increase), "MD")
            start_MD_cerebellum = md_nb_cerebellum_increase
        else:
            worksheet.write('A' + str(md_nb_cerebellum_decrease), "MD")
            worksheet.write('D' + str(md_nb_cerebellum_decrease), "MD")
            start_MD_cerebellum = md_nb_cerebellum_decrease
        
        if (len(E1_bis_cerebellum_increase[numero_cluster + 3*1]) == 0 and len(E1_bis_cerebellum_decrease[numero_cluster + 3*1]) == 0):
            start_MD_cerebellum = start_MD_cerebellum + 1
        
        ad_nb_cerebellum_increase = start_MD_cerebellum + len(E1_bis_cerebellum_increase[numero_cluster + 3*1])
        ad_nb_cerebellum_decrease = start_MD_cerebellum + len(E1_bis_cerebellum_decrease[numero_cluster + 3*1])
        if(ad_nb_cerebellum_increase > ad_nb_cerebellum_decrease):
            worksheet.write('A' + str(ad_nb_cerebellum_increase), "AD")
            worksheet.write('D' + str(ad_nb_cerebellum_increase), "AD")
            start_AD_cerebellum = ad_nb_cerebellum_increase
        else:
            worksheet.write('A' + str(ad_nb_cerebellum_decrease), "AD")
            worksheet.write('D' + str(ad_nb_cerebellum_decrease), "AD")
            start_AD_cerebellum = ad_nb_cerebellum_decrease
              
        if (len(E1_bis_cerebellum_increase[numero_cluster + 3*2]) == 0 and len(E1_bis_cerebellum_decrease[numero_cluster + 3*2]) == 0):
            start_AD_cerebellum = start_AD_cerebellum + 1
            
        rd_nb_cerebellum_increase = start_AD_cerebellum + len(E1_bis_cerebellum_increase[numero_cluster + 3*2])
        rd_nb_cerebellum_decrease = start_AD_cerebellum + len(E1_bis_cerebellum_decrease[numero_cluster + 3*2])
        if(rd_nb_cerebellum_increase > rd_nb_cerebellum_decrease):
            worksheet.write('A' + str(rd_nb_cerebellum_increase), "RD")
            worksheet.write('D' + str(rd_nb_cerebellum_increase), "RD")
            start_RD_cerebellum = rd_nb_cerebellum_increase
        else:
            worksheet.write('A' + str(rd_nb_cerebellum_decrease), "RD")
            worksheet.write('D' + str(rd_nb_cerebellum_decrease), "RD")
            start_RD_cerebellum = rd_nb_cerebellum_decrease

        worksheet.write('B1', "Atlas significatifs - Increase")
        worksheet.write('C1', "Percentage Change")
        worksheet.write('E1', "Atlas significatifs - Decrease")
        worksheet.write('F1', "Percentage Change")
        
        start_wm = [start_FA_wm, start_MD_wm, start_AD_wm, start_RD_wm]
        start_gm = [start_FA_gm, start_MD_gm, start_AD_gm, start_RD_gm]
        start_lobes = [start_FA_lobes, start_MD_lobes, start_AD_lobes, start_RD_lobes]
        start_subcortical = [start_FA_subcortical, start_MD_subcortical, start_AD_subcortical, start_RD_subcortical]
        start_cerebellum = [start_FA_cerebellum, start_MD_cerebellum, start_AD_cerebellum, start_RD_cerebellum]

        type_matter = ["wm", "gm", "lobes", "subcortical", "cerebellum"]
        type_metric = [numero_cluster, numero_cluster + 3, numero_cluster + 6, numero_cluster + 9]
        
        for matter in type_matter:
            if matter == "wm":
                for metric,k in zip(type_metric,start_wm):
                    for i,j in zip(range(k, len(E1_bis_wm_increase[metric]) + k), range(len(E1_bis_wm_increase[metric]))):
                        worksheet.write('B' + str(i), E1_bis_wm_increase[metric][j][0])
                        
                        pp = (E2_bis_wm_increase[metric][j][1] - E1_bis_wm_increase[metric][j][1])*100/E1_bis_wm_increase[metric][j][1]
                        pp[np.isnan(pp)==True] = 0
                        pp[np.isinf(pp)==True] = 0
                        percentage_change = np.mean(pp[pp != 0])
                        worksheet.write('C' + str(i), percentage_change)
                    
                    for i,j in zip(range(k, len(E1_bis_wm_decrease[metric]) + k), range(len(E1_bis_wm_decrease[metric]))):
                        worksheet.write('E' + str(i), E1_bis_wm_decrease[metric][j][0])
                        
                        pp = (E2_bis_wm_decrease[metric][j][1] - E1_bis_wm_decrease[metric][j][1])*100/E1_bis_wm_decrease[metric][j][1]
                        pp[np.isnan(pp)==True] = 0
                        pp[np.isinf(pp)==True] = 0
                        percentage_change = np.mean(pp[pp != 0])
                        worksheet.write('F' + str(i), percentage_change)
            
            elif matter == "gm":
                for metric,k in zip(type_metric,start_gm):
                    for i,j in zip(range(k, len(E1_bis_gm_increase[metric]) + k), range(len(E1_bis_gm_increase[metric]))):
                        worksheet.write('B' + str(i), E1_bis_gm_increase[metric][j][0])
                        
                        pp = (E2_bis_gm_increase[metric][j][1] - E1_bis_gm_increase[metric][j][1])*100/E1_bis_gm_increase[metric][j][1]
                        pp[np.isnan(pp)==True] = 0
                        pp[np.isinf(pp)==True] = 0
                        percentage_change = np.mean(pp[pp != 0])
                        worksheet.write('C' + str(i), percentage_change)
                    
                    for i,j in zip(range(k, len(E1_bis_gm_decrease[metric]) + k), range(len(E1_bis_gm_decrease[metric]))):
                        worksheet.write('E' + str(i), E1_bis_gm_decrease[metric][j][0])
                        
                        pp = (E2_bis_gm_decrease[metric][j][1] - E1_bis_gm_decrease[metric][j][1])*100/E1_bis_gm_decrease[metric][j][1]
                        pp[np.isnan(pp)==True] = 0
                        pp[np.isinf(pp)==True] = 0
                        percentage_change = np.mean(pp[pp != 0])
                        worksheet.write('F' + str(i), percentage_change)
                    
            elif matter == "lobes":
                for metric,k in zip(type_metric,start_lobes):
                    for i,j in zip(range(k, len(E1_bis_lobes_increase[metric]) + k), range(len(E1_bis_lobes_increase[metric]))):
                        worksheet.write('B' + str(i), E1_bis_lobes_increase[metric][j][0])
                        
                        pp = (E2_bis_lobes_increase[metric][j][1] - E1_bis_lobes_increase[metric][j][1])*100/E1_bis_lobes_increase[metric][j][1]
                        pp[np.isnan(pp)==True] = 0
                        pp[np.isinf(pp)==True] = 0
                        percentage_change = np.mean(pp[pp != 0])
                        worksheet.write('C' + str(i), percentage_change)
                    
                    for i,j in zip(range(k, len(E1_bis_lobes_decrease[metric]) + k), range(len(E1_bis_lobes_decrease[metric]))):
                        worksheet.write('E' + str(i), E1_bis_lobes_decrease[metric][j][0])
                        
                        pp = (E2_bis_lobes_decrease[metric][j][1] - E1_bis_lobes_decrease[metric][j][1])*100/E1_bis_lobes_decrease[metric][j][1]
                        pp[np.isnan(pp)==True] = 0
                        pp[np.isinf(pp)==True] = 0
                        percentage_change = np.mean(pp[pp != 0])
                        worksheet.write('F' + str(i), percentage_change)
            
            elif matter == "subcortical":
                for metric,k in zip(type_metric,start_subcortical):
                    for i,j in zip(range(k, len(E1_bis_subcortical_increase[metric]) + k), range(len(E1_bis_subcortical_increase[metric]))):
                        worksheet.write('B' + str(i), E1_bis_subcortical_increase[metric][j][0])
                        
                        pp = (E2_bis_subcortical_increase[metric][j][1] - E1_bis_subcortical_increase[metric][j][1])*100/E1_bis_subcortical_increase[metric][j][1]
                        pp[np.isnan(pp)==True] = 0
                        pp[np.isinf(pp)==True] = 0
                        percentage_change = np.mean(pp[pp != 0])
                        worksheet.write('C' + str(i), percentage_change)
                    
                    for i,j in zip(range(k, len(E1_bis_subcortical_decrease[metric]) + k), range(len(E1_bis_subcortical_decrease[metric]))):
                        worksheet.write('E' + str(i), E1_bis_subcortical_decrease[metric][j][0])
                        
                        pp = (E2_bis_subcortical_decrease[metric][j][1] - E1_bis_subcortical_decrease[metric][j][1])*100/E1_bis_subcortical_decrease[metric][j][1]
                        pp[np.isnan(pp)==True] = 0
                        pp[np.isinf(pp)==True] = 0
                        percentage_change = np.mean(pp[pp != 0])
                        worksheet.write('F' + str(i), percentage_change)
            
            else:
                for metric,k in zip(type_metric,start_cerebellum):
                    for i,j in zip(range(k, len(E1_bis_cerebellum_increase[metric]) + k), range(len(E1_bis_cerebellum_increase[metric]))):
                        worksheet.write('B' + str(i), E1_bis_cerebellum_increase[metric][j][0])
                        
                        pp = (E2_bis_cerebellum_increase[metric][j][1] - E1_bis_cerebellum_increase[metric][j][1])*100/E1_bis_cerebellum_increase[metric][j][1]
                        pp[np.isnan(pp)==True] = 0
                        pp[np.isinf(pp)==True] = 0
                        percentage_change = np.mean(pp[pp != 0])
                        worksheet.write('C' + str(i), percentage_change)
                    
                    for i,j in zip(range(k, len(E1_bis_cerebellum_decrease[metric]) + k), range(len(E1_bis_cerebellum_decrease[metric]))):
                        worksheet.write('E' + str(i), E1_bis_cerebellum_decrease[metric][j][0])
                        
                        pp = (E2_bis_cerebellum_decrease[metric][j][1] - E1_bis_cerebellum_decrease[metric][j][1])*100/E1_bis_cerebellum_decrease[metric][j][1]
                        pp[np.isnan(pp)==True] = 0
                        pp[np.isinf(pp)==True] = 0
                        percentage_change = np.mean(pp[pp != 0])
                        worksheet.write('F' + str(i), percentage_change)

    workbook.close()
    
def get_excel_ttest_MULTICOMP(model, E1_bis_wm_increase, E1_bis_wm_decrease, E2_bis_wm_increase, E2_bis_wm_decrease, E1_bis_subcortical_increase, E1_bis_subcortical_decrease, E2_bis_subcortical_increase, E2_bis_subcortical_decrease, E1_bis_cerebellum_increase, E1_bis_cerebellum_decrease, E2_bis_cerebellum_increase, E2_bis_cerebellum_decrease):
    
    """
        Parameters
        ----------
        Outputs of get_results_ttest function.
    
        Returns
        -------
        None. Creation of Excel file for NODDI, DIAMOND and MF. 

    """
    
    cluster_name = ["Cluster 0", "Cluster 1", "Cluster 2"]
    
    workbook = xlsxwriter.Workbook(excel_path + "Results_ttest_" + model + ".xlsx")
    
    if (model == "NODDI"):  
        metrics = ["fintra", "fextra", "fiso", "odi"]
    elif (model == "DIAMOND1"):
        metrics = ["wFA", "wMD", "wAD", "wRD"]
    elif (model == "DIAMOND2"):
        metrics = ["frac_csf", "frac_ftot"]
    elif (model == "DIAMOND"):
        metrics = ["wFA", "wMD", "wAD", "wRD","fractions_csf", "fractions_ftot"]
    else:#MF
        metrics = ["frac_csf", "frac_ftot", "fvf_tot", "wfvf"]
    
    for cluster, numero_cluster in zip(cluster_name, range(len(cluster_name))):
        
        worksheet = workbook.add_worksheet(cluster)
        
        # WHITE MATTER
        worksheet.write('B1', "Atlas significatifs - Increase")
        worksheet.write('C1', "Percentage Change")
        worksheet.write('E1', "Atlas significatifs - Decrease")
        worksheet.write('F1', "Percentage Change")
        
        type_metric = [numero_cluster]
        start_wm = np.array([3])
        
        worksheet.write('A2', "White Matter")
        worksheet.write('A' + str(3), metrics[0])
        worksheet.write('D' + str(3), metrics[0])
        
        for name, indent in zip(metrics[1:], range(len(metrics))):
            
            if (len(E1_bis_wm_increase[numero_cluster + 3*indent]) == 0 and len(E1_bis_wm_decrease[numero_cluster + 3*indent]) == 0):
                start_wm[-1] = start_wm[-1] + 1
            
            nb_wm_increase = start_wm[-1] + len(E1_bis_wm_increase[numero_cluster + 3*indent]) 
            nb_wm_decrease = start_wm[-1] + len(E1_bis_wm_decrease[numero_cluster + 3*indent]) 
            if(nb_wm_increase > nb_wm_decrease):
                worksheet.write('A' + str(nb_wm_increase), name)
                worksheet.write('D' + str(nb_wm_increase), name)
                start_wm = np.append(start_wm, nb_wm_increase)
                
            else:
                worksheet.write('A' + str(nb_wm_decrease), name)
                worksheet.write('D' + str(nb_wm_decrease), name)
                start_wm = np.append(start_wm, nb_wm_decrease)
                
            if(len(E1_bis_wm_increase[numero_cluster + 3*(indent + 1)]) > len(E1_bis_wm_decrease[numero_cluster + 3*(indent + 1)]) ):
                last_wm = len(E1_bis_wm_increase[numero_cluster + 3*(indent + 1)]) 
            else:
                last_wm = len(E1_bis_wm_decrease[numero_cluster + 3*(indent + 1)]) 
        
        # SUBCORTICAL
        if (last_wm == 0):
            subcortical_nb = 1 + start_wm[-1] + 1
        else:
            subcortical_nb = 1 + start_wm[-1] + last_wm
        
        start_subcortical = np.array([subcortical_nb + 1])
        
        worksheet.write('A' + str(subcortical_nb), "Subcortical")
        worksheet.write('A' + str(subcortical_nb + 1), metrics[0])
        worksheet.write('D' + str(subcortical_nb + 1), metrics[0])
        
        for name, indent in zip(metrics[1:], range(len(metrics))):
            
            if (len(E1_bis_subcortical_increase[numero_cluster + 3*indent]) == 0 and len(E1_bis_subcortical_decrease[numero_cluster + 3*indent]) == 0):
                start_subcortical[-1] = start_subcortical[-1] + 1
            
            nb_subcortical_increase = start_subcortical[-1] + len(E1_bis_subcortical_increase[numero_cluster + 3*indent]) 
            nb_subcortical_decrease = start_subcortical[-1] + len(E1_bis_subcortical_decrease[numero_cluster + 3*indent]) 
            
            if(nb_subcortical_increase > nb_subcortical_decrease):
                worksheet.write('A' + str(nb_subcortical_increase), name)
                worksheet.write('D' + str(nb_subcortical_increase), name)
                start_subcortical = np.append(start_subcortical, nb_subcortical_increase)

            else:
                worksheet.write('A' + str(nb_subcortical_decrease), name)
                worksheet.write('D' + str(nb_subcortical_decrease), name)
                start_subcortical = np.append(start_subcortical, nb_subcortical_decrease)
            
            if(len(E1_bis_subcortical_increase[numero_cluster + 3*(indent + 1)]) > len(E1_bis_subcortical_decrease[numero_cluster + 3*(indent + 1)]) ):
                last_subcor = len(E1_bis_subcortical_increase[numero_cluster + 3*(indent + 1)]) 
            else:
                last_subcor = len(E1_bis_subcortical_decrease[numero_cluster + 3*(indent + 1)]) 
        
        # CEREBELLUM
        if (last_subcor ==0):
            cerebellum_nb = 1 + start_subcortical[-1] + 1
        else:
            cerebellum_nb = 1 + start_subcortical[-1] + last_subcor
        
        start_cerebellum = np.array([cerebellum_nb + 1])
        
        worksheet.write('A' + str(cerebellum_nb), "Cerebellum")
        worksheet.write('A' + str(cerebellum_nb + 1), metrics[0])
        worksheet.write('D' + str(cerebellum_nb + 1), metrics[0])
        
        for name, indent in zip(metrics[1:], range(len(metrics))):
            
            if (len(E1_bis_cerebellum_increase[numero_cluster + 3*indent]) == 0 and len(E1_bis_cerebellum_decrease[numero_cluster + 3*indent]) == 0):
                start_cerebellum[-1] = start_cerebellum[-1] + 1
            
            nb_cerebellum_increase = start_cerebellum[-1] + len(E1_bis_cerebellum_increase[numero_cluster + 3*indent]) 
            nb_cerebellum_decrease = start_cerebellum[-1] + len(E1_bis_cerebellum_decrease[numero_cluster + 3*indent]) 
            
            if(nb_cerebellum_increase > nb_cerebellum_decrease):
                worksheet.write('A' + str(nb_cerebellum_increase), name)
                worksheet.write('D' + str(nb_cerebellum_increase), name)
                start_cerebellum = np.append(start_cerebellum, nb_cerebellum_increase)

            else:
                worksheet.write('A' + str(nb_cerebellum_decrease), name)
                worksheet.write('D' + str(nb_cerebellum_decrease), name)
                start_cerebellum = np.append(start_cerebellum, nb_cerebellum_decrease)
            
            type_metric = np.append(type_metric, numero_cluster + 3*(indent + 1))

        type_matter = ["wm", "subcortical", "cerebellum"]
        for matter in type_matter:
            if (matter == "wm"):
                for metric,k in zip(type_metric, start_wm):
                    for i,j in zip(range(k, len(E1_bis_wm_increase[metric]) + k), range(len(E1_bis_wm_increase[metric]))):
                        worksheet.write('B' + str(i), E1_bis_wm_increase[metric][j][0])
                        
                        pp = (E2_bis_wm_increase[metric][j][1] - E1_bis_wm_increase[metric][j][1])*100/E1_bis_wm_increase[metric][j][1]
                        pp[np.isnan(pp)==True]=0
                        pp[np.isinf(pp)==True] = 0
                        percentage_change = np.mean(pp[pp != 0])
                        worksheet.write('C' + str(i), percentage_change)
                    
                    for i,j in zip(range(k, len(E1_bis_wm_decrease[metric]) + k), range(len(E1_bis_wm_decrease[metric]))):
                        worksheet.write('E' + str(i), E1_bis_wm_decrease[metric][j][0])
                        
                        pp = (E2_bis_wm_decrease[metric][j][1] - E1_bis_wm_decrease[metric][j][1])*100/E1_bis_wm_decrease[metric][j][1]
                        pp[np.isnan(pp)==True]=0
                        pp[np.isinf(pp)==True] = 0
                        percentage_change = np.mean(pp[pp != 0])
                        worksheet.write('F' + str(i), percentage_change)
            
            elif (matter == "subcortical"):
                for metric,k in zip(type_metric, start_subcortical):
                    for i,j in zip(range(k, len(E1_bis_subcortical_increase[metric]) + k), range(len(E1_bis_subcortical_increase[metric]))):
                        worksheet.write('B' + str(i), E1_bis_subcortical_increase[metric][j][0])
                        
                        pp = (E2_bis_subcortical_increase[metric][j][1] - E1_bis_subcortical_increase[metric][j][1])*100/E1_bis_subcortical_increase[metric][j][1]
                        pp[np.isnan(pp)==True]=0
                        pp[np.isinf(pp)==True] = 0
                        percentage_change = np.mean(pp[pp != 0])
                        worksheet.write('C' + str(i), percentage_change)
                    
                    for i,j in zip(range(k, len(E1_bis_subcortical_decrease[metric]) + k), range(len(E1_bis_subcortical_decrease[metric]))):
                        worksheet.write('E' + str(i), E1_bis_subcortical_decrease[metric][j][0])
                        
                        pp = (E2_bis_subcortical_decrease[metric][j][1] - E1_bis_subcortical_decrease[metric][j][1])*100/E1_bis_subcortical_decrease[metric][j][1]
                        pp[np.isnan(pp)==True]=0
                        pp[np.isinf(pp)==True] = 0
                        percentage_change = np.mean(pp[pp != 0])
                        worksheet.write('F' + str(i), percentage_change)
                        
            else:   
                for metric, k in zip(type_metric, start_cerebellum):       
                    for i,j in zip(range(k, len(E1_bis_cerebellum_increase[metric]) + k), range(len(E1_bis_cerebellum_increase[metric]))):
                        worksheet.write('B' + str(i), E1_bis_cerebellum_increase[metric][j][0])
                        
                        pp = (E2_bis_cerebellum_increase[metric][j][1] - E1_bis_cerebellum_increase[metric][j][1])*100/E1_bis_cerebellum_increase[metric][j][1]
                        pp[np.isnan(pp)==True]=0
                        pp[np.isinf(pp)==True] = 0
                        percentage_change = np.mean(pp[pp != 0])
                        worksheet.write('C' + str(i), percentage_change)
                        
                    for i,j in zip(range(k, len(E1_bis_cerebellum_decrease[metric]) + k), range(len(E1_bis_cerebellum_decrease[metric]))):
                        worksheet.write('E' + str(i), E1_bis_cerebellum_decrease[metric][j][0])
                        
                        pp = (E2_bis_cerebellum_decrease[metric][j][1] - E1_bis_cerebellum_decrease[metric][j][1])*100/E1_bis_cerebellum_decrease[metric][j][1]
                        pp[np.isnan(pp)==True]=0
                        pp[np.isinf(pp)==True] = 0
                        percentage_change = np.mean(pp[pp != 0])
                        worksheet.write('F' + str(i), percentage_change)

    workbook.close()
