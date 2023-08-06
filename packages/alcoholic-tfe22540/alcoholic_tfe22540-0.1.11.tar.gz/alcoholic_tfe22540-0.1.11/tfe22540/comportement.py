# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 21:32:05 2022

@author: manou
"""

import seaborn as sns
import pandas as pd
import numpy as np
import xlsxwriter
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

from tfe22540.perso_path import perso_path_string, patient_number_list


perso_path, excel_path, subjects_path, patients_path, plot_path, atlas_path = perso_path_string() 


def get_comportements(file_path, patient_list):
    
    """
    Parameters
    ----------
    file_path : File path in string
        Excel file containing General_data or behavioural data (provided by Melissa).
    patient_list : List of strings

    Returns
    -------
    patients_all : List of tuples
        List containing as many tuples as patients, each summarizing the important behavioural informations. 
    """
    
    worksheet = pd.read_excel(file_path)
    tabular = worksheet.to_numpy()
    patients_all = []
    
    for i in patient_list:
        for j in range(len(worksheet["Numéro"])):
            if (i == worksheet["Numéro"][j]):
                patients_all.append(tabular[j,:])
    
    return patients_all
    
patient_number = patient_number_list("int_nb")
patients_all = get_comportements(excel_path + "Comportements_data.xlsx", patient_number)

def comportement_to_excel(patients_all, only_percentage):
    
    """
    Parameters
    ----------
    patients_all : List returned by get_comportements() function

    Returns
    -------
    None. Excel file summarizing information contained in patients_all. 
    """
    
    if (only_percentage == False):
        workbook = xlsxwriter.Workbook(excel_path + 'Behavioural_data.xlsx')
    else:
        workbook = xlsxwriter.Workbook(excel_path + 'Behavioural_data_only_percentage.xlsx')
      
    patient_data = patients_all.copy()
    
    for i in patient_data:
        if(i[0] == 2 or i[0] == 4 or i[0] == 5 or i[0] == 8 or i[0] == 9):
            worksheet = workbook.add_worksheet("0"+str(int(i[0])))
        else:
            worksheet = workbook.add_worksheet(str(int(i[0])))
        
        if (only_percentage == False):
            list_data = ["Unités", "Osmolalité", "T1_BDI", "T1_OCDS_MODIFIE_Total", "T1_OCDS_Obsessions", "T1_OCDS_Compulsions", "T1_STAI_YA", "T1_MFI", 
                         "T2_Bearni", "T2_BDI", "T2_OCDS_MODIFIE_Total", "T2_OCDS_Obsessions", "T2_OCDS_Compulsions", "T2_STAI_YA", "T2_MFI", 
                         "Percentage BDI", "Percentage OCDS_MODIFIE_Total", "Percentage OCDS_Obsessions", "Percentage OCDS_Compulsions", "Percentage STAI_YA", "Percentage MFI"]
        else:
            list_data = ["Percentage BDI", "Percentage OCDS_MODIFIE_Total", "Percentage OCDS_Obsessions", "Percentage OCDS_Compulsions", "Percentage STAI_YA", "Percentage MFI"]
        
        
        azer = 2
        
        if (only_percentage == False):
            start = 1
        else:
            start = 16
            
        for j,k in zip(range(start,len(i)),list_data):
            worksheet.write('A'+str(azer), k)
            if(i[j] != "/"):
                if(np.isnan(i[j])==True):
                    i[j] = 0
            else:
                i[j] = 0
            worksheet.write('B'+str(azer), i[j])
            azer += 1
    
    workbook.close()

comportement_to_excel(patients_all, False)
comportement_to_excel(patients_all, True)

cluster0 = ['05','26','35','36','37','40','41']
cluster1 = ['02', '04', '08', '09', '11', '12', '14', '15', '18', '20', '21', '22', '24', '27', '28', '30', '34', '39', '42', '45']
cluster2 = ['13', '17', '19', '31', '32', '33', '43', '46']        
clusters = [cluster0,cluster1,cluster2]

list_data = ["Unités", "Osmolalité", "T1_BDI", "T1_OCDS_MODIFIE_Total", "T1_OCDS_Obsessions", "T1_OCDS_Compulsions", "T1_STAI_YA", "T1_MFI", 
             "T2_Bearni", "T2_BDI", "T2_OCDS_MODIFIE_Total", "T2_OCDS_Obsessions", "T2_OCDS_Compulsions", "T2_STAI_YA", "T2_MFI", 
             "Percentage BDI", "Percentage OCDS_MODIFIE_Total", "Percentage OCDS_Obsessions", "Percentage OCDS_Compulsions", "Percentage STAI_YA",     "Percentage MFI"]

color = ["blue", "orange", "#008000"]
labels = ["Cluster 0", "Cluster 1", "Cluster 2"]
for k in range(6): #6
    for data in [[2+k,9+k]]:
                   
        to_plot_cluster = []
        pops = []
        fig = plt.figure(figsize=(14.5,8))
        j = 0
        for cluster, couleur, nom_clust in zip(clusters, color, labels):
            to_plot = []
            
            for i in cluster:
                workbook = pd.read_excel(excel_path + 'Behavioural_data.xlsx', sheet_name=i)
                worksheet = workbook.to_numpy()
                
                if k < 6:
                    to_plot.append(worksheet[data[1],1]-worksheet[data[0],1])
                else:
                    to_plot.append(worksheet[data[1],1])
            
            y = np.ones(len(to_plot))*j
            
            plt.scatter(to_plot, y, s=400,color=couleur,alpha=0.5)
            pop_a = mpatches.Patch(color=couleur, label=nom_clust)
            pops.append(pop_a)
            j += 1
            
        new_name = worksheet[data[1],0].replace('T2_', '')
        new_name = new_name.replace('_', ' ')
        
        plt.axvline(x=0,linestyle="--",color="gray")
        plt.title("Difference of "+ new_name + " between T2 and T1")
        plt.xlabel("Score [/]")
        plt.legend(handles=pops)
        plt.yticks([])
        fig.tight_layout()
        fig.savefig(plot_path + "[Behavior] - Difference of "+ new_name + " between E2 and E1.pdf")

fig = plt.figure(figsize=(14.5,8))           
j = 0
to_plot_cluster = []
pops = []
for cluster, couleur, nom_clust in zip(clusters, color, labels):
    print(cluster)
    to_plot = []
    
    for i in cluster:
        workbook = pd.read_excel(excel_path + 'Behavioural_data.xlsx', sheet_name=i)
        worksheet = workbook.to_numpy()
        
        to_plot.append(worksheet[0,1])
    
    y = np.ones(len(to_plot))*j
    
    plt.scatter(to_plot, y, s=400,color=couleur,alpha=0.5)
    pop_a = mpatches.Patch(color=couleur, label=nom_clust)
    pops.append(pop_a)
    j += 1
    
plt.title("Alcohol consumption during the week before E1")
plt.xlabel("Alcohol unit [/]")
plt.axvline(x=0,linestyle="--",color="gray")
plt.legend(handles=pops)
plt.yticks([])
fig.tight_layout()
fig.savefig(plot_path + "[Behavior] - Alcohol consumption during the week before E1.pdf")

to_plot_cluster = []
pops = []
fig = plt.figure(figsize=(14.5,8))
      
for cluster, couleur, nom_clust in zip(clusters, color, labels):
    to_plot0 = []
    to_plot1 = []
    to_plot2 = []
    to_plot3 = []
    to_plot4 = []
    to_plot5 = []
    
    for i in cluster:
        workbook = pd.read_excel(excel_path + 'Behavioural_data.xlsx', sheet_name=i)
        worksheet = workbook.to_numpy()
        
        to_plot0.append(worksheet[15,1])
        to_plot1.append(worksheet[16,1])
        to_plot4.append(worksheet[19,1])
        to_plot5.append(worksheet[20,1])
    
    y0 = np.ones(len(to_plot0))*(1/4)
    y1 = np.ones(len(to_plot1))*(2/4)
    y4 = np.ones(len(to_plot4))*(3/4)
    y5 = np.ones(len(to_plot5))*(4/4)
    
    if (nom_clust == "Cluster 0"):
        y0 = np.ones(len(to_plot0))*(1/4+0.06)
        y1 = np.ones(len(to_plot1))*(2/4+0.06)
        y4 = np.ones(len(to_plot4))*(3/4+0.06)
        y5 = np.ones(len(to_plot5))*(4/4+0.06)
    elif (nom_clust == "Cluster 2"):
        y0 = np.ones(len(to_plot0))*(1/4-0.06)
        y1 = np.ones(len(to_plot1))*(2/4-0.06)
        y4 = np.ones(len(to_plot4))*(3/4-0.06)
        y5 = np.ones(len(to_plot5))*(4/4-0.06)

    plt.scatter(to_plot0, y0, s=400, color=couleur, alpha=0.5)
    plt.scatter(to_plot1, y1, s=400, color=couleur, alpha=0.5)
    plt.scatter(to_plot4, y4, s=400, color=couleur, alpha=0.5)
    plt.scatter(to_plot5, y5, s=400, color=couleur, alpha=0.5)
    pop_a = mpatches.Patch(color=couleur, label=nom_clust)
    pops.append(pop_a)

plt.title("Percentage change between E2 and E1")
plt.xlabel("Variation [%]")
plt.legend(handles=pops)
plt.ylim(0.0,5/4)
plt.yticks(ticks=[1/4,2/4,3/4,4/4],labels=["BDI", "OCDS - Total", "STAI YA", "MFI"])
fig.tight_layout()
fig.savefig(plot_path + "[Behavior] - Percentage change between E2 and E1.pdf")
  
workbook = pd.read_excel(excel_path + "violin_plot.xlsx", sheet_name="1")
workbook1 = pd.read_excel(excel_path + "violin_plot.xlsx", sheet_name="2")
# #37483E et black

fig, ax = plt.subplots(2,1,figsize = (20,16),gridspec_kw={'height_ratios': [1,3]})
sns.violinplot(y="Behavioral metrics", x="[/]", hue=" ",palette = ["navajowhite", "#56af59ff"],data=workbook1, split=True, ax=ax[0])
sns.stripplot(y="Behavioral metrics", x="[/]", hue=" ",data=workbook1, palette = ["orange", "#008000"], jitter = 0, split=True, ax=ax[0])
ax[0].set_title("Alcohol consumption during the week before E1",fontsize=25)
ax[0].set_ylabel("",fontsize = 0)
ax[0].set_xlabel("Alcohol unit [/]",fontsize = 23)
ax[0].set_xlim(-170,70)
ax[0].tick_params(axis='x', labelsize= 21)
ax[0].tick_params(axis='y', labelsize= 21)
ax[0].axvline(x=0,linestyle="--",color="gray")

sns.violinplot(y="Behavioral metrics", x="[/]", hue=" ",palette = ["navajowhite", "#56af59ff"], data=workbook, split=True, ax=ax[1])
sns.stripplot(y="Behavioral metrics", x="[/]", hue=" ",data=workbook, palette = ["orange", "#008000"], jitter = 0, split=True, ax=ax[1])
ax[1].set_title("Difference of behavioral metrics between E2 and E1",fontsize=25)
ax[1].set_ylabel("",fontsize = 0)
ax[1].set_xlabel("Score [/]",fontsize = 23)
ax[1].tick_params(axis='x', labelsize= 21)
ax[1].tick_params(axis='y', labelsize= 21)
ax[1].axvline(x=0,linestyle="--",color="gray")
ax[1].set_xlim(-170,70)
fig.supylabel("Behavioral metrics",fontsize = 23)
fig.tight_layout()
fig.savefig(plot_path + "[Behavior] - Violin plot.pdf")