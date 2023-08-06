import numpy as np
from dipy.data import get_fnames
from dipy.io.image import load_nifti_data
import xlsxwriter 
import nibabel as nib
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from tfe22540.plot_functions import histo_multicomp
from tfe22540.atlas_modif_name import get_corr_atlas_list, get_atlas_list
from tfe22540.perso_path import perso_path_string, patient_number_list


perso_path, excel_path, subjects_path, patients_path, plot_path, atlas_path = perso_path_string() 

patient_numbers = patient_number_list("string_nb") # Manon


# =============================================================================
# EXCEL
# =============================================================================

Anat_all = np.array(["seg_E1","seg_E2"])
for patient_nb in patient_numbers :
    paths = np.array([subjects_path + "sub" + patient_nb + "_E1/T1/sub" + patient_nb + "_E1_T1_segmentation.nii.gz",
                      subjects_path + "sub" + patient_nb + "_E2/T1/sub" + patient_nb + "_E2_T1_segmentation.nii.gz"])
    Anat_all = np.append(Anat_all,paths,axis=0)
Anat_all = np.reshape(Anat_all,((len(patient_numbers)+1),2))
Anat_all = np.delete(Anat_all, (0), axis=0)

def get_excel_tissue_classification(Anat_all, patient_numbers):
    
    workbook = xlsxwriter.Workbook(excel_path + 'DTI_Volume_changes.xlsx') 
    
    name_sheet =  ["E1", "E2"]
    
    for name in range(len(name_sheet)):
        worksheet = workbook.add_worksheet(name_sheet[name]) 
        
        worksheet.write("B1", "volume_CSF")
        worksheet.write("C1", "volume_WM")
        worksheet.write("D1", "volume_GM")
        worksheet.write("E1", "volume_rel_CSF") 
        worksheet.write("F1", "volume_rel_WM")	
        worksheet.write("G1", "volume_rel_GM")
        
        for seg, patient_nb in zip(Anat_all, range(len(patient_numbers))):
            
            t1_fname, _, _ = get_fnames('tissue_data')
            t1 = load_nifti_data(seg[name])
        
            mask_CSF = np.zeros((t1.shape[0], t1.shape[1], t1.shape[2]))
            mask_GM = np.zeros((t1.shape[0], t1.shape[1], t1.shape[2]))
            mask_WM = np.zeros((t1.shape[0], t1.shape[1], t1.shape[2]))

            mask_CSF[t1 == 1] = 1
            mask_GM[t1 == 2] = 1
            mask_WM[t1 == 3] = 1
            
            volume_CSF = np.sum(mask_CSF)
            volume_GM = np.sum(mask_GM)
            volume_WM = np.sum(mask_WM)
        
            volume_total = volume_CSF + volume_WM + volume_GM
            volume_relCSF = volume_CSF / volume_total
            volume_relWM = volume_WM / volume_total
            volume_relGM = volume_GM / volume_total
        
            worksheet.write('A'+str(patient_nb+2), "sub"+str(patient_numbers[patient_nb]))
            worksheet.write('B'+str(patient_nb+2), volume_CSF) 
            worksheet.write('C'+str(patient_nb+2), volume_WM) 
            worksheet.write('D'+str(patient_nb+2), volume_GM) 
            worksheet.write('E'+str(patient_nb+2), volume_relCSF) 
            worksheet.write('F'+str(patient_nb+2), volume_relWM) 
            worksheet.write('G'+str(patient_nb+2), volume_relGM) 
    
    worksheet_percentage = workbook.add_worksheet("Percentage change") 
    worksheet_percentage.write("A1", "Patients")
    worksheet_percentage.write("B1", "Percentage change")
    worksheet_percentage.write("C1", "volume_rel_CSF")
    worksheet_percentage.write("D1", "volume_rel_WM")
    worksheet_percentage.write("E1", "volume_rel_GM")
    worksheet_percentage.write("F1", "Difference")
    worksheet_percentage.write("G1", "volume_rel_CSF")
    worksheet_percentage.write("H1", "volume_rel_WM")
    worksheet_percentage.write("I1", "volume_rel_GM")
    worksheet_percentage.write("J1", "Sum")
    
    worksheet_T1 = workbook.get_worksheet_by_name('E1')
    worksheet_T2 = workbook.get_worksheet_by_name('E2')
    
    for patient_nb in range(len(patient_numbers)):
        worksheet_percentage.write("A"+str(2+patient_nb), "sub"+str(patient_numbers[patient_nb]))
        worksheet_percentage.write("C"+str(2+patient_nb), (worksheet_T2.table[1+patient_nb][4].number - worksheet_T1.table[1+patient_nb][4].number)*100/worksheet_T1.table[1+patient_nb][4].number)
        worksheet_percentage.write("D"+str(2+patient_nb), (worksheet_T2.table[1+patient_nb][5].number - worksheet_T1.table[1+patient_nb][5].number)*100/worksheet_T1.table[1+patient_nb][5].number)
        worksheet_percentage.write("E"+str(2+patient_nb), (worksheet_T2.table[1+patient_nb][6].number - worksheet_T1.table[1+patient_nb][6].number)*100/worksheet_T1.table[1+patient_nb][6].number)
        
        worksheet_percentage.write("G"+str(2+patient_nb), (worksheet_T2.table[1+patient_nb][4].number - worksheet_T1.table[1+patient_nb][4].number)*100)
        worksheet_percentage.write("H"+str(2+patient_nb), (worksheet_T2.table[1+patient_nb][5].number - worksheet_T1.table[1+patient_nb][5].number)*100)
        worksheet_percentage.write("I"+str(2+patient_nb), (worksheet_T2.table[1+patient_nb][6].number - worksheet_T1.table[1+patient_nb][6].number)*100)
        diffCSF = (worksheet_T2.table[1+patient_nb][4].number - worksheet_T1.table[1+patient_nb][4].number)*100
        diffWM = (worksheet_T2.table[1+patient_nb][5].number - worksheet_T1.table[1+patient_nb][5].number)*100
        diffGM = (worksheet_T2.table[1+patient_nb][6].number - worksheet_T1.table[1+patient_nb][6].number)*100
        somme = diffCSF + diffWM + diffGM
        worksheet_percentage.write("J"+str(2+patient_nb), somme)
   
    workbook.close() 
        
get_excel_tissue_classification(Anat_all, patient_numbers)

def volume_all(diff, clusters):
    
    workbook = pd.read_excel(excel_path + 'DTI_Volume_changes.xlsx', sheet_name = "Percentage change")
    worksheet = workbook.to_numpy()
    noddi_means_all = []
    coherence_all = []
    
    for cluster in clusters:
        noddi_means = np.zeros((len(cluster),3))
        
        for i,j in zip(cluster,range(noddi_means.shape[0])):
            
            indice = np.where(worksheet[:,0] == i)[0][0]
            
            if (diff == False):
                noddi_means[j,0] = worksheet[indice,2]
                noddi_means[j,1] = worksheet[indice,3]
                noddi_means[j,2] = worksheet[indice,4]
            else:
                noddi_means[j,0] = worksheet[indice,6]
                noddi_means[j,1] = worksheet[indice,7]
                noddi_means[j,2] = worksheet[indice,8]
            
            coherence = np.sum(noddi_means, axis=1)
        
        noddi_means_all.append(noddi_means)
        coherence_all.append(coherence)
    
    return noddi_means_all, coherence_all

cluster0 = ['sub05','sub26','sub35','sub36','sub37','sub40','sub41']
cluster1 = ['sub02', 'sub04', 'sub08', 'sub09', 'sub11', 'sub12', 'sub14', 'sub15', 'sub18', 'sub20', 'sub21', 'sub22', 'sub24', 'sub27', 'sub28', 'sub30', 'sub34', 'sub39', 'sub42', 'sub45']
cluster2 = ['sub13', 'sub17', 'sub19', 'sub31', 'sub32', 'sub33', 'sub43', 'sub46']        
clusters_subname = [cluster1,cluster2]

cluster_name = ["Cluster 1", 'Cluster 2']
noddi_means_all_diff, coherence_all = volume_all(True, clusters_subname)
noddi_means_all, coherence_all_diff = volume_all(False, clusters_subname)

for i in range(len(cluster_name)):
    histo_multicomp(noddi_means_all_diff[i], clusters_subname[i], "[Volume] - " + cluster_name[i] + " - volume changes in the whole brain (difference)", cluster_name[i] + " - volume changes in the whole brain (difference)", ["CSF", "WM", "GM"], True, True)
    histo_multicomp(noddi_means_all_diff[i], clusters_subname[i], "[Volume] - " + cluster_name[i] + " - volume changes in the whole brain (percentage change)", cluster_name[i] + " - volume changes in the whole brain (percentage change)", ["CSF", "WM", "GM"], True, True)
    
coherence_cluster1 = np.mean(coherence_all[0])*100
coherence_cluster2 = np.mean(coherence_all[1])*100

def volume_atlas_signif(clusters,atlas):
    diff_all = []
    percentage_all = []
    mean_all = []
    
    for cluster in clusters:
        interm = []
        interm1 = []
        
        for patient in cluster:
            atlas_T1 = patients_path + "#" + patient + "/Mask/sub" + patient + "_" + atlas + "_mask_E1.nii.gz"
            atlas_T2 = patients_path + "#" + patient + "/Mask/sub" + patient + "_" + atlas + "_mask_E2.nii.gz"
            
            atlas_T1 = nib.load(atlas_T1).get_fdata()
            atlas_T2 = nib.load(atlas_T2).get_fdata()
            
            volume_atlas_T1 = np.sum(atlas_T1) 
            volume_atlas_T2 = np.sum(atlas_T2)
            
            diff = volume_atlas_T2 - volume_atlas_T1
            percentage = (volume_atlas_T2 - volume_atlas_T1)*100/volume_atlas_T1

            interm.append(diff)
            interm1.append(percentage)
            
        mean_all.append(np.mean(interm))
        diff_all.append(interm)
        percentage_all.append(interm1)
        
    return diff_all, mean_all, percentage_all
    
cluster0 = ['05','26','35','36','37','40','41']
cluster1 = ['02', '04', '08', '09', '11', '12', '14', '15', '18', '20', '21', '22', '24', '27', '28', '30', '34', '39', '42', '45']
cluster2 = ['13', '17', '19', '31', '32', '33', '43', '46']        
clusters = [cluster1,cluster2]

cluster_name1 = ['sub02', 'sub04', 'sub08', 'sub09', 'sub11', 'sub12', 'sub14', 'sub15', 'sub18', 'sub20', 'sub21', 'sub22', 'sub24', 'sub27', 'sub28', 'sub30', 'sub34', 'sub39', 'sub42', 'sub45']
cluster_name2 = ['sub13', 'sub17', 'sub19', 'sub31', 'sub32', 'sub33', 'sub43', 'sub46']     
cluster_all = ['sub02', 'sub04', 'sub08', 'sub09', 'sub11', 'sub12', 'sub13', 'sub14', 'sub15', 'sub17', 'sub18', 'sub19', 'sub20', 'sub21', 'sub22', 'sub24', 'sub27', 'sub28', 'sub30', 'sub31', 'sub32', 'sub33', 'sub34', 'sub39', 'sub42','sub43', 'sub45', 'sub46']   
cluster_name = [cluster_name1,cluster_name2]

# Acoustic radiation, Anterior comissure, Cerebellum, Cingulum, CC, Cortico ponto cerebellum, Fornix, Inferior/middle/superior cerebellar fasciculus, middle longitudinal fasciculus, optic radiation, uncinate fasciculus

atlas_list_tt = ["Brain-Stem",
                 "Amygdala L",
                 "Amygdala R",
                 "Cerebellum  Crus I R",
                 "Cerebellum  Crus II R",
                 "Cerebellum  I-IV L",
                 "Cerebellum  IX L", 
                 "Cerebellum  VIIIa L",
                 "Cerebellum  VIIIb L",
                 "Cerebellum  VIIIb R",
                 "Cerebellum  VIIb R",
                 "Cerebellum  X L",
                 "Cerebellum  X R", 
                 "Cerebellum Vermis", 
                 "Cortico Ponto Cerebellum  L", 
                 "Cortico Ponto Cerebellum  R",
                 "Fornix L",
                 "Inferior Cerebellar Pedunculus  L", 
                 "Inferior Cerebellar Pedunculus  R",
                 "Hippocampus L",
                 "Hippocampus R",
                 "Middle Cerebellar Peduncle", 
                 "Superior Cerebellar Pedunculus  L",
                 "Superior Cerebellar Pedunculus  R",
                 "Thalamus L",
                 "Thalamus R"]

atlas_list = get_atlas_list()
atlas_name = get_corr_atlas_list(atlas_list)

diff_all_atlas = []
mean_all_atlas = []
percentage_all_atlas = []
j = 0

fig = plt.figure(figsize = (14.5,8))

for i, atlas_nb in zip(atlas_list_tt, range(len(atlas_list_tt))):
    indice = np.where(atlas_name[:,0] == i)[0][0]
    
    atlas = atlas_name[indice,1]
    if(".nii.gz" in atlas):
        atlas = atlas.replace('.nii.gz', '')
    if("Cerebellar/" in atlas):
        atlas = atlas.replace('Cerebellar/', '')
    if("Cerebelar" in atlas):
        atlas = atlas.replace('Cerebelar', 'Cerebellar')
    if("Cerebellum/" in atlas):
        atlas = atlas.replace('Cerebellum/', '')
    if("Harvard/" in atlas):
        atlas = atlas.replace('Harvard/', '')
    if("Harvard_cortex/" in atlas):
        atlas = atlas.replace('Harvard_cortex/', '')
    if("Lobes/" in atlas):
        atlas = atlas.replace('Lobes/', '')
    if("XTRACT/" in atlas):
        atlas = atlas.replace('XTRACT/', '')
    if("CC/" in atlas): 
        atlas = atlas.replace('CC/', '')
    
    diff, mean, percentage = volume_atlas_signif(clusters,atlas)
    diff_all_atlas.append(diff) 
    mean_all_atlas.append(mean)
    percentage_all_atlas.append(percentage)
    new_name = atlas.replace('  ', ' ')
    color = ["red", "blue"]
    labels = ["Cluster 1", "Cluster 2"]
         
    to_plot_cluster = []
    pops = []
    indent = 0

    for cluster, couleur, nom_clust in zip(clusters, color, labels):
        to_plot = []
        
        for i in range(len(cluster)):
            worksheet = percentage_all_atlas[atlas_nb][indent][i]
            to_plot.append(worksheet)
            
        y = np.ones(len(to_plot))*j
                
        plt.scatter(to_plot, y, s=400,color=couleur,alpha=0.5)
        pop_a = mpatches.Patch(color=couleur, label=nom_clust)
        pops.append(pop_a)
    
        indent += 1
    j += 2
    
plt.title("Percentage change of volume between E2 and E1")
plt.xlabel("Variation [%]")
plt.legend(handles=pops)
plt.xlim(-150,150)
plt.yticks(ticks=np.arange(0,2*26,2),labels=atlas_list_tt)
plt.ylim(-2,2*26)
fig.tight_layout()
plt.show()
fig.savefig("[Tissue classification] - Percentage change of volume between E2 and E1.pdf")

percent_clust1 = []
percent_clust2 = []

for i in range(len(percentage_all_atlas)):
    percent_clust1 = np.append(percent_clust1,percentage_all_atlas[i][0],axis=0)
    percent_clust2 = np.append(percent_clust2,percentage_all_atlas[i][1],axis=0)
    
percent_clust1 = np.reshape(percent_clust1,(26,20))
percent_clust1 = np.nan_to_num(percent_clust1, copy=True)
percent_clust2 = np.reshape(percent_clust2,(26,8))
percent_clust2 = np.nan_to_num(percent_clust2, copy=True)


for j in range(percent_clust1.shape[0]):
    mean_line = np.mean(percent_clust1[j,:][percent_clust1[j,:]!=0])
    percent_clust1[j,:][percent_clust1[j,:]==0] = mean_line
    
for j in range(percent_clust2.shape[0]):
    mean_line = np.mean(percent_clust2[j,:][percent_clust2[j,:]!=0])
    percent_clust2[j,:][percent_clust2[j,:]==0] = mean_line

fig = plt.figure(figsize=(20,16))
plt.style.use('seaborn')
plt.grid(axis='x',linestyle='--')
plt.grid(axis='y',linestyle='--')
plt.boxplot(percent_clust1.T,vert=False,labels = atlas_list_tt)
plt.xlim(-120,250)
plt.tick_params(axis='y', labelsize= 20)
plt.tick_params(axis='x', labelsize= 20)
plt.xlabel("Variation [%]",fontsize=23)
plt.title("Percentage of changes of the volume between E2 and E1 (counpicuous zones) - Cluster 1",fontsize=25)
fig.savefig(plot_path + "[Tissue classification] - Percentage of changes of the volume between E2 and E1 (counpicuous zones) - Cluster 1.pdf")

fig = plt.figure(figsize=(20,16))
plt.style.use('seaborn')
plt.grid(axis='x',linestyle='--')
plt.grid(axis='y',linestyle='--')
plt.boxplot(percent_clust2.T,vert=False,labels = atlas_list_tt)
plt.xlim(-120,150)
plt.tick_params(axis='y', labelsize= 20)
plt.tick_params(axis='x', labelsize= 20)
plt.xlabel("Variation [%]",fontsize=23)
plt.title("Percentage of changes of the volume between E2 and E1 (conspicuous zones) - Cluster 2",fontsize=25)
fig.savefig(plot_path + "[Tissue classification] - Percentage of changes of the volume between E2 and E1 (counpicuous zones) - Cluster 2.pdf")

    