"""
Created on Wed Mar 23 11:07:27 2022

@author: Fauston
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
from sklearn.cluster import KMeans, AffinityPropagation

from tfe22540.atlas_modif_name import get_corr_atlas_list, get_atlas_list
from tfe22540.perso_path import perso_path_string


perso_path, excel_path, subjects_path, patients_path, plot_path, atlas_path = perso_path_string() 


def get_all_metric(file_path, patient_numbers, bool_metric): 
    
    """
        Parameters
        ----------
        file_path : List of strings 
            Links of the considerind files. For example, [link of FA, link of MD] 
        patient_numbers : List of strings
            Number of all patients in string ["02"] for example.    
        bool_metric : boolean
            Specify if we work in WM only or in both GM and WM.
            
        Returns
        -------
        all_metric : Matrix of int
            The columns are representing the patient and the rows the atlases. For example, this matrix will be (141*4) x 35 : "*4" because of the four DTI metrics. So the first 141 are representing the values of FA in each atlas for          each patient and so on.
    """
    
    nb_metrics = len(file_path)
    atlas_list = get_corr_atlas_list(get_atlas_list(onlywhite = bool_metric))
    percentage_change_all = np.zeros((len(atlas_list), len(patient_numbers)))
    all_metric = np.zeros((len(atlas_list)*nb_metrics, len(patient_numbers)))
    
    for metric, j in zip(file_path, range(nb_metrics)):
        for patient_nb, i in zip(patient_numbers, range(len(patient_numbers))):
            worksheet = pd.read_excel(metric, sheet_name=patient_nb)
            worksheet = worksheet.to_numpy()
            worksheet = np.nan_to_num(worksheet)
            # a = np.nan_to_num(worksheet[:,0]) #Atlas name
            for atlas in range(len(atlas_list)):
                b = np.nan_to_num(worksheet[atlas,1]) #Mean E1
                c = np.nan_to_num(worksheet[atlas,2]) #Mean E2
                d = np.nan_to_num(worksheet[atlas,3]) #Mean E3
                e = np.nan_to_num(worksheet[atlas,4]) #Percentage change (Value not loaded because of the formula, so it must be recalculated)
                if b == 0:
                    percentage_change_all[atlas,i] = 0
                else:
                    percentage_change_all[atlas,i] = np.nan_to_num((c-b)*100/b)
        start = j*len(atlas_list)
        stop = (len(atlas_list))+j*len(atlas_list)
        all_metric[start:(stop),:] = percentage_change_all
        
    return all_metric


def get_all_metric_for_one_particular_roi(file_path, patient_numbers, list_atlas):
   
    """
        Parameters
        ----------
        file_path : List of strings 
            Links of the considerind files. For example, [link of FA, link of MD] 
        patient_numbers : List of strings
            Number of all patients in string ["02"] for example.    
        list_atlas : list of strings
            To specify the atlases on which to base clustering.
            
        Returns
        -------
        all_metric : Matrix of int
            The columns are representing the patient and the rows the atlases. For example, this matrix will be (X*4) x 35 : "*4" because of the four DTI metrics. Thus, the first X represents the AF values in each selected atlas for           each patient and so on.
    """
     
    nb = len(list_atlas)
    nb_metrics = len(file_path)
    
    percentage_change_all = np.zeros((nb, len(patient_numbers)))

    all_metric = np.zeros((nb*nb_metrics, len(patient_numbers)))
    
    for metric, j in zip(file_path, range(nb_metrics)):
        for patient_nb, i in zip(patient_numbers, range(len(patient_numbers))):
            worksheet = pd.read_excel(metric, sheet_name=patient_nb)
            worksheet = worksheet.to_numpy()
            
            for l in range(len(list_atlas)):
                for k in range(worksheet.shape[0]):
                    if worksheet[k,0] in list_atlas[l]:
                        percentage_change_all[l,i] = worksheet[k,4]
        
        start = j*nb
        stop = (nb)+j*nb
        all_metric[start:(stop),:] = percentage_change_all

    return all_metric


def get_kmeans(all_metric, nb_clust, axes_names, affinity, display, save):
    
    """
        Parameters
        ----------
        all_metric : Matrix of int
            Results of get_all_metric or get_all_metric_for_one_particular_roi.
        nb_clust : Int
            Number of clusters.
        axes_names : List of string
            Need a list of three strings for axes (x,y,z).
        affinity : Boolean
            To choose the model, either KMeans of AffinityPropagation.
        display : Boolean
            To show the plot.
        save : Boolean
            To save the plot.
    
        Returns
        -------
        y : List of int
            A label is assigned to each patient and each label corresponds to a cluster.
    """
    
    X = all_metric.T
    
    #------------------ KMeans clustering ----------------------
    if (affinity == False):
        model = KMeans(n_clusters=nb_clust,n_init=1000)
    
    #----------- AffinityPropagation clustering ----------------
    else:
        model = AffinityPropagation()
    
    model.fit(X)
    y = model.predict(X)

    if (display == True):
        fig = plt.figure(figsize=(15, 12))
        ax = Axes3D(fig, rect=[0, 0, 0.95, 1], elev=10, azim=124)
        labs = []
        for i in range(nb_clust):
            ax.scatter(X[y==i,0],X[y==i,1],X[y==i,2])
            labs = np.append(labs, 'Cluster '+str(i))
        
        ax.legend(labels=labs)
        
        ax.set_title("Cluster")
        ax.set_xlabel(axes_names[0], fontsize=13)
        ax.set_ylabel(axes_names[1], fontsize=13)
        ax.set_zlabel(axes_names[2], fontsize=13)
        plt.show
        
    if (save == True):
        fig.savefig(plot_path + "[3D] - Clusters_3D.pdf")

    return y