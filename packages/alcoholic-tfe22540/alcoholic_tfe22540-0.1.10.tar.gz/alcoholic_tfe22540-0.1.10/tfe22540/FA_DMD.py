"""
Created on Wed Apr 13 09:14:26 2022

@author: Fauston
"""

import numpy as np
import nibabel as nib

from tfe22540.perso_path import perso_path_string


perso_path, excel_path, subjects_path, patients_path, plot_path, atlas_path = perso_path_string()


def get_FA_DIAMOND(folder_path, patient_path):
    """
        Parameters
        ----------
        folder_path : String 
            Link of the file in which we are. 
        patient_path : List of strings
            Number of all patients in string ["sub#_E1"] for example.

        Returns
        -------
        None. But creation of files containing the cFA, cMD, cAD and cRD for each patient. "c" stands for compartment.
    """

    tenseur_list = ["t0", "t1"]

    for tenseur in tenseur_list:

        path = folder_path + "/subjects/" + patient_path + "/dMRI/microstructure/dti/" + patient_path + "_FA.nii.gz"

        comp = folder_path + "/subjects/" + patient_path + "/dMRI/microstructure/diamond/" + patient_path + "_diamond_" + tenseur + ".nii.gz"
        comp = nib.load(comp).get_fdata()

        MD = np.zeros((comp.shape[0], comp.shape[1], comp.shape[2]))
        print(MD.shape)
        AD = np.zeros((comp.shape[0], comp.shape[1], comp.shape[2]))
        RD = np.zeros((comp.shape[0], comp.shape[1], comp.shape[2]))
        FA = np.zeros((comp.shape[0], comp.shape[1], comp.shape[2]))

        D = np.array([[np.squeeze(comp[:, :, :, :, 0]), np.squeeze(comp[:, :, :, :, 1]), np.squeeze(comp[:, :, :, :, 3])],
                      [np.squeeze(comp[:, :, :, :, 1]), np.squeeze(comp[:, :, :, :, 2]), np.squeeze(comp[:, :, :, :, 4])],
                      [np.squeeze(comp[:, :, :, :, 3]), np.squeeze(comp[:, :, :, :, 4]), np.squeeze(comp[:, :, :, :, 5])]])

        for i in range(comp.shape[0]):
            for j in range(comp.shape[1]):
                for k in range(comp.shape[2]):

                    valeurs_propres = np.array(np.linalg.eigvals(D[:, :, i, j, k]))
                    max_valeur = max(np.abs(valeurs_propres))
                    index_lambda = [l for l in range(len(valeurs_propres)) if abs(valeurs_propres[l]) == max_valeur]

                    copy_valeurs_propres = np.copy(valeurs_propres)
                    copy_valeurs_propres = np.delete(copy_valeurs_propres, index_lambda[0])
                    copy_valeurs_propres = np.array(copy_valeurs_propres)

                    MD[i, j, k] = (valeurs_propres[0] + valeurs_propres[1] + valeurs_propres[2]) / 3
                    AD[i, j, k] = valeurs_propres[index_lambda[0]]
                    RD[i, j, k] = (copy_valeurs_propres[0] + copy_valeurs_propres[1]) / 2

                    if((valeurs_propres[0]**2 + valeurs_propres[1]**2 + valeurs_propres[2]**2) == 0):
                        FA[i, j, k] = 0
                    else:
                        FA[i, j, k] = np.sqrt(3 / 2) * np.sqrt(((valeurs_propres[0] - MD[i, j, k])**2 + (valeurs_propres[1] - MD[i, j, k])**2 + (valeurs_propres[2] - MD[i, j, k])**2) / (valeurs_propres[0]**2 + valeurs_propres[1]**2 + valeurs_propres[2]**2))

        MD[np.isnan(MD)] = 0
        print(MD.shape)
        out = nib.Nifti1Image(MD, affine=nib.load(path).affine, header=nib.load(path).header)
        out.to_filename(folder_path + "/subjects/" + patient_path + "/dMRI/microstructure/diamond/" + patient_path + "_MD_DMD_" + tenseur + ".nii.gz")

        AD[np.isnan(AD)] = 0
        out1 = nib.Nifti1Image(AD, affine=nib.load(path).affine, header=nib.load(path).header)
        out1.to_filename(folder_path + "/subjects/" + patient_path + "/dMRI/microstructure/diamond/" + patient_path + "_AD_DMD_" + tenseur + ".nii.gz")

        RD[np.isnan(RD)] = 0
        out2 = nib.Nifti1Image(RD, affine=nib.load(path).affine, header=nib.load(path).header)
        out2.to_filename(folder_path + "/subjects/" + patient_path + "/dMRI/microstructure/diamond/" + patient_path + "_RD_DMD_" + tenseur + ".nii.gz")

        FA[np.isnan(FA)] = 0
        out3 = nib.Nifti1Image(FA, affine=nib.load(path).affine, header=nib.load(path).header)
        out3.to_filename(folder_path + "/subjects/" + patient_path + "/dMRI/microstructure/diamond/" + patient_path + "_FA_DMD_" + tenseur + ".nii.gz")


def get_cMetrics(folder_path, patient_path):
    """
        Parameters
        ----------
        folder_path : String 
            Link of the file in which we are. 
        patient_path : List of strings
            Number of all patients in string ["sub#_E1"] for example.

        Returns
        -------
        None. But creation of files containing the wFA, wMD, wAD and wRD for each patient. "w" stands for weigthed.
    """

    metrics = ["FA", "MD", "AD", "RD"]

    for metric in metrics:
        metric_t0 = folder_path + "/subjects/" + patient_path + "/dMRI/microstructure/diamond/" + patient_path + "_" + metric + "_DMD_t0.nii.gz"

        metric_t1 = folder_path + "/subjects/" + patient_path + "/dMRI/microstructure/diamond/" + patient_path + "_" + metric + "_DMD_t1.nii.gz"

        fraction_t0 = folder_path + "/subjects/" + patient_path + "/dMRI/microstructure/diamond/" + patient_path + "_diamond_fractions_f0.nii.gz"

        fraction_t1 = folder_path + "/subjects/" + patient_path + "/dMRI/microstructure/diamond/" + patient_path + "_diamond_fractions_f1.nii.gz"

        cMetric = (nib.load(metric_t0).get_fdata() * nib.load(fraction_t0).get_fdata() + nib.load(metric_t1).get_fdata() * nib.load(fraction_t1).get_fdata()) / (nib.load(fraction_t1).get_fdata() + nib.load(fraction_t0).get_fdata())

        out = nib.Nifti1Image(cMetric, affine=nib.load(metric_t0).affine, header=nib.load(metric_t0).header)
        out.to_filename(folder_path + "/subjects/" + patient_path + "/dMRI/microstructure/diamond/" + patient_path + "_w" + metric + ".nii.gz")
