"""
Created on Mon Apr 18 10:23:52 2022

@author: Fauston
"""


import numpy as np
import pandas as pd
import xlsxwriter
from collections import OrderedDict

from tfe22540.perso_path import perso_path_string
from tfe22540.atlas_modif_name import get_corr_atlas_list, get_atlas_list
from tfe22540.plot_functions import histo_hori, histo_multicomp, plot_all_matter

perso_path, excel_path, subjects_path, patients_path, plot_path, atlas_path = perso_path_string() 


def analyse_excel_ttest_DTI(file_path, seuil, display, save):
    
    """
        Parameters
        ----------
        file_path : String 
            File path of the Excel with the results of the t-test for the concerned model, here DTI.
        seuil : Int
            Threshold above which you wish to display the zones.
        display : Boolean
            To show the plot.
        save : Boolean
            To save the plot.
    
        Returns
        -------
        None. 
    """
    
    means_all_FA = []
    names_all_FA = []
    means_all_MD = []
    names_all_MD = []
    means_all_AD = []
    names_all_AD = []
    means_all_RD = []
    names_all_RD = []
    
    colors_all_FA = []
    colors_all_AD = []
    colors_all_MD = []
    colors_all_RD = []
    
    for cluster_nb in range(3):
        worksheet = pd.read_excel(file_path, sheet_name = "Cluster " + str(cluster_nb))
        worksheet = worksheet.to_numpy()
        first_col = worksheet[:,0]
        
        FA_ind = np.where(first_col == "FA")[0]
        MD_ind = np.where(first_col == "MD")[0]
        AD_ind = np.where(first_col == "AD")[0]
        RD_ind = np.where(first_col == "RD")[0]

        gm_ind = np.where(first_col == "Grey Matter")[0][0]
        lobes_ind = np.where(first_col == "Lobes")[0][0]
        subcor_ind = np.where(first_col == "Subcortical")[0][0]
        cereb_ind = np.where(first_col == "Cerebellum")[0][0]
        end_index = [gm_ind, lobes_ind, subcor_ind, cereb_ind, worksheet.shape[0]]
        
        types = ["wm", "gm", "lobes", "subcortical", "cerebellum"]
        
        FA_all_means = []
        MD_all_means = []
        AD_all_means = []
        RD_all_means = []
        
        FA_all_names = []
        MD_all_names = []
        AD_all_names = []
        RD_all_names = []
        
        colors_FA = []
        colors_MD = []
        colors_AD = []
        colors_RD = []
    
        for i,type_matter,end in zip(range(len(FA_ind)), types, end_index):
            # FA
            FA_changes_neg = worksheet[FA_ind[i]:(MD_ind[i]),1:3]
            FA_changes_pos = worksheet[FA_ind[i]:(MD_ind[i]),4:6]
            
            for j in range(FA_changes_neg.shape[0]):                    
                if(np.isnan(FA_changes_neg[j,1]) == True):
                    FA_changes_neg = FA_changes_neg[:j,:]
                    break
            for j in range(FA_changes_pos.shape[0]):                    
                if(np.isnan(FA_changes_pos[j,1]) == True):
                    FA_changes_pos = FA_changes_pos[:j,:]
                    break
                
            FA_changes = np.append(FA_changes_neg,FA_changes_pos,axis=0)
            FA_changes = FA_changes[abs(FA_changes[:,1]) > seuil]
            
            # MD
            MD_changes_neg = worksheet[MD_ind[i]:(AD_ind[i]),1:3]
            MD_changes_pos = worksheet[MD_ind[i]:(AD_ind[i]),4:6]
            
            for j in range(MD_changes_neg.shape[0]):                    
                if(np.isnan(MD_changes_neg[j,1]) == True):
                    MD_changes_neg = MD_changes_neg[:j,:]
                    break
            for j in range(MD_changes_pos.shape[0]):                    
                if(np.isnan(MD_changes_pos[j,1]) == True):
                    MD_changes_pos = MD_changes_pos[:j,:]
                    break
            
            MD_changes = np.append(MD_changes_neg,MD_changes_pos,axis=0)
            MD_changes = MD_changes[abs(MD_changes[:,1]) > seuil]
            
            # AD
            AD_changes_neg = worksheet[AD_ind[i]:(RD_ind[i]),1:3]
            AD_changes_pos = worksheet[AD_ind[i]:(RD_ind[i]),4:6]
            
            for j in range(AD_changes_neg.shape[0]):                    
                if(np.isnan(AD_changes_neg[j,1]) == True):
                    AD_changes_neg = AD_changes_neg[:j,:]
                    break
            for j in range(AD_changes_pos.shape[0]):                    
                if(np.isnan(AD_changes_pos[j,1]) == True):
                    AD_changes_pos = AD_changes_pos[:j,:]
                    break
                
            AD_changes = np.append(AD_changes_neg,AD_changes_pos,axis=0)
            AD_changes = AD_changes[abs(AD_changes[:,1]) > seuil]
                
            # RD
            RD_changes_neg = worksheet[RD_ind[i]:end,1:3]
            RD_changes_pos = worksheet[RD_ind[i]:end,4:6]
            
            for j in range(RD_changes_neg.shape[0]):                    
                if(np.isnan(RD_changes_neg[j,1]) == True):
                    RD_changes_neg = RD_changes_neg[:j,:]
                    break
            for j in range(RD_changes_pos.shape[0]):                    
                if(np.isnan(RD_changes_pos[j,1]) == True):
                    RD_changes_pos = RD_changes_pos[:j,:]
                    break
                        
            RD_changes = np.append(RD_changes_neg,RD_changes_pos,axis=0)
            RD_changes = RD_changes[abs(RD_changes[:,1]) > seuil]
            
            FA_all_means = np.append(FA_all_means, FA_changes[:,1]) 
            MD_all_means = np.append(MD_all_means, MD_changes[:,1])
            AD_all_means = np.append(AD_all_means, AD_changes[:,1])
            RD_all_means = np.append(RD_all_means, RD_changes[:,1])
            
            FA_all_names = np.append(FA_all_names, FA_changes[:,0]) 
            MD_all_names = np.append(MD_all_names, MD_changes[:,0])
            AD_all_names = np.append(AD_all_names, AD_changes[:,0])
            RD_all_names = np.append(RD_all_names, RD_changes[:,0])
            
            if(type_matter == "wm"):
                col = ["coral"]
            elif(type_matter == "gm"):
                col = ["yellowgreen"]
            elif(type_matter == "subcortical"):
                col = ["gold"]
            elif(type_matter == "cerebellum"):
                col = ["dodgerblue"]
            else : 
                col = ["plum"]
            
            colors_FA += int(len(FA_changes[:,1])) * col
            colors_MD += int(len(MD_changes[:,1])) * col
            colors_AD += int(len(AD_changes[:,1])) * col
            colors_RD += int(len(RD_changes[:,1])) * col
            
        if(display == True) :   
            # FA   
            if(len(FA_all_means) > 20):
                FA_means_wm = [FA_all_means[i] for i in range(len(FA_all_means)) if(colors_FA[i]=="coral")]
                FA_names_wm = [FA_all_names[i] for i in range(len(FA_all_names)) if(colors_FA[i]=="coral")]
                FA_means_gm = [FA_all_means[i] for i in range(len(FA_all_means)) if(colors_FA[i]=="yellowgreen")]
                FA_names_gm = [FA_all_names[i] for i in range(len(FA_all_names)) if(colors_FA[i]=="yellowgreen")]
                FA_means_subcor = [FA_all_means[i] for i in range(len(FA_all_means)) if(colors_FA[i]=="gold")]
                FA_names_subcor = [FA_all_names[i] for i in range(len(FA_all_names)) if(colors_FA[i]=="gold")]
                FA_means_cereb = [FA_all_means[i] for i in range(len(FA_all_means)) if(colors_FA[i]=="dodgerblue")]
                FA_names_cereb = [FA_all_names[i] for i in range(len(FA_all_names)) if(colors_FA[i]=="dodgerblue")]
                FA_means_lobes = [FA_all_means[i] for i in range(len(FA_all_means)) if(colors_FA[i]=="plum")]
                FA_names_lobes = [FA_all_names[i] for i in range(len(FA_all_names)) if(colors_FA[i]=="plum")]
                
                
                if(len(FA_means_wm) != 0):
                    histo_hori(FA_means_wm, FA_names_wm, "coral",
                               "[DTI] - Percentage of changes of FA (WM) - Cluster " + str(cluster_nb),
                               "[DTI] - Percentage of changes of FA (WM) - Cluster " + str(cluster_nb), display, save)
                if(len(FA_means_gm) != 0):
                    histo_hori(FA_means_gm, FA_names_gm, "yellowgreen",
                               "[DTI] - Percentage of changes of FA (GM) - Cluster " + str(cluster_nb),
                               "[DTI] - Percentage of changes of FA (GM) - Cluster " + str(cluster_nb), display, save)
                if(len(FA_means_subcor) != 0):
                    histo_hori(FA_means_subcor, FA_names_subcor, "gold",
                               "[DTI] - Percentage of changes of FA (Subcortical) - Cluster " + str(cluster_nb),
                               "[DTI] - Percentage of changes of FA (Subcortical) - Cluster " + str(cluster_nb), display, save)
                if(len(FA_means_cereb) != 0):
                    histo_hori(FA_means_cereb, FA_names_cereb, "dodgerblue",
                               "[DTI] - Percentage of changes of FA (Cerebellum) - Cluster " + str(cluster_nb),
                               "[DTI] - Percentage of changes of FA (Cerebellum) - Cluster " + str(cluster_nb), display, save)
                if(len(FA_means_lobes) != 0):
                    histo_hori(FA_means_lobes, FA_names_lobes, "plum",
                               "[DTI] - Percentage of changes of FA (Lobes) - Cluster " + str(cluster_nb),
                               "[DTI] - Percentage of changes of FA (Lobes) - Cluster " + str(cluster_nb), display, save)
            else: 
                plot_all_matter(FA_all_means, FA_all_names, colors_FA, 
                                "[DTI] - Percentage of changes of FA (All matters) - Cluster " + str(cluster_nb), 
                                "[DTI] - Percentage of changes of FA (All matters) - Cluster " + str(cluster_nb), display, save)

            # MD 
            if(len(MD_all_means) > 20):
                MD_means_wm = [MD_all_means[i] for i in range(len(MD_all_means)) if(colors_MD[i]=="coral")]
                MD_names_wm = [MD_all_names[i] for i in range(len(MD_all_names)) if(colors_MD[i]=="coral")]
                MD_means_gm = [MD_all_means[i] for i in range(len(MD_all_means)) if(colors_MD[i]=="yellowgreen")]
                MD_names_gm = [MD_all_names[i] for i in range(len(MD_all_names)) if(colors_MD[i]=="yellowgreen")]
                MD_means_subcor = [MD_all_means[i] for i in range(len(MD_all_means)) if(colors_MD[i]=="gold")]
                MD_names_subcor = [MD_all_names[i] for i in range(len(MD_all_names)) if(colors_MD[i]=="gold")]
                MD_means_cereb = [MD_all_means[i] for i in range(len(MD_all_means)) if(colors_MD[i]=="dodgerblue")]
                MD_names_cereb = [MD_all_names[i] for i in range(len(MD_all_names)) if(colors_MD[i]=="dodgerblue")]
                MD_means_lobes = [MD_all_means[i] for i in range(len(MD_all_means)) if(colors_MD[i]=="plum")]
                MD_names_lobes = [MD_all_names[i] for i in range(len(MD_all_names)) if(colors_MD[i]=="plum")]
    
                
                if(len(MD_means_wm)!=0):
                    histo_hori(MD_means_wm,MD_names_wm,"coral",
                                "[DTI] - Percentage of changes of MD (WM) - Cluster " + str(cluster_nb),
                                "[DTI] - Percentage of changes of MD (WM) - Cluster " + str(cluster_nb), display, save)
                if(len(MD_means_gm)!=0):
                    histo_hori(MD_means_gm,MD_names_gm,"yellowgreen",
                                "[DTI] - Percentage of changes of MD (GM) - Cluster " + str(cluster_nb),
                                "[DTI] - Percentage of changes of MD (GM) - Cluster " + str(cluster_nb), display, save)
                if(len(MD_means_subcor)!=0):
                    histo_hori(MD_means_subcor,MD_names_subcor,"gold",
                                "[DTI] - Percentage of changes of MD (Subcortical) - Cluster " + str(cluster_nb),
                                "[DTI] - Percentage of changes of MD (Subcortical) - Cluster " + str(cluster_nb), display, save)
                if(len(MD_means_cereb)!=0):
                    histo_hori(MD_means_cereb,MD_names_cereb,"dodgerblue",
                                "[DTI] - Percentage of changes of MD (Cerebellum) - Cluster " + str(cluster_nb),
                                "[DTI] - Percentage of changes of MD (Cerebellum) - Cluster " + str(cluster_nb), display, save)
                if(len(MD_means_lobes)!=0):
                    histo_hori(MD_means_lobes,MD_names_lobes,"plum",
                                "[DTI] - Percentage of changes of MD (Lobes) - Cluster " + str(cluster_nb),
                                "[DTI] - Percentage of changes of MD (Lobes) - Cluster " + str(cluster_nb), display, save)
            else:
                plot_all_matter(MD_all_means, MD_all_names,colors_MD, 
                                "[DTI] - Percentage of changes of MD (All matters) - Cluster " + str(cluster_nb), 
                                "[DTI] - Percentage of changes of MD (All matters) - Cluster " + str(cluster_nb), display, save)
            # AD 
            if(len(AD_all_means) > 20):
                AD_means_wm = [AD_all_means[i] for i in range(len(AD_all_means)) if(colors_AD[i]=="coral")]
                AD_names_wm = [AD_all_names[i] for i in range(len(AD_all_names)) if(colors_AD[i]=="coral")]
                AD_means_gm = [AD_all_means[i] for i in range(len(AD_all_means)) if(colors_AD[i]=="yellowgreen")]
                AD_names_gm = [AD_all_names[i] for i in range(len(AD_all_names)) if(colors_AD[i]=="yellowgreen")]
                AD_means_subcor = [AD_all_means[i] for i in range(len(AD_all_means)) if(colors_AD[i]=="gold")]
                AD_names_subcor = [AD_all_names[i] for i in range(len(AD_all_names)) if(colors_AD[i]=="gold")]
                AD_means_cereb = [AD_all_means[i] for i in range(len(AD_all_means)) if(colors_AD[i]=="dodgerblue")]
                AD_names_cereb = [AD_all_names[i] for i in range(len(AD_all_names)) if(colors_AD[i]=="dodgerblue")]
                AD_means_lobes = [AD_all_means[i] for i in range(len(AD_all_means)) if(colors_AD[i]=="plum")]
                AD_names_lobes = [AD_all_names[i] for i in range(len(AD_all_names)) if(colors_AD[i]=="plum")]
                
                
                if(len(AD_means_wm)!=0):
                    histo_hori(AD_means_wm,AD_names_wm,"coral",
                                "[DTI] - Percentage of changes of AD (WM) - Cluster " + str(cluster_nb),
                                "[DTI] - Percentage of changes of AD (WM) - Cluster " + str(cluster_nb), display, save)
                if(len(AD_means_gm)!=0):
                    histo_hori(AD_means_gm,AD_names_gm,"yellowgreen",
                                "[DTI] - Percentage of changes of AD (GM) - Cluster " + str(cluster_nb),
                                "[DTI] - Percentage of changes of AD (GM) - Cluster " + str(cluster_nb), display, save)
                if(len(AD_means_subcor)!=0):
                    histo_hori(AD_means_subcor,AD_names_subcor,"gold",
                                "[DTI] - Percentage of changes of AD (Subcortical) - Cluster " + str(cluster_nb),
                                "[DTI] - Percentage of changes of AD (Subcortical) - Cluster " + str(cluster_nb), display, save)
                if(len(AD_means_cereb)!=0):
                    histo_hori(AD_means_cereb,AD_names_cereb,"dodgerblue",
                                "[DTI] - Percentage of changes of AD (Cerebellum) - Cluster " + str(cluster_nb),
                                "[DTI] - Percentage of changes of AD (Cerebellum) - Cluster " + str(cluster_nb), display, save)
                if(len(AD_means_lobes)!=0):
                    histo_hori(AD_means_lobes,AD_names_lobes,"plum",
                                "[DTI] - Percentage of changes of AD (Lobes) - Cluster " + str(cluster_nb),
                                "[DTI] - Percentage of changes of AD (Lobes) - Cluster " + str(cluster_nb), display, save)
            else:
                plot_all_matter(AD_all_means, AD_all_names,colors_AD, 
                                "[DTI] - Percentage of changes of AD (All matters) - Cluster " + str(cluster_nb), 
                                "[DTI] - Percentage of changes of AD (All matters) - Cluster " + str(cluster_nb), display, save)           
            # RD 
            if(len(RD_all_means) > 20):
                RD_means_wm = [RD_all_means[i] for i in range(len(RD_all_means)) if(colors_RD[i]=="coral")]
                RD_names_wm = [RD_all_names[i] for i in range(len(RD_all_names)) if(colors_RD[i]=="coral")]
                RD_means_gm = [RD_all_means[i] for i in range(len(RD_all_means)) if(colors_RD[i]=="yellowgreen")]
                RD_names_gm = [RD_all_names[i] for i in range(len(RD_all_names)) if(colors_RD[i]=="yellowgreen")]
                RD_means_subcor = [RD_all_means[i] for i in range(len(RD_all_means)) if(colors_RD[i]=="gold")]
                RD_names_subcor = [RD_all_names[i] for i in range(len(RD_all_names)) if(colors_RD[i]=="gold")]
                RD_means_cereb = [RD_all_means[i] for i in range(len(RD_all_means)) if(colors_RD[i]=="dodgerblue")]
                RD_names_cereb = [RD_all_names[i] for i in range(len(RD_all_names)) if(colors_RD[i]=="dodgerblue")]
                RD_means_lobes = [RD_all_means[i] for i in range(len(RD_all_means)) if(colors_RD[i]=="plum")]
                RD_names_lobes = [RD_all_names[i] for i in range(len(RD_all_names)) if(colors_RD[i]=="plum")]
                
                
                if(len(RD_means_wm)!=0):
                    histo_hori(RD_means_wm,RD_names_wm,"coral",
                                "[DTI] - Percentage of changes of RD (WM) - Cluster " + str(cluster_nb),
                                "[DTI] - Percentage of changes of RD (WM) - Cluster " + str(cluster_nb), display, save)
                if(len(RD_means_gm)!=0):
                    histo_hori(RD_means_gm,RD_names_gm,"yellowgreen",
                                "[DTI] - Percentage of changes of RD (GM) - Cluster " + str(cluster_nb),
                                "[DTI] - Percentage of changes of RD (GM) - Cluster " + str(cluster_nb), display, save)
                if(len(RD_means_subcor)!=0):
                    histo_hori(RD_means_subcor,RD_names_subcor,"gold",
                                "[DTI] - Percentage of changes of RD (Subcortical) - Cluster " + str(cluster_nb),
                                "[DTI] - Percentage of changes of RD (Subcortical) - Cluster " + str(cluster_nb), display, save)
                if(len(RD_means_cereb)!=0):
                    histo_hori(RD_means_cereb,RD_names_cereb,"dodgerblue",
                                "[DTI] - Percentage of changes of RD (Cerebellum) - Cluster " + str(cluster_nb),
                                "[DTI] - Percentage of changes of RD (Cerebellum) - Cluster " + str(cluster_nb), display, save)
                if(len(RD_means_lobes)!=0):
                    histo_hori(RD_means_lobes,RD_names_lobes,"plum",
                                "[DTI] - Percentage of changes of RD (Lobes) - Cluster " + str(cluster_nb),
                                "[DTI] - Percentage of changes of RD (Lobes) - Cluster " + str(cluster_nb), display, save)
            else:
                plot_all_matter(RD_all_means, RD_all_names,colors_RD, 
                                "[DTI] - Percentage of changes of RD (All matters) - Cluster " + str(cluster_nb), 
                                "[DTI] - Percentage of changes of RD (All matters) - Cluster " + str(cluster_nb), display, save)            
        
        means_all_FA.append(FA_all_means)
        names_all_FA.append(FA_all_names)
        colors_all_FA.append(colors_FA)
        means_all_MD.append(MD_all_means)
        names_all_MD.append(MD_all_names)
        colors_all_MD.append(colors_MD)
        means_all_AD.append(AD_all_means)
        names_all_AD.append(AD_all_names)
        colors_all_AD.append(colors_AD)
        means_all_RD.append(RD_all_means)
        names_all_RD.append(RD_all_names)
        colors_all_RD.append(colors_RD)
        
    # return means_all_FA, names_all_FA, means_all_MD, names_all_MD, means_all_AD, names_all_AD, means_all_RD, names_all_RD, colors_all_FA, colors_all_MD, colors_all_AD, colors_all_RD


def analyse_excel_ttest_MULTICOMP(file_path, seuil, model, metric, display, save):
    
    """
        Parameters
        ----------
        file_path : String 
            File path of the Excel with the results of the t-test for the concerned model, here NODDI, DIAMOND or MF.
        seuil : Int
            Threshold above which you wish to display the zones.
        model : String
            Name of the model.
        metric : List of string
            List of the metrics to be displayed.
        display : Boolean
            To show the plot.
        save : Boolean
            To save the plot.
    
        Returns
        -------
        None. 
    """
    
    means_all_wm = []
    names_all_wm = []
    colors_all_wm = []
    
    for cluster_nb in range(3):
        worksheet = pd.read_excel(file_path, sheet_name = "Cluster " + str(cluster_nb))
        worksheet = worksheet.to_numpy()
        first_col = worksheet[:,0]
        
        indexes = []
        for i in metric:
            indexes.append(np.where(first_col == i)[0])
        
        indexes.append(worksheet.shape[0])
        subcor_ind = np.where(first_col == "Subcortical")[0][0]
        cereb_ind = np.where(first_col == "Cerebellum")[0][0]
        end_index = [subcor_ind, cereb_ind,worksheet.shape[0]]
        
        types = ["wm", "subcortical", "cerebellum"]
        
        multicomp_means = []
        multicomp_names = [] 

        for i,type_matter,end in zip(range(len(indexes[0])),types,end_index):
            for k in range(len(metric)):
                if (k != len(metric)-1):
                    changes_neg = worksheet[indexes[k][i]:(indexes[k+1][i]),1:3]
                    changes_pos = worksheet[indexes[k][i]:(indexes[k+1][i]),4:6]
                else:
                    changes_neg = worksheet[indexes[k][i]:(indexes[k+1]),1:3]
                    changes_pos = worksheet[indexes[k][i]:(indexes[k+1]),4:6]
                
                for j in range(changes_neg.shape[0]):                    
                    if(np.isnan(changes_neg[j,1])==True):
                        changes_neg = changes_neg[:j,:]
                        break
                for j in range(changes_pos.shape[0]):                    
                    if(np.isnan(changes_pos[j,1])==True):
                        changes_pos = changes_pos[:j,:]
                        break
                    
                metric_changes = np.append(changes_neg,changes_pos,axis=0)
                metric_changes = metric_changes[abs(metric_changes[:,1])>seuil]

                multicomp_means.append(metric_changes[:,1])
                multicomp_names.append(metric_changes[:,0])
        
        new_means = []
        new_names = []
    
        for p, met in zip(range(int(len(multicomp_means)/3)), metric):
            colors = []
            if (len(multicomp_means[p])!=0 and len(multicomp_means[p+int(len(multicomp_means)/3)])!=0 and len(multicomp_means[p+int(2*len(multicomp_means)/3)])!=0):
                means = np.append(multicomp_means[p], multicomp_means[p+int(len(multicomp_means)/3)])
                means = np.append(means, multicomp_means[p+int(2*len(multicomp_means)/3)])
                names = np.append(multicomp_names[p], multicomp_names[p+int(len(multicomp_names)/3)])
                names = np.append(names, multicomp_names[p+int(2*len(multicomp_names)/3)])
                new_means.append(means)
                new_names.append(names)

                if (len(multicomp_means[p])!=1):
                    colors += int(len(multicomp_means[p])) * ["coral"]                   
                else:
                    colors += 1 * ["coral"]

                if(len(multicomp_means[p+int(len(multicomp_means)/3)])!=1):
                    colors += int(len(multicomp_means[p+int(len(multicomp_means)/3)])) * ["gold"]
                else:
                    colors += 1 * ["gold"]
                
                if(len(multicomp_means[p+int(2*len(multicomp_means)/3)])!=1):
                    colors += int(len(multicomp_means[p+int(2*len(multicomp_means)/3)])) * ["dodgerblue"]
                else:
                    colors += 1 * ["dodgerblue"]

            elif (len(multicomp_means[p+int(len(multicomp_means)/3)])!=0):
                means = multicomp_means[p+int(len(multicomp_means)/3)]
                names = multicomp_names[p+int(len(multicomp_names)/3)]
                new_means.append(means)
                new_names.append(names)

                if(len(multicomp_means[p+int(len(multicomp_means)/3)])!=1):
                    colors += int(len(multicomp_means[p+int(len(multicomp_means)/3)])) * ["gold"]
                else:
                    colors += 1 * ["gold"]
                    
            elif (len(multicomp_means[p+int(2*len(multicomp_means)/3)])!=0):
                means = multicomp_means[p+int(2*len(multicomp_means)/3)]
                names = multicomp_names[p+int(2*len(multicomp_names)/3)]
                new_means.append(means)
                new_names.append(names)

                if(len(multicomp_means[p+int(2*len(multicomp_means)/3)])!=1):
                    colors += int(len(multicomp_means[p+int(2*len(multicomp_means)/3)])) * ["dodgerblue"]
                else:
                    colors += 1 * ["dodgerblue"]

            elif (len(multicomp_means[p])!=0):
                means = multicomp_means[p]
                names = multicomp_names[p]
                new_means.append(means)
                new_names.append(names)
                if (len(multicomp_means[p])!=1):
                    colors += int(len(multicomp_means[p])) * ["coral"]                   
                else:
                    colors += 1 * ["coral"]
            else:
                means = [0]
                names = [0]
                colors = ["coral"]

            if(len(means)>20):
                means_wm = [means[i] for i in range(len(means)) if(colors[i]=="coral")]
                names_wm = [names[i] for i in range(len(names)) if(colors[i]=="coral")]
                means_subcor = [means[i] for i in range(len(means)) if(colors[i]=="gold")]
                names_subcor = [names[i] for i in range(len(names)) if(colors[i]=="gold")]
                means_cereb = [means[i] for i in range(len(means)) if(colors[i]=="dodgerblue")]
                names_cereb = [names[i] for i in range(len(names)) if(colors[i]=="dodgerblue")]
                
                if(len(means_wm)!=0):
                    histo_hori(means_wm, names_wm, "coral",
                               "["+ model +"] - " + "Percentage of changes of "+met+" (WM) - Cluster " + str(cluster_nb),
                               "["+ model +"] - " + "Percentage of changes of "+met+" (WM) - Cluster " + str(cluster_nb), display, save)
                
                if(len(means_subcor)!=0):
                    histo_hori(means_subcor, names_subcor, "gold",
                               "["+ model +"] - " + "Percentage of changes of "+met+" (Subcortical) - Cluster " + str(cluster_nb),
                               "["+ model +"] - " + "Percentage of changes of "+met+" (Subcortical) - Cluster " + str(cluster_nb), display, save)
            
                if(len(means_cereb)!=0):
                    histo_hori(means_cereb, names_cereb, "dodgerblue",
                               "["+ model +"] - " + "Percentage of changes of "+met+" (Cerebellum) - Cluster " + str(cluster_nb),
                               "["+ model +"] - " + "Percentage of changes of "+met+" (Cerebellum) - Cluster " + str(cluster_nb), display, save)
            
            else:
                plot_all_matter(means, names,colors,
                                "["+ model +"] - " + "Percentage of changes of "+met+" (All matters) - Cluster " + str(cluster_nb), 
                                "["+ model +"] - " + "Percentage of changes of "+met+" (All matters) - Cluster " + str(cluster_nb), display, save) 
            
            means_all_wm.append(means)
            names_all_wm.append(names)
            colors_all_wm.append(colors)
            
    # return multicomp_names, means_all_wm, names_all_wm, colors_all_wm
                            
# =============================================================================
# ANALYSE COHERENCE 
# =============================================================================
def coherence(model, type_matter, seuil, file_path):
    
    """
        Parameters
        ----------
        model : String
            Name of the model.
        type_matter : List of string 
            List of the different types of matter.
        seuil : Int
            Threshold above which you wish to display the zones.
        file_path : String 
            File path of the Excel with the results of the t-test for the concerned model, here DTI.
    
        Returns
        -------
        atlas_name_all : List 3 lists of string (one by clusters)
            List of all atlases showing a percentage of change higher in absolute value than the seuil.
    """
    
    cluster_name = ["Cluster 0", "Cluster 1", "Cluster 2"]
    atlas_name_all = []
    
    for cluster, cluster_nb in zip(cluster_name, range(len(cluster_name))):
        worksheet = pd.read_excel(file_path, sheet_name = "Cluster " + str(cluster_nb))    
        worksheet = worksheet.to_numpy()
        matter_col = worksheet[:,0]
        
        if (model == "NODDI"):  
            ind_start = np.where(matter_col=="fintra")[0]
            ind_stop = np.where(matter_col=="odi")[0]
            
        elif (model == "DIAMOND2"):
            ind_start = np.where(matter_col=="frac_csf")[0]
            ind_stop = np.where(matter_col=="frac_ftot")[0]
            
        else:
            ind_start = np.where(matter_col=="frac_csf")[0]
            ind_stop = np.where(matter_col=="fvf_tot")[0]
        
        atlas_col1 = worksheet[:,1] #Increase
        atlas_col2 = worksheet[:,4] #Decrease
        percent_col1 = worksheet[:,2]
        percent_col2 = worksheet[:,5]
        atlas_name_col1 = [str(x) for x in atlas_col1]
        atlas_name_col2 = [str(x) for x in atlas_col2]
        
        atlas_name_col1_bis = []
        for i in range(len(atlas_name_col1)):
            if(abs(percent_col1[i])>seuil):
                atlas_name_col1_bis.append(atlas_name_col1[i])
            else:
                atlas_name_col1_bis.append('nan')
        
        atlas_name_col2_bis = []
        for i in range(len(atlas_name_col2)):
            if(abs(percent_col2[i])>seuil):
                atlas_name_col2_bis.append(atlas_name_col2[i])
            else:
                atlas_name_col2_bis.append('nan')
        
        signif1 = np.append(atlas_name_col1_bis[ind_start[0]:ind_stop[0]], atlas_name_col1_bis[ind_start[1]:ind_stop[1]])
        signif2 = np.append(atlas_name_col2_bis[ind_start[0]:ind_stop[0]], atlas_name_col2_bis[ind_start[1]:ind_stop[1]])
            
        col3 = np.append(signif1,signif2)
        col33 = []
        for name in col3:
            if(name!="nan"):
                col33.append(name)
        col33 = list(OrderedDict.fromkeys(col33))
        atlas_name_all.append(col33)

    return atlas_name_all
                
def coherencebis(fa_or_csf, type_matter, seuil, file_paths):
    
    """
        Parameters
        ----------
        fa_or_csf : String
            To choose the "model" in order to analyse a specific part of the coherence.
        type_matter : List of string 
            List of the different types of matter.
        seuil : Int
            Threshold above which you wish to display the zones.
        file_path : String 
            File path of the Excel with the results of the t-test for the concerned model, here DTI.
    
        Returns
        -------
        atlas_name_all_all : List 3 lists of string (one by clusters)
            List of all atlases showing a percentage of change higher in absolute value than the seuil.
    """
    
    cluster_name = ["Cluster 0", "Cluster 1", "Cluster 2"]
    
    if (fa_or_csf == "FA"):
        metrics = ["FA","odi","wFA"]
        metrics_stop = ["MD","odi","wMD"]
    else:
        metrics = ["fiso","frac_csf","frac_csf"]
        metrics_stop = ["odi","frac_ftot","frac_ftot"]
    
    atlas_name_all_all = []
    
    for cluster, cluster_nb in zip(cluster_name, range(len(cluster_name))):
        atlas_name_all = []
        for path,i in zip(file_paths,range(len(file_paths))):

            worksheet = pd.read_excel(path, sheet_name="Cluster "+str(cluster_nb))
            worksheet = worksheet.to_numpy()
            matter_col = worksheet[:,0]
            
            if (fa_or_csf == "FA"):
                if (i==0):
                    ind_start = np.where(matter_col==metrics[i])[0]
                    ind_stop = np.where(matter_col==metrics_stop[i])[0]
                    ind_start = [ind_start[0], ind_start[-1]]
                    ind_stop = [ind_stop[0], ind_stop[-1]]
                elif (i==2):
                    ind_start = np.where(matter_col==metrics[i])[0]
                    ind_stop = np.where(matter_col==metrics_stop[i])[0]
                else:
                    ind_start = np.where(matter_col=="odi")[0]
                    ind_stop = [np.where(matter_col=="Cerebellum")[0][0]-1,worksheet.shape[0]]
            else:
                ind_start = np.where(matter_col==metrics[i])[0]
                ind_stop = np.where(matter_col==metrics_stop[i])[0]


            atlas_col1 = worksheet[:,1]
            atlas_col2 = worksheet[:,4]
            percent_col1 = worksheet[:,2]
            percent_col2 = worksheet[:,5]
            atlas_name_col1 = [str(x) for x in atlas_col1]
            atlas_name_col2 = [str(x) for x in atlas_col2]
            
            atlas_name_col1_bis = []
            for j in range(len(atlas_name_col1)):
                if(abs(percent_col1[j])>seuil):
                    atlas_name_col1_bis.append(atlas_name_col1[j])
                else:
                    atlas_name_col1_bis.append('nan')
            
            atlas_name_col2_bis = []
            for j in range(len(atlas_name_col2)):
                if(abs(percent_col2[j])>seuil):

                    atlas_name_col2_bis.append(atlas_name_col2[j])
                else:
                    atlas_name_col2_bis.append('nan')
            
            signif1 = np.append(atlas_name_col1_bis[ind_start[0]:ind_stop[0]],atlas_name_col1_bis[ind_start[1]:ind_stop[1]])
            signif2 = np.append(atlas_name_col2_bis[ind_start[0]:ind_stop[0]],atlas_name_col2_bis[ind_start[1]:ind_stop[1]])

            col3 = np.append(signif1,signif2)
            col33 = []
            for name in col3:
                if(name!="nan"):
                    col33.append(name)
            col33 = list(OrderedDict.fromkeys(col33))
            atlas_name_all = np.append(atlas_name_all,col33)
        
        atlas_name_all_all.append(list(atlas_name_all))
             
    return atlas_name_all_all
  
def excel_patient_to_clust(clusters, model):
    
    """
        Parameters
        ----------
        clusters : clusters : List of list 
            List containing the lists of the different clusters.
        model : String
            Name of the model.
    
        Returns
        -------
        None. Creation of an Excel file. 
    """
    
    cluster_names = ["Cluster 0", "Cluster 1", "Cluster 2"]
    path = []
    if (model == "DTI"):         
        path.append(excel_path + "Mean_ROI_FA.xlsx")
        path.append(excel_path + "Mean_ROI_MD.xlsx")
        path.append(excel_path + "Mean_ROI_AD.xlsx")
        path.append(excel_path + "Mean_ROI_RD.xlsx")
    
    elif (model == "NODDI"):  
        path.append(excel_path + "Mean_ROI_noddi_fintra.xlsx")
        path.append(excel_path + "Mean_ROI_noddi_fextra.xlsx")
        path.append(excel_path + "Mean_ROI_noddi_fiso.xlsx")
        path.append(excel_path + "Mean_ROI_noddi_odi.xlsx")

    elif (model == "DIAMOND1"):
        path.append(excel_path + "Mean_ROI_wFA.xlsx")
        path.append(excel_path + "Mean_ROI_wMD.xlsx")
        path.append(excel_path + "Mean_ROI_wAD.xlsx")
        path.append(excel_path + "Mean_ROI_wRD.xlsx")
        
    elif (model == "DIAMOND2"):
        path.append(excel_path + "Mean_ROI_diamond_fractions_csf.xlsx")
        path.append(excel_path + "Mean_ROI_diamond_fractions_ftot.xlsx")
        
    elif (model == "DIAMOND"):
        path.append(excel_path + "Mean_ROI_wFA.xlsx")
        path.append(excel_path + "Mean_ROI_wMD.xlsx")
        path.append(excel_path + "Mean_ROI_wAD.xlsx")
        path.append(excel_path + "Mean_ROI_wRD.xlsx")
        path.append(excel_path + "Mean_ROI_diamond_fractions_csf.xlsx")
        path.append(excel_path + "Mean_ROI_diamond_fractions_ftot.xlsx")
        
    else: #MF
        path.append(excel_path + "Mean_ROI_mf_frac_csf.xlsx")
        path.append(excel_path + "Mean_ROI_mf_frac_ftot.xlsx")
        path.append(excel_path + "Mean_ROI_mf_fvf_tot.xlsx")
        path.append(excel_path + "Mean_ROI_mf_wfvf.xlsx")
    
    for pat in path :
        new_name = pat
        new_name = new_name.replace('Mean_ROI_', 'Cluster_ROI_')
            
        workbook = xlsxwriter.Workbook(new_name)
        for cluster, cluster_name in zip(clusters, cluster_names):
            worksheet_new = workbook.add_worksheet(cluster_name)
            worksheet_new.write('A1', "Atlas")
            worksheet_new.write('B1', "Mean diff")
            worksheet_new.write('C1', "Percentage Change")
            big_sheet_percent = []
            big_sheet = []
            
            for patient,i in zip(cluster,range(len(cluster))):
                worksheet_read = pd.read_excel(pat, sheet_name=patient)
                worksheet_read = worksheet_read.to_numpy()
                if(i==0):
                    for atlas_name,k in zip(worksheet_read[:,0],range(2,len(worksheet_read[:,0])+2)):
                        worksheet_new.write('A'+str(k),atlas_name)
                intermediate_val = np.zeros(len(worksheet_read[:,1]))
                for valeur in range(len(worksheet_read[:,1])):
                    if (worksheet_read[valeur,1] == 0):
                        intermediate_val[valeur] = 0
                    else:
                        intermediate_val[valeur] = (worksheet_read[valeur,2]-worksheet_read[valeur,1])*100/worksheet_read[valeur,1]
                
                big_sheet_percent.append(intermediate_val)
                big_sheet.append((worksheet_read[:,2]-worksheet_read[:,1])*100)
            mean_sheet_percent = np.mean(big_sheet_percent,axis=0)
            mean_sheet_T1 = np.mean(big_sheet,axis=0)
            for mean_percent,mean_T1,l in zip(mean_sheet_percent,mean_sheet_T1,range(2,len(mean_sheet_percent)+2)):
                worksheet_new.write('B'+str(l),mean_T1)              
                worksheet_new.write('C'+str(l),mean_percent)

        workbook.close()
        
def retirer_same(atlas_signif):
    
    """
        Parameters
        ----------
        atlas_signif : List 3 lists of string (one by clusters) --> Resulting of coherencebis function.
            List of all atlases showing a percentage of change higher in absolute value than the seuil.
    
        Returns
        -------
        atlas_signif_corr : List of string
            Corrected list = no more duplicates in the list.
    """
    
    atlas_list = get_corr_atlas_list(get_atlas_list(onlywhite=True))
    atlas_name = np.array(atlas_list[:,0])
    
    atlas_signif_corr = []
    for i in range(len(atlas_signif)):
        if (atlas_signif[i][0] in atlas_name):
            atlas_signif_correct = atlas_signif[i][0]
        else:
            atlas_signif_correct = []
   
        for j in range(1,len(atlas_signif[i])):
            if (atlas_signif[i][j] in atlas_signif_correct):
                j += 1
            else:
                if(atlas_signif[i][j] in atlas_name):
                    atlas_signif_correct = np.append(atlas_signif_correct,atlas_signif[i][j])
        
        atlas_signif_corr.append(atlas_signif_correct)
    
    return atlas_signif_corr

def coherence_plot(model, atlas_signif, labels, percentage, display, save):
    
    """
        Parameters
        ----------
        model : String
            Name of the model.
        atlas_signif : List 3 lists of string (one by clusters) --> Resulting of coherencebis function after correction and of coherence function.
            List of all atlases showing a percentage of change higher in absolute value than the seuil.
        labels : List of string
            Name of the different metrics that appear in the plot.
        percentage : Int
            Threshold of the displayed areas.
        display : Boolean
            To show the plot.
        save : Boolean
            To save the plot.
    
        Returns
        -------
        To be completed.
        gather_metrics_all : TYPE
            DESCRIPTION.
        gather_metrics_diff_all : TYPE
            DESCRIPTION.
        atlas_signifi_all : TYPE
            DESCRIPTION.
    """
    
    path = []
    cluster_names = ["Cluster 0", "Cluster 1", "Cluster 2"]
    gather_metrics_all = []
    gather_metrics_diff_all = []
    atlas_signifi_all = []
    
    if (model == "NODDI"):  
        path.append(excel_path + "Cluster_ROI_noddi_fintra.xlsx")
        path.append(excel_path + "Cluster_ROI_noddi_fextra.xlsx")
        path.append(excel_path + "Cluster_ROI_noddi_fiso.xlsx")
    
    elif (model == "DIAMOND1"):
        path.append(excel_path + "Mean_ROI_wFA.xlsx")
        path.append(excel_path + "Mean_ROI_wMD.xlsx")
        path.append(excel_path + "Mean_ROI_wAD.xlsx")
        path.append(excel_path + "Mean_ROI_wRD.xlsx")
    
    elif (model == "DIAMOND2"):
        path.append(excel_path + "Cluster_ROI_diamond_fractions_csf.xlsx")
        path.append(excel_path + "Cluster_ROI_diamond_fractions_ftot.xlsx")
    
    elif (model == "MF"):
        path.append(excel_path + "Cluster_ROI_mf_frac_csf.xlsx")
        path.append(excel_path + "Cluster_ROI_mf_frac_ftot.xlsx")
    
    elif (model == "CSF"):
        path.append(excel_path + "Cluster_ROI_noddi_fiso.xlsx")
        path.append(excel_path + "Cluster_ROI_diamond_fractions_csf.xlsx")
        path.append(excel_path + "Cluster_ROI_mf_frac_csf.xlsx")
    
    else : 
        path.append(excel_path + "Cluster_ROI_FA.xlsx")
        path.append(excel_path + "Cluster_ROI_noddi_odi.xlsx")
        path.append(excel_path + "Cluster_ROI_wFA.xlsx")
        
    for cluster_name, cluster_num in zip(cluster_names, range(len(cluster_names))):
        if(model == "Combined"):
            if (cluster_num == 1):
                atlas_signifi = np.sort(np.array(atlas_signif[cluster_num]).T)
            else:
                atlas_signifi = np.sort(np.array(atlas_signif[cluster_num]).T)
        else: 
            atlas_signifi = np.sort(np.array(atlas_signif[cluster_num]).T)

        gather_metrics = []
        gather_metrics_diff = []
        
        for pat in path :
            worksheet = pd.read_excel(pat, sheet_name=cluster_name)
            worksheet = worksheet.to_numpy()
            percentage_signif = []
            diff_signif = []
            
            for name,i in zip(worksheet[:,0], range(len(worksheet[:,0]))):
                if (name in atlas_signifi):
                    percentage_signif = np.append(percentage_signif, worksheet[i,2])
                    diff_signif = np.append(diff_signif, worksheet[i,1])
                    
            gather_metrics = np.append(gather_metrics, percentage_signif, axis=0)
            gather_metrics_diff = np.append(gather_metrics_diff, diff_signif, axis=0)
        
        gather_metrics = (np.reshape(gather_metrics, (len(path), len(atlas_signifi)))).T
        gather_metrics_all.append(gather_metrics)
        
        gather_metrics_diff = (np.reshape(gather_metrics_diff, (len(path), len(atlas_signifi)))).T
        gather_metrics_diff_all.append(gather_metrics_diff)
        
        atlas_signifi_all.append(atlas_signifi)
        
        if(percentage==True):
        #GRAPHS PERCENTAGE
            if (gather_metrics.shape[0]>25):
                middle = int(gather_metrics.shape[0]/2)
                gather_metrics1 = gather_metrics[0:middle,:]
                gather_metrics2 = gather_metrics[middle:,:]
                atlas_signifi1 = atlas_signifi[0:middle]
                atlas_signifi2 = atlas_signifi[middle:]
                
                title1 = "["+model+"] - Metrics evolution (Coherence part1) - Cluster " + str(cluster_num)
                namefig1 = "["+model+"] - Metrics evolution (Coherence part1) - Cluster " + str(cluster_num)
                histo_multicomp(gather_metrics1, atlas_signifi1, namefig1, title1, labels, display, save)
                
                title2 = "["+model+"] - Metrics evolution (Coherence part2) - Cluster " + str(cluster_num)
                namefig2 = "["+model+"] - Metrics evolution (Coherence part2) - Cluster " + str(cluster_num)
                histo_multicomp(gather_metrics2, atlas_signifi2, namefig2, title2, labels, display, save)
                
            else:
                title = "["+model+"] - Metrics evolution (Coherence) - Cluster " + str(cluster_num)
                namefig = "["+model+"] - Metrics evolution (Coherence) - Cluster " + str(cluster_num)
                histo_multicomp(gather_metrics, atlas_signifi, namefig, title, labels, display, save)
        else:
        #GRAPHS DIFFERENCE
            if (gather_metrics_diff.shape[0] > 25):
                middle = int(gather_metrics_diff.shape[0]/2)
                gather_metrics1 = gather_metrics_diff[0:middle,:]
                gather_metrics2 = gather_metrics_diff[middle:,:]
                atlas_signifi1 = atlas_signifi[0:middle]
                atlas_signifi2 = atlas_signifi[middle:]
                
                title1 = "["+model+"] - Metrics difference (Coherence part1) - Cluster " + str(cluster_num)
                namefig1 = "["+model+"] - Metrics difference (Coherence part1) - Cluster " + str(cluster_num)
                histo_multicomp(gather_metrics1, atlas_signifi1, namefig1, title1, labels, display, save)
                
                title2 = "["+model+"] - Metrics difference (Coherence part2) - Cluster " + str(cluster_num)
                namefig2 = "["+model+"] - Metrics difference (Coherence part2) - Cluster " + str(cluster_num)
                histo_multicomp(gather_metrics2, atlas_signifi2, namefig2, title2, labels, display, save)
                
            else:
                title = "["+model+"] - Metrics difference (Coherence) - Cluster " + str(cluster_num)
                namefig = "["+model+"] - Metrics difference (Coherence) - Cluster " + str(cluster_num)
                histo_multicomp(gather_metrics_diff, atlas_signifi, namefig, title, labels, display, save)
    
    return gather_metrics_all,gather_metrics_diff_all,atlas_signifi_all
        
# =============================================================================
# APPEL FCT
# =============================================================================

# =============================================================================
# RESULTS OF CLUSTERING
# =============================================================================
cluster0 = ['05','26','35','36','37','40','41']
cluster1 = ['02', '04', '08', '09', '11', '12', '14', '15', '18', '20', '21', '22', '24', '27', '28', '30', '34', '39', '42', '45']
cluster2 = ['13', '17', '19', '31', '32', '33', '43', '46']        
clusters = [cluster0, cluster1, cluster2]

# =============================================================================
# CLUSTER EXCEL FILES (TO RUN ONE TIME)
# =============================================================================
excel_patient_to_clust(clusters, "DTI")
excel_patient_to_clust(clusters, "NODDI")
excel_patient_to_clust(clusters, "DIAMOND")
excel_patient_to_clust(clusters, "MF")

# =============================================================================
# INDIVIDUAL METRIC PLOTS 
# =============================================================================
analyse_excel_ttest_DTI(excel_path + "Results_ttest_DTI.xlsx", 8, True, True)
analyse_excel_ttest_MULTICOMP(excel_path + "Results_ttest_NODDI.xlsx", 8, "NODDI", ["fintra", "fextra","fiso","odi"], True, True)
analyse_excel_ttest_MULTICOMP(excel_path + "Results_ttest_DIAMOND1.xlsx", 8, "DIAMOND1", ["wFA", "wMD","wAD","wRD"], True, True)
analyse_excel_ttest_MULTICOMP(excel_path + "Results_ttest_DIAMOND2.xlsx", 8, "DIAMOND2", ["frac_csf", "frac_ftot"], True, True)
analyse_excel_ttest_MULTICOMP(excel_path + "Results_ttest_MF.xlsx", 8, "MF", ["frac_csf", "frac_ftot", "fvf_tot", "wfvf"], True, True)

# =============================================================================
# THE COHERENCE OF EACH MODEL SEPARATELY
# =============================================================================
atlas_name_NODDI = coherence("NODDI", ["White Matter", "Subcortical", "Cerebellum"], 8, excel_path + "Results_ttest_NODDI.xlsx") 
atlas_name_DIAMOND2 = coherence("DIAMOND2", ["White Matter", "Subcortical", "Cerebellum"], 8, excel_path + "Results_ttest_DIAMOND2.xlsx") 
atlas_name_MF = coherence("MF", ["White Matter", "Subcortical", "Cerebellum"], 8, excel_path + "Results_ttest_MF.xlsx") 

# PERCENTAGE
gather_metrics_NODDI, gather_metrics_diff_NODDI, atlas_signifi_NODDI = coherence_plot("NODDI", atlas_name_NODDI, ["fintra", "fextra", "fiso","odi"], True, True, False)            
gather_metrics_DIAMOND2, gather_metrics_diff_DIAMOND2, atlas_signifi_DIAMOND2 = coherence_plot("DIAMOND2", atlas_name_DIAMOND2, ["fraction_csf", "fraction_ftot"], True, True, False)            
gather_metrics_MF, gather_metrics_diff_MF, atlas_signifi_MF = coherence_plot("MF", atlas_name_MF, ["fraction_csf", "fraction_ftot"], True, True, False)         

# DIFFERENCE
gather_metrics_NODDI, gather_metrics_diff_NODDI,atlas_signifi_NODDI = coherence_plot("NODDI", atlas_name_NODDI, ["fintra", "fextra", "fiso","odi"], False, True, False)            
gather_metrics_DIAMOND2, gather_metrics_diff_DIAMOND2, atlas_signifi_DIAMOND2 = coherence_plot("DIAMOND2", atlas_name_DIAMOND2, ["frac_csf", "frac_ftot"], False, True, False)            
gather_metrics_MF, gather_metrics_diff_MF, atlas_signifi_MF = coherence_plot("MF", atlas_name_MF, ["frac_csf", "frac_ftot"], False, True, False)  

# =============================================================================
# COHERENCE COMBINED OF THE MODELS
# =============================================================================
# FA, wFA, ODI
atlas_name_all_fa_odi_cfa = coherencebis("FA", ["White Matter", "Subcortical", "Cerebellum"], 8, [excel_path + "Results_ttest_DTI.xlsx", excel_path + "Results_ttest_NODDI.xlsx",excel_path + "Results_ttest_DIAMOND1.xlsx"])
atlas_signif_corr = retirer_same(atlas_name_all_fa_odi_cfa)
gather_metrics_FAcFAodi, gather_metrics_diff_FAcFAodi, atlas_signifi_FAcFAodi = coherence_plot("Combined", atlas_signif_corr, ["FA","odi","wFA"], False, True, True) 

# FRACTION OF CSF
atlas_name_all_CSF = coherencebis("CSF", ["White Matter", "Subcortical", "Cerebellum"], 8, [excel_path + "Results_ttest_NODDI.xlsx", excel_path + "Results_ttest_DIAMOND2.xlsx", excel_path + "Results_ttest_MF.xlsx"])
atlas_signif_corr_CSF = retirer_same(atlas_name_all_CSF)
gather_metrics_CSF, gather_metrics_diff_CSF, atlas_signifi_CSF = coherence_plot("CSF", atlas_signif_corr_CSF, ["fiso","frac_csf (DIAMOND)","frac_csf (MF)"], False, True ,False) 

# VERIFICATION THANKS TO NUMBERS
cluster1_NODDI = np.zeros(gather_metrics_diff_NODDI[1].shape[0])
for i in range(gather_metrics_diff_NODDI[1].shape[0]):
    cluster1_NODDI[i] = gather_metrics_diff_NODDI[1][i,0] + gather_metrics_diff_NODDI[1][i,1] + gather_metrics_diff_NODDI[1][i,2]

mean_cluster1_NODDI = np.mean(cluster1_NODDI)*100
print("Sum of the differences bewteen fractions (error) considering Cluster 1 =", mean_cluster1_NODDI)

cluster2_NODDI = np.zeros(gather_metrics_diff_NODDI[2].shape[0])
for i in range(gather_metrics_diff_NODDI[2].shape[0]):
    cluster2_NODDI[i] = gather_metrics_diff_NODDI[2][i,0] + gather_metrics_diff_NODDI[2][i,1] + gather_metrics_diff_NODDI[2][i,2]

mean_cluster2_NODDI = np.mean(cluster2_NODDI)*100
print("Sum of the differences bewteen fractions (error) considering Cluster 2 =", mean_cluster2_NODDI)
