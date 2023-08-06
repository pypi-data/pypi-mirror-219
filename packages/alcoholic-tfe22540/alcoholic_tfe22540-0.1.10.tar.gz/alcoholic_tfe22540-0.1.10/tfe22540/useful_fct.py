import os
import datetime
import time
import numpy as np
from future.utils import iteritems
import subprocess

from tfe22540.perso_path import perso_path_string, patient_number_list


perso_path, excel_path, subjects_path, patients_path, plot_path, atlas_path = perso_path_string() 


def makedir(dir_path):
    
    """
        Create a directory in the location specified by the dir_path and write the log in the log_path.
    
        :param dir_path: The path to the directory to create.
        :param log_path: The path to the log file to write verbose data.
        :param log_prefix: The prefix to use in the log file.
    """
    
    if not(os.path.exists(dir_path)):
        try:
            os.makedirs(dir_path)
        except OSError:
            print ("Creation of the directory %s failed" % dir_path)
        else:
            print ("Successfully created the directory %s " % dir_path)


def folder_patients(patient_numbers, folder_path, sub_files, sub_sub_files, sub_sub_files2):
    
    atlas_dir = os.path.join(folder_path, "Atlas")
    makedir(atlas_dir)
    analyse_dir = os.path.join(folder_path, "Analyse")
    makedir(analyse_dir)
    excel_dir = os.path.join(analyse_dir, "Excel")
    makedir(excel_dir)
    plot_dir = os.path.join(analyse_dir, "Plots")
    makedir(plot_dir)
    patient_dir = os.path.join(folder_path, "Patients")
    makedir(patient_dir)
    code_dir = os.path.join(folder_path, "Codes")
    makedir(code_dir)
    
    for i in patient_numbers:
        out_dir = os.path.join(patient_dir, "#" + i + "/")
        makedir(out_dir)
        for j in sub_files:
            out_dir_sub = os.path.join(out_dir + j + "/")
            makedir(out_dir_sub)
            if (j == "Atlas"):
                for k in sub_sub_files: 
                    out_dir_sub_sub = os.path.join(out_dir_sub + k + "/")
                    makedir(out_dir_sub_sub)
            elif (j == "Registration"):
                out_dir_sub_sub = os.path.join(out_dir_sub + "/microstructure/")
                makedir(out_dir_sub_sub)
                for k in sub_sub_files2: 
                    out_dir_sub_sub_sub = os.path.join(out_dir_sub_sub + k + "/")
                    makedir(out_dir_sub_sub_sub)

patient_numbers = patient_number_list("string_nb")   

sub_files = ["Anat", "Atlas", "Mask", "Maps", "Registration"]
sub_sub_files = ["CC", "Cerebellar", "Cerebellum", "Harvard", "Harvard_cortex", "Lobes", "XTRACT"]
sub_sub_files2 = ["dti", "diamond", "noddi", "mf"]

if __name__ == '__main__':
    
    folder_patients(patient_numbers, perso_path, sub_files, sub_sub_files, sub_sub_files2)