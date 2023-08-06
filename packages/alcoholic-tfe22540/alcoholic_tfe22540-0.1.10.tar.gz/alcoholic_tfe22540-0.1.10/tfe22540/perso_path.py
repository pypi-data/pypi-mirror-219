"""
Created on Mon Jul 18 15:26:44 2022

@author: Fauston
"""

#TO BE ADAPTED ACCORDING TO FILES LOCATION

def perso_path_string(on_cluster=False):
    
    """
        Parameters
        ----------
        on_cluster : Boolean 
            True if works on clusters, False if work in local on your laptop computer. Warnings: in both cases, the structure of the study should be similar.
            
        Returns
        -------
        perso_path : String 
            File path of your study
    """
    
    if (on_cluster == False):
        perso_path = "D:/EPL/MASTER/TFE/alcoolique/"
    else: 
        perso_path = "/CECI/proj/pilab/PermeableAccess/alcooliques_copie/"
    
    excel_path = perso_path + "Analyse/Excel/"
    subjects_path = perso_path + "alcoholic_study/subjects/"
    patients_path = perso_path + "Patients/"
    plot_path = perso_path + "Analyse/Plots/"
    atlas_path = perso_path + "Atlas/"

    return perso_path, excel_path, subjects_path, patients_path, plot_path, atlas_path
    

def patient_number_list(list_type):
    if (list_type == "string_nb"):
        patient_numbers = ["02", "04", "05", "08", "09", "11", "12", "13", "14", "15", "17", "18", "19", "20", "21", "22", "24", "26", "27", "28", "30", "31", "32", "33", "34", "35", "36", "37", "39", "40", "41", "42", "43", "45", "46"] # Manon
        
        #["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","50","51","52","53"] # Laura     

    elif(list_type == "int_nb"):
        patient_numbers = [2,4,5,8,9,11,12,13,14,15,17,18,19,20,21,22,24,26,27,28,29,30,31,32,33,34,35,36,37,39,40,41,42,43,45,46]
        
        # [8,9,11,12,13,14,15,18,19,20,21,22,24,26,27,28,31,32,33,34,36,39,40,41,42,43,45,46,48,50,51,52,53]
        # [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,50,51,52,53] # Laura     

        
    return patient_numbers