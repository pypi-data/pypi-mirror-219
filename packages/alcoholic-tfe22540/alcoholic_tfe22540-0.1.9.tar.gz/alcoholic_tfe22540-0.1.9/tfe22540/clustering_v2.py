
import numpy as np
import pandas as pd
import xlsxwriter
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import seaborn as sns

from tfe22540.perso_path import perso_path_string, patient_number_list

"""
    DATASET
"""

perso_path, excel_path, subjects_path, patients_path, plot_path, atlas_path = perso_path_string() 
path = excel_path

# Methode par DTI :
mean_ROI_AD = path + r'mean_ROI_AD.xlsx'
mean_ROI_FA = path + r'mean_ROI_FA.xlsx'
mean_ROI_MD = path + r'mean_ROI_MD.xlsx'
mean_ROI_RD = path + r'mean_ROI_RD.xlsx'
#print("La taille du dataset pour un patient en employant la DTI est de" , pd.read_excel(mean_ROI_AD).shape)

# Methode par NODDI :
# mean_ROI_noddi_fbundle = path + r'mean_ROI_noddi_fbundle.xlsx'
mean_ROI_noddi_fextra = path + r'mean_ROI_noddi_fextra.xlsx'
mean_ROI_noddi_fintra = path + r'mean_ROI_noddi_fintra.xlsx'
mean_ROI_noddi_fiso = path + r'mean_ROI_noddi_fiso.xlsx'
mean_ROI_noddi_icvf = path + r'mean_ROI_noddi_icvf.xlsx'
mean_ROI_noddi_odi = path + r'mean_ROI_noddi_odi.xlsx'
#print("La taille du dataset pour un patient en employant NODDI est de", pd.read_excel(mean_ROI_noddi_fextra).shape)

# Methode par DIAMOND :
mean_ROI_diamond_fractions_csf = path + r'mean_ROI_diamond_fractions_csf.xlsx'
mean_ROI_diamond_fraction_ftot = path + r'mean_ROI_diamond_fractions_ftot.xlsx'
mean_ROI_wAD = path + r'mean_ROI_wAD.xlsx'
mean_ROI_wFA = path + r'mean_ROI_wFA.xlsx'
mean_ROI_wMD = path + r'mean_ROI_wMD.xlsx'
mean_ROI_wRD = path + r'mean_ROI_wRD.xlsx'
#print("La taille du dataset pour un patient en employant DIAMOND est de" ,pd.read_excel(mean_ROI_diamond_fractions_csf).shape)

# Methode par MicroFingerprinting :
mean_ROI_mf_frac_csf = path + r'mean_ROI_mf_frac_csf.xlsx'
mean_ROI_mf_frac_ftot = path + r'mean_ROI_mf_frac_ftot.xlsx'
mean_ROI_mf_fvf_tot = path + r'mean_ROI_mf_fvf_tot.xlsx'
mean_ROI_mf_wfvf = path + r'mean_ROI_mf_wfvf.xlsx'
#print("La taille du dataset pour un patient en employant MF est de", pd.read_excel(mean_ROI_mf_frac_csf).shape)

metric_name_DTI = ["FA", "MD", "AD", "RD"]
metric_name_NODDI = ["fintra", "fextra", "fiso", "odi"]
metric_name_DIAMOND1 = ["wFA", "wMD", "wAD", "wRD"]
metric_name_DIAMOND2 = ["frac_ftot", "frac_csf"]
metric_name_DIAMOND = ["wFA", "wMD", "wAD", "wRD", "frac_ftot", "frac_csf"]
metric_name_MF = ["frac_csf", "frac_ftot", "fvf_tot", "wfvf"]


"""
    FONCTIONS UTILES 
"""


def get_kmeans(all_metric, nb_cluster):
    
    """
        Algorithme Kmeans implementé
    """
   
    X = all_metric.T
    model = KMeans(n_clusters=nb_cluster, init='k-means++')
    model.fit(X)
    y = model.predict(X)
    return y


def get_cluster(ypred, patient_numbers, nb_cluster):
    
    """
        Retourne une liste (clusters) avec des nb_cluster sub_lists, 
            chaque sub_list contient les numéros des patients associées à un cluster
    """
    
    clusters = []
    for n in range(nb_cluster):
        sublist = []
        for i, patient_nb in zip(ypred, patient_numbers):
            if (i == n):
                sublist.append(patient_nb)
        clusters.append(sublist)
    return clusters


def elbow_graph(all_metric):
    
    """
        Plot un graph elbow : 
            cela permet de sélectionner le nombre optimal de clusters 
            en ajustant le modèle avec une gamme de valeurs pour k dans l'algorithme Kmeans
    """
    
    X = all_metric.T
    inertias = []
    K = range(1, 10)
    for k in K:
        model = KMeans(n_clusters=k).fit(X)
        model.fit(X)
        inertias.append(model.inertia_)
    plt.plot(K, inertias, 'bx-')
    plt.xlabel('Values of K')
    plt.ylabel('Inertia')
    plt.title('The Elbow Method using Inertia')
    plt.show()
    return


def PCA_explained_variance(all_metric):
    
    """
        Plot la variance expliquée par PCA 
    """
    
    X = all_metric.T
    pca = PCA(n_components=10)
    data = pca.fit_transform(X)
    x = [0]
    y = [0]
    value = 0
    for i in range(len(pca.explained_variance_ratio_)):
        print("Variance", pca.explained_variance_ratio_[i])
        value += pca.explained_variance_ratio_[i]
        x.append(i+1)
        y.append(value)
    plt.figure(figsize=(10, 10))
    plt.plot(x, y, marker='o')
    plt.xlim(-0.5)
    plt.ylim(-0.2, 1)
    plt.title('Explained Variance by Components')
    plt.xlabel('Number of Components')
    plt.ylabel('Cumulative Explained Variance')
    plt.show()
    return


def get_PCA_Kmeans(all_metric, nb_cluster):
    
    """
        Algorithme Kmeans implementé avec PCA au préalable
    """   
    
    X = all_metric.T
    pca = PCA(n_components=2)
    data = pca.fit_transform(X)
    model = KMeans(n_clusters=nb_cluster, init="k-means++")
    y = model.fit_predict(data)
    uniq = np.unique(y)
    for i in uniq:
        plt.scatter(data[y == i, 0], data[y == i, 1])
    centers = np.array(model.cluster_centers_)
    plt.scatter(centers[:, 0], centers[:, 1], marker="x", color='k')
    plt.xlabel('Principal component 1')
    plt.ylabel('Principal component 2')
    plt.legend()
    plt.show()
    return y


def get_PCA_Standard_Kmeans(all_metric, nb_cluster):
    
    """
        Algorithme Kmeans implementé avec PCA et Standardisation au préalable
    """
    
    X = all_metric.T
    scaler = StandardScaler()
    data_std = scaler.fit_transform(X)
    pca = PCA(n_components=3)
    pca.fit(data_std)
    scores = pca.transform(data_std)
    model = KMeans(n_clusters=nb_cluster, init="k-means++")
    y = model.fit(scores)
    data_pca_kmean = pd.DataFrame(
        scores, columns=['Component 1', 'Component 2', 'Component 3'])
    clusters_assignation = np.zeros(len(X))
    col_cluster_assi = pd.DataFrame(
        clusters_assignation, columns=['Cluster Assignation'])
    df = pd.concat([data_pca_kmean, col_cluster_assi], axis=1)
    df['Cluster Assignation'] = model.labels_
    plt.figure(figsize=(15, 15))
    sns.scatterplot(x=df['Component 1'], y=df['Component 2'],
                    hue=df['Cluster Assignation'])
    plt.show()
    return df['Cluster Assignation']



"""
    ANALYSE TYPE I
"""

patient_numbers_typeI = ["02","04","08","09","11","13","15","17","18","19","20","22","26","31","32","33","35","37","39","42","43","45","48","50","51"]

def get_all_metric_typeI(file_path, patient_numbers, nb_atlas):
    
    """
        Analyse de type I : 
            Patient est enlevé si le préprocessing à attribuer une valeur de 0 à une région du cerveau
    """
    
    nb_metrics = len(file_path) #Nombre de metrics utilisées
    percentage_change_all = np.zeros((nb_atlas, len(patient_numbers)))
    all_metric = np.zeros((nb_atlas*nb_metrics, len(patient_numbers)))

    for metric, j in zip(file_path, range(nb_metrics)):
        for patient_nb, i in zip(patient_numbers, range(len(patient_numbers))):
            worksheet = pd.read_excel(metric, sheet_name=patient_nb)
            worksheet = worksheet.to_numpy()
            worksheet = np.nan_to_num(worksheet)
            # a = np.nan_to_num(worksheet[:,0]) #Atlas name
            
            for atlas in range(nb_atlas):
                b = np.nan_to_num(worksheet[atlas,1]) #Mean E1
                c = np.nan_to_num(worksheet[atlas,2]) #Mean E2
                d = np.nan_to_num(worksheet[atlas,3]) #Mean E3
                e = np.nan_to_num(worksheet[atlas,4]) #Percentage change (Value not loaded because of the formula, so it must be recalculated)
                if b == 0:
                    percentage_change_all[atlas,i] = 0
                else:
                    percentage_change_all[atlas,i] = np.nan_to_num((c-b)*100/b)

        start = j*nb_atlas
        stop = nb_atlas+j*nb_atlas
        all_metric[start:(stop),:] = percentage_change_all
    return all_metric

all_metric_DTI = get_all_metric_typeI([mean_ROI_AD, mean_ROI_FA, mean_ROI_MD, mean_ROI_RD], patient_numbers_typeI, 141)
all_metric_NODDI = get_all_metric_typeI([mean_ROI_noddi_fextra, mean_ROI_noddi_fintra, mean_ROI_noddi_fiso, mean_ROI_noddi_odi], patient_numbers_typeI, 88)
all_metric_DIAMOND1 = get_all_metric_typeI([mean_ROI_diamond_fractions_csf, mean_ROI_diamond_fraction_ftot], patient_numbers_typeI, 88)
all_metric_DIAMOND2 = get_all_metric_typeI([mean_ROI_wAD, mean_ROI_wFA, mean_ROI_wMD, mean_ROI_wRD], patient_numbers_typeI, 88)
all_metric_MF = get_all_metric_typeI([mean_ROI_mf_frac_csf, mean_ROI_mf_frac_ftot, mean_ROI_mf_fvf_tot, mean_ROI_mf_wfvf], patient_numbers_typeI, 88)

all_metric_DTI_NODDI = np.append(all_metric_DTI, all_metric_NODDI, axis=0)
all_metric_DIAMOND = np.append(all_metric_DIAMOND2, all_metric_DIAMOND1, axis=0)
all_metric_DTI_NODDI_DIAMOND = np.append(all_metric_DTI_NODDI, all_metric_DIAMOND, axis=0)
all_metric_together_typeI = np.append(all_metric_DTI_NODDI_DIAMOND, all_metric_MF, axis=0)
print("Metrics type I Done !")

elbow_graph(all_metric_together_typeI)
nb_cluster_typeI = 3
ypred_typeI = get_kmeans(all_metric_together_typeI, nb_cluster_typeI)
clusters_typeI = get_cluster(ypred_typeI, patient_numbers_typeI, nb_cluster_typeI)
print(clusters_typeI)

PCA_explained_variance(all_metric_together_typeI)
yV1 = get_PCA_Kmeans(all_metric_together_typeI, nb_cluster_typeI)
clusters_typeI = get_cluster(yV1, patient_numbers_typeI, nb_cluster_typeI)
print(clusters_typeI)

yV2 = get_PCA_Standard_Kmeans(all_metric_together_typeI, nb_cluster_typeI)
clusters_typeI = get_cluster(yV2, patient_numbers_typeI, nb_cluster_typeI)
print(clusters_typeI)


"""
    ANALYSE TYPE II
"""

patient_numbers_typeII = ["01","02","04","05","08","09","11","12","13","14","15","17","18","19","20","21","22","24","26","27","28","29","30","31","32","33","34","35","36","37","39","40","41","42","43","45","46","48","50","51","52","53"]

def get_all_metric_typeII(file_path, patient_numbers, nb_atlas):
    
    """
        Analyse de type II : 
            Région est enlevée si ​le préprocessing à attribuer une valeur de 0 à une région du cerveau 
    ​"""
    
    nb_metrics = len(file_path)
    dic = {} #contient les zones du cerveau que l'on retire de l'étude car données manquantes
    for metric, j in zip(file_path, range(nb_metrics)):
        for patient_nb, i in zip(patient_numbers, range(len(patient_numbers))):
            worksheet = pd.read_excel(metric, sheet_name=patient_nb)
            worksheet = worksheet.to_numpy()
            worksheet = np.nan_to_num(worksheet)
            a = np.nan_to_num(worksheet[:,0])  #Atlas name
            b = np.nan_to_num(worksheet[:,1])  #Mean at E1
            c = np.nan_to_num(worksheet[:,2])  #Mean at E2
            d = np.nan_to_num(worksheet[:,3])  #Mean at E3
            #e = np.nan_to_num(worksheet[:,4])  #Percentage change bewteen E2 and E1
            for k in range(len(a)) :
                if (b[k]==0 or c[k]==0):
                    key = a[k]
                    if key not in dic.keys():
                        dic[key] = [patient_nb]
                    else:
                        if patient_nb not in dic[key]:
                            dic[key].append(patient_nb)
    #print(dic.keys())
    regions_out = len(dic)
    nb_regions = nb_atlas - regions_out

    percentage_change_all = np.zeros((nb_regions, len(patient_numbers)))
    all_metric = np.zeros((nb_regions*nb_metrics, len(patient_numbers)))
    for metric, j in zip(file_path, range(nb_metrics)):
        for patient_nb, i in zip(patient_numbers, range(len(patient_numbers))):
            worksheet = pd.read_excel(metric, sheet_name=patient_nb)
            worksheet = worksheet.to_numpy()
            worksheet = np.nan_to_num(worksheet)
            a = np.nan_to_num(worksheet[:,0])  #Atlas name
            b = np.nan_to_num(worksheet[:,1])  #Mean at E1
            c = np.nan_to_num(worksheet[:,2])  #Mean at E2
            d = np.nan_to_num(worksheet[:,3])  #Mean at E3
            value = 0
            for k in range(len(a)):
                key = a[k]
                if key in dic.keys():
                    value +=1
                if key not in dic.keys():
                    percentage_change_all[k-value,i] = (worksheet[k,1]-worksheet[k,2])*100/worksheet[k,1]
        start = j*nb_regions
        stop = nb_regions+j*nb_regions
        all_metric[start:(stop),:] = percentage_change_all
        
    return all_metric

all_metric_DTI = get_all_metric_typeII([mean_ROI_AD, mean_ROI_FA, mean_ROI_MD, mean_ROI_RD], patient_numbers_typeII, 141)
all_metric_NODDI = get_all_metric_typeII([mean_ROI_noddi_fextra, mean_ROI_noddi_fintra, mean_ROI_noddi_fiso, mean_ROI_noddi_odi], patient_numbers_typeII, 88)
all_metric_DIAMOND1 = get_all_metric_typeII([mean_ROI_diamond_fractions_csf, mean_ROI_diamond_fraction_ftot], patient_numbers_typeII, 88)
all_metric_DIAMOND2 = get_all_metric_typeII([mean_ROI_wAD, mean_ROI_wFA, mean_ROI_wMD, mean_ROI_wRD], patient_numbers_typeII, 88)
all_metric_MF = get_all_metric_typeII([mean_ROI_mf_frac_csf, mean_ROI_mf_frac_ftot, mean_ROI_mf_fvf_tot, mean_ROI_mf_wfvf], patient_numbers_typeII, 88)

all_metric_DTI_NODDI = np.append(all_metric_DTI, all_metric_NODDI, axis=0)
all_metric_DIAMOND = np.append(all_metric_DIAMOND2, all_metric_DIAMOND1, axis=0)
all_metric_DTI_NODDI_DIAMOND = np.append(all_metric_DTI_NODDI, all_metric_DIAMOND, axis=0)
all_metric_together_typeII = np.append(all_metric_DTI_NODDI_DIAMOND, all_metric_MF, axis=0)
print("Metrics type II Done !")

elbow_graph (all_metric_together_typeII)
nb_cluster_typeII = 3
ypred_typeII = get_kmeans(all_metric_together_typeII, nb_cluster_typeII)
clusters_typeII = get_cluster(ypred_typeII, patient_numbers_typeII, nb_cluster_typeII)
print(clusters_typeII)
PCA_explained_variance(all_metric_together_typeII)

yV3 = get_PCA_Kmeans(all_metric_together_typeII, nb_cluster_typeII)
clusters_typeII = get_cluster(yV3, patient_numbers_typeII, nb_cluster_typeII)
print(clusters_typeII)
yV4 = get_PCA_Standard_Kmeans(all_metric_together_typeII, nb_cluster_typeII)
clusters_typeII = get_cluster(yV4, patient_numbers_typeII, nb_cluster_typeII)
print(clusters_typeII)


"""
    ANALYSE TYPE III
"""

patient_numbers_typeIII = ["01","02","04","05","08","09","11","12","13","14","15","17","18","19","20","21","22","24","26","27","28","29","30","31","32","33","34","35","36","37","39","40","41","42","43","45","46","48","50","51","52","53"]

def get_all_metric_typeIII(file_path, patient_numbers, nb_atlas):
    
    """
        Analyse de type III: 
            Région est enlevée si ​plus de 10% de la population (soit 5 patients) 
            voit le préprocessing attribuer une valeur de 0 ​à une région du cerveau
            sinon valeur de la région est remplacée par la moyenne sur le reste de la population 
    ​"""
    
    nb_metrics = len(file_path)
    dic = {}  # contient les zones du cerveau que l'on retire de l'étude car données manquantes
    for metric, j in zip(file_path, range(nb_metrics)):
        for patient_nb, i in zip(patient_numbers, range(len(patient_numbers))):
            worksheet = pd.read_excel(metric, sheet_name=patient_nb)
            worksheet = worksheet.to_numpy()
            worksheet = np.nan_to_num(worksheet)
            a = np.nan_to_num(worksheet[:, 0])  # Atlas name
            b = np.nan_to_num(worksheet[:, 1])  # Mean at E1
            c = np.nan_to_num(worksheet[:, 2])  # Mean at E2
            d = np.nan_to_num(worksheet[:, 3])  # Mean at E3
            # e = np.nan_to_num(worksheet[:,4])  #Percentage change bewteen E2 and E1
            for k in range(len(a)):
                if (b[k] == 0 or c[k] == 0):
                    key = a[k]
                    if key not in dic.keys():
                        dic[key] = [patient_nb]
                    else:
                        if patient_nb not in dic[key]:
                            dic[key].append(patient_nb)
    # print(dic)
    regions_out = 0
    lst_out = []
    lst_in = []
    for key, value in dic.items():
        if len(value) > 5:
            regions_out += 1
            lst_out.append(key)
        else:
            lst_in.append(key)
    #print("lst_in", lst_in)
    print("lst_out", lst_out)

    dic_in = {}
    for i in lst_in:
        dic_in[i] = 0

    for metric, j in zip(file_path, range(nb_metrics)):
        for patient_nb, i in zip(patient_numbers, range(len(patient_numbers))):
            worksheet = pd.read_excel(metric, sheet_name=patient_nb)
            worksheet = worksheet.to_numpy()
            worksheet = np.nan_to_num(worksheet)
            a = np.nan_to_num(worksheet[:, 0])  # Atlas name
            b = np.nan_to_num(worksheet[:, 1])  # Mean at E1
            c = np.nan_to_num(worksheet[:, 2])  # Mean at E2
            d = np.nan_to_num(worksheet[:, 3])  # Mean at E3
            # e = np.nan_to_num(worksheet[:,4])  #Percentage change bewteen E2 and E1
            for k in range(len(a)):
                key = a[k]
                if key in lst_in:
                    if patient_nb not in dic[key]:
                        dic_in[key] += (b[k]-c[k])*100/b[k]

        for i in lst_in:
            longueur = len(patient_numbers)-len(dic[i])
            dic_in[i] /= longueur

    nb_regions = nb_atlas - regions_out
    percentage_change_all = np.zeros((nb_regions, len(patient_numbers)))
    all_metric = np.zeros((nb_regions*nb_metrics, len(patient_numbers)))
    for metric, j in zip(file_path, range(nb_metrics)):
        for patient_nb, i in zip(patient_numbers, range(len(patient_numbers))):
            worksheet = pd.read_excel(metric, sheet_name=patient_nb)
            worksheet = worksheet.to_numpy()
            worksheet = np.nan_to_num(worksheet)
            a = np.nan_to_num(worksheet[:, 0])  # Atlas name
            b = np.nan_to_num(worksheet[:, 1])  # Mean at E1
            c = np.nan_to_num(worksheet[:, 2])  # Mean at E2
            d = np.nan_to_num(worksheet[:, 3])  # Mean at E3
            value = 0
            for k in range(len(a)):
                key = a[k]
                if key in dic.keys():
                    if key not in dic_in.keys():
                        value += 1
                    if key in dic_in.keys():
                        if patient_nb in dic[key]:
                            percentage_change_all[k-value, i] = dic_in[key]
                        else:
                            percentage_change_all[k-value, i] = (
                                worksheet[k, 1]-worksheet[k, 2])*100/worksheet[k, 1]
                else:
                    percentage_change_all[k-value, i] = (
                        worksheet[k, 1]-worksheet[k, 2])*100/worksheet[k, 1]
        start = j*nb_regions
        stop = nb_regions+j*nb_regions
        all_metric[start:(stop), :] = percentage_change_all
    return all_metric

all_metric_DTI = get_all_metric_typeIII([mean_ROI_AD, mean_ROI_FA, mean_ROI_MD, mean_ROI_RD], patient_numbers_typeIII, 141)
all_metric_NODDI = get_all_metric_typeIII([mean_ROI_noddi_fextra, mean_ROI_noddi_fintra, mean_ROI_noddi_fiso, mean_ROI_noddi_odi], patient_numbers_typeIII, 88)
all_metric_DIAMOND1 = get_all_metric_typeIII([mean_ROI_diamond_fractions_csf, mean_ROI_diamond_fraction_ftot], patient_numbers_typeIII, 88)
all_metric_DIAMOND2 = get_all_metric_typeIII([mean_ROI_wAD, mean_ROI_wFA, mean_ROI_wMD, mean_ROI_wRD], patient_numbers_typeIII, 88)
all_metric_MF = get_all_metric_typeIII([mean_ROI_mf_frac_csf, mean_ROI_mf_frac_ftot, mean_ROI_mf_fvf_tot, mean_ROI_mf_wfvf], patient_numbers_typeIII, 88)

all_metric_DTI_NODDI = np.append(all_metric_DTI, all_metric_NODDI, axis=0)
all_metric_DIAMOND = np.append(all_metric_DIAMOND2, all_metric_DIAMOND1, axis=0)
all_metric_DTI_NODDI_DIAMOND = np.append(all_metric_DTI_NODDI, all_metric_DIAMOND, axis=0)
all_metric_together_typeIII = np.append(all_metric_DTI_NODDI_DIAMOND, all_metric_MF, axis=0)
print("Metrics type III Done !")

elbow_graph (all_metric_together_typeIII)
nb_cluster_typeIII = 3
ypred_typeIII = get_kmeans(all_metric_together_typeIII, nb_cluster_typeIII)
clusters_typeIII = get_cluster(ypred_typeIII, patient_numbers_typeIII, nb_cluster_typeIII)

PCA_explained_variance(all_metric_together_typeIII)
yV5 = get_PCA_Kmeans(all_metric_together_typeIII, nb_cluster_typeIII)
clusters_typeIII = get_cluster(yV5, patient_numbers_typeIII, nb_cluster_typeIII)

yV6 = get_PCA_Standard_Kmeans(all_metric_together_typeIII, nb_cluster_typeIII)
clusters_typeIII = get_cluster(yV6, patient_numbers_typeIII, nb_cluster_typeIII)


""" 
    Analyse comportementale 
"""

patient_with_data_comp = ["02", "04", "05", "08", "09", "11", "12", "13", "14", "15", "17", "18", "19", "20", "21", "22", "24", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "39", "40", "41", "42", "43", "45", "46", "47", "48", "50", "51", "52", "53"]

behavior = path + r'Comportements_data.xlsx'
print("La taille du dataset des comportements pour un patient est de", pd.read_excel(behavior).shape)
file_path = path + r'Behavior_data.xlsx'


def get_comportements(file_path, patient_list):
    
    worksheet = pd.read_excel(file_path)
    tabular = worksheet.to_numpy()
    patients_all = []

    for i in patient_list:
        for j in range(len(worksheet["Numéro"])):
            if (int(i) == worksheet["Numéro"][j]):
                patients_all.append(tabular[j, :])
                
    return patients_all


def comportement_to_excel(patients_all):
    
    workbook = xlsxwriter.Workbook(path + 'Behavior_data.xlsx')
    patient_data = patients_all.copy()
    for i in patient_data:
        if(i[0] == 2 or i[0] == 4 or i[0] == 5 or i[0] == 8 or i[0] == 9):
            worksheet = workbook.add_worksheet("0" + str(int(i[0])))
        else:
            worksheet = workbook.add_worksheet(str(int(i[0])))
        list_data = ["Unités", "Osmolalité", "T1_BDI", "T1_OCDS_MODIFIE_Total", "T1_OCDS_Obsessions", "T1_OCDS_Compulsions", "T1_STAI_YA", "T1_MFI",
                     "T2_Bearni", "T2_BDI", "T2_OCDS_MODIFIE_Total", "T2_OCDS_Obsessions", "T2_OCDS_Compulsions", "T2_STAI_YA", "T2_MFI",
                     "Percentage BDI", "Percentage OCDS_MODIFIE_Total", "Percentage OCDS_Obsessions", "Percentage OCDS_Compulsions", "Percentage STAI_YA", "Percentage MFI"]
        azer = 2
        start = 1
        for j, k in zip(range(start, len(i)), list_data):
            worksheet.write('A'+str(azer), k)
            if(i[j] != "/"):
                if(np.isnan(i[j]) == True):
                    i[j] = 0
            else:
                i[j] = -1
            worksheet.write('B'+str(azer), i[j])
            azer += 1
    workbook.close()
    return


def get_all_comportements(file_path, patient_numbers, nb_param):
    
    """
        Analyse de comportement : 
            paramètre est enlevé si ​plus de 10% de la population (soit 5 patients) 
            n'ont pas de valeur 
            sinon valeur du paramètre est remplacée par la moyenne sur le reste de la population 
    ​"""
    
    dic = {}
    for patient_nb, i in zip(patient_numbers, range(len(patient_numbers))):
        worksheet = pd.read_excel(file_path, sheet_name=patient_nb)
        worksheet = worksheet.to_numpy()
        a = np.nan_to_num(worksheet[:, 0])  # Params
        b = np.nan_to_num(worksheet[:, 1])  # Valeurs
        for k in range(len(a)-6):
            if (b[k] == -1):
                key = a[k]
                if key not in dic.keys():
                    dic[key] = [patient_nb]
                else:
                    if patient_nb not in dic[key]:
                        dic[key].append(patient_nb)
    # print(dic)
    param_out = 0
    lst_out = []
    lst_in = []
    for key, value in dic.items():
        if len(value) > 5:
            param_out += 1
            lst_out.append(key)
        else:
            lst_in.append(key)
    print("lst_in", lst_in)
    print("lst_out", lst_out)

    dic_in = {}
    for i in lst_in:
        dic_in[i] = 0

    for patient_nb, i in zip(patient_numbers, range(len(patient_numbers))):
        worksheet = pd.read_excel(file_path, sheet_name=patient_nb)
        worksheet = worksheet.to_numpy()
        a = np.nan_to_num(worksheet[:, 0])  # Params
        b = np.nan_to_num(worksheet[:, 1])  # Valeurs
        for k in range(len(a)-6):
            key = a[k]
            if key in lst_in:
                if patient_nb not in dic[key]:
                    if key == 'Unités':
                        dic_in[key] += b[0]
                    if key == 'Osmolalité':
                        dic_in[key] += b[1]
                    if key == 'T1_BDI':
                        dic_in[key] += b[2]
                    if key == 'T1_OCDS_MODIFIE_Total':
                        dic_in[key] += b[3]
                    if key == 'T1_OCDS_Obsessions':
                        dic_in[key] += b[4]
                    if key == 'T1_OCDS_Compulsions':
                        dic_in[key] += b[5]
                    if key == 'T1_STAI_YA':
                        dic_in[key] += b[6]
                    if key == 'T1_MFI':
                        dic_in[key] += b[7]
                    if key == 'T2_Bearni':
                        dic_in[key] += b[8]
                    if key == 'T2_BDI':
                        dic_in[key] += b[9]
                    if key == 'T2_OCDS_MODIFIE_Total':
                        dic_in[key] += b[10]
                    if key == 'T2_OCDS_Obsessions':
                        dic_in[key] += b[11]
                    if key == 'T2_OCDS_Compulsions':
                        dic_in[key] += b[12]
                    if key == 'T2_STAI_YA':
                        dic_in[key] += b[13]
                    if key == 'T2_MFI':
                        dic_in[key] += b[14]

    print("dic_in", dic_in)
    nb_regions = nb_param - param_out
    for i in lst_in:
        longueur = len(patient_numbers)-len(dic[i])
        dic_in[i] /= longueur
        #print(i , dic_in[i])
    metric_all = np.zeros((nb_regions, len(patient_numbers)))
    for patient_nb, i in zip(patient_numbers, range(len(patient_numbers))):
        worksheet = pd.read_excel(file_path, sheet_name=patient_nb)
        worksheet = worksheet.to_numpy()
        a = np.nan_to_num(worksheet[:, 0])  # Params
        b = np.nan_to_num(worksheet[:, 1])  # Valeurs
        value = 0
        for k in range(len(a)-6-6):
            key = a[k]
            if k == 0 or k == 1:
                if key in dic.keys():
                    if key not in dic_in.keys():
                        value += 1
                    if key in dic_in.keys():
                        if patient_nb in dic[key]:
                            metric_all[k-value, i] = dic_in[key]
                else:
                    metric_all[k-value, i] = b[k]

            if k > 1:
                key2 = a[k+7]
                if key in dic.keys() and key2 in dic.keys():
                    if key in dic_in.keys() and key2 in dic_in.keys():
                        if patient_nb in dic[key] and patient_nb in dic[key2]:
                            metric_all[k-value,
                                       i] = (dic_in[key]-dic_in[key2])*100/dic_in[key]
                        if patient_nb in dic[key]:
                            metric_all[k-value,
                                       i] = (dic_in[key]-b[k+7])*100/dic_in[key]
                        if patient_nb in dic[key2]:
                            if b[k] != 0:
                                metric_all[k-value,
                                           i] = (b[k]-dic_in[key2])*100/b[k]
                            else:
                                metric_all[k-value,
                                           i] = (b[k]-dic_in[key2])*100/30
                        else:
                            if b[k] != 0:
                                metric_all[k-value, i] = (b[k]-b[k+7])*100/b[k]
                            else:
                                metric_all[k-value, i] = (b[k]-b[k+7])*100/30
                    if key in dic_in.keys():
                        if patient_nb in dic[key]:
                            metric_all[k-value,
                                       i] = (dic_in[key]-b[k+7])*100/dic_in[key]
                        else:
                            if b[k] != 0:
                                metric_all[k-value, i] = (b[k]-b[k+7])*100/b[k]
                            else:
                                metric_all[k-value, i] = (b[k]-b[k+7])*100/30
                    if key2 in dic_in.keys():
                        if patient_nb in dic[key2]:
                            if b[k] != 0:
                                metric_all[k-value,
                                           i] = (b[k]-dic_in[key2])*100/b[k]
                            else:
                                metric_all[k-value,
                                           i] = (b[k]-dic_in[key2])*100/30
                        else:
                            if b[k] != 0:
                                metric_all[k-value, i] = (b[k]-b[k+7])*100/b[k]
                            else:
                                metric_all[k-value, i] = (b[k]-b[k+7])*100/30
                    else:
                        value += 1

                if key in dic.keys():
                    if key in dic_in.keys():
                        if patient_nb in dic[key]:
                            metric_all[k-value,
                                       i] = (dic_in[key]-b[k+7])*100/dic_in[key]
                        else:
                            if b[k] != 0:
                                metric_all[k-value, i] = (b[k]-b[k+7])*100/b[k]
                            else:
                                metric_all[k-value, i] = (b[k]-b[k+7])*100/30
                    else:
                        value += 1
                if key2 in dic.keys():
                    if key2 in dic_in.keys():
                        if patient_nb in dic[key2]:
                            if b[k] != 0:
                                metric_all[k-value,
                                           i] = (b[k]-dic_in[key2])*100/b[k]
                            else:
                                metric_all[k-value,
                                           i] = (b[k]-dic_in[key2])*100/30
                        else:
                            if b[k] != 0:
                                metric_all[k-value, i] = (b[k]-b[k+7])*100/b[k]
                            else:
                                metric_all[k-value, i] = (b[k]-b[k+7])*100/30
                    else:
                        value += 1
                else:
                    if b[k] != 0:
                        metric_all[k-value, i] = (b[k]-b[k+7])*100/b[k]
                    else:
                        metric_all[k-value, i] = (b[k]-b[k+7])*100/30
    return metric_all


patients_all = get_comportements(behavior, patient_with_data_comp)
comportement_to_excel(patients_all)
a = get_all_comportements(file_path, patient_with_data_comp, 9)
print("a is done")

nb_cluster_comp = 3
y = get_kmeans(a, nb_cluster_comp)
clusters_comp = get_cluster(y, patient_with_data_comp, nb_cluster_comp)
print(clusters_comp)

yV1 = get_PCA_Kmeans(a, nb_cluster_comp)
clusters_comp = get_cluster(yV1, patient_with_data_comp, nb_cluster_comp)
print(clusters_comp)

yV2 = get_PCA_Standard_Kmeans(a, nb_cluster_comp)
clusters_comp = get_cluster(yV2, patient_with_data_comp, nb_cluster_comp)
print(clusters_comp)



""" 
    Analyse TOUT ensemble : diffusion et comportementale 
"""

patient_ALL = ["02", "04", "05", "08", "09", "11", "12", "13", "14", "15", "17", "18", "19", "20", "21", "22", "24", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "39", "40", "41", "42", "43", "45", "46", "48", "50", "51", "52", "53"]

all_metric_DTI = get_all_metric_typeIII([mean_ROI_AD, mean_ROI_FA, mean_ROI_MD, mean_ROI_RD], patient_ALL, 141)
all_metric_NODDI = get_all_metric_typeIII([mean_ROI_noddi_fextra, mean_ROI_noddi_fintra, mean_ROI_noddi_fiso, mean_ROI_noddi_odi], patient_ALL, 88)
all_metric_DIAMOND1 = get_all_metric_typeIII([mean_ROI_diamond_fractions_csf, mean_ROI_diamond_fraction_ftot], patient_ALL, 88)
all_metric_DIAMOND2 = get_all_metric_typeIII([mean_ROI_wAD, mean_ROI_wFA, mean_ROI_wMD, mean_ROI_wRD], patient_ALL, 88)
all_metric_MF = get_all_metric_typeIII([mean_ROI_mf_frac_csf, mean_ROI_mf_frac_ftot, mean_ROI_mf_fvf_tot, mean_ROI_mf_wfvf], patient_ALL, 88)

all_metric_DTI_NODDI = np.append(all_metric_DTI, all_metric_NODDI, axis=0)
all_metric_DIAMOND = np.append(all_metric_DIAMOND2, all_metric_DIAMOND1, axis=0)
all_metric_DTI_NODDI_DIAMOND = np.append(all_metric_DTI_NODDI, all_metric_DIAMOND, axis=0)
all_metric_together_typeIII = np.append(all_metric_DTI_NODDI_DIAMOND, all_metric_MF, axis=0)
print("Metric diffusion is done")

patients_all = get_comportements(behavior, patient_ALL)
comportement_to_excel(patients_all)
a = get_all_comportements(file_path, patient_ALL, 9)
print("Metric comportementale is done")

ALL = np.append(all_metric_together_typeIII, a, axis=0)
print("Metric ALL is done")

nb_cluster_ALL = 3
y = get_kmeans(ALL, nb_cluster_ALL)
clusters_ALL = get_cluster(y, patient_ALL, nb_cluster_ALL)
print(clusters_ALL)

yV1 = get_PCA_Kmeans(ALL, nb_cluster_ALL)
clusters_ALL = get_cluster(yV1, patient_ALL, nb_cluster_ALL)
print(clusters_ALL)

yV2 = get_PCA_Standard_Kmeans(ALL, nb_cluster_ALL)
clusters_ALL = get_cluster(yV2, patient_ALL, nb_cluster_ALL)
print(clusters_ALL)


""" 
    Analyse TOUT ensemble : diffusion et comportementale SANS OUTLIERS 
"""

patient_without_outliers = []
outliers = ["02", "04", "05", "17", "29", "30", "35"]

for elem in patient_ALL:
    if elem not in outliers:
        patient_without_outliers.append(elem)

all_metric_DTI = get_all_metric_typeIII([mean_ROI_AD, mean_ROI_FA, mean_ROI_MD, mean_ROI_RD], patient_without_outliers, 141)
all_metric_NODDI = get_all_metric_typeIII([mean_ROI_noddi_fextra, mean_ROI_noddi_fintra, mean_ROI_noddi_fiso, mean_ROI_noddi_odi], patient_without_outliers, 88)
all_metric_DIAMOND1 = get_all_metric_typeIII([mean_ROI_diamond_fractions_csf, mean_ROI_diamond_fraction_ftot], patient_without_outliers, 88)
all_metric_DIAMOND2 = get_all_metric_typeIII([mean_ROI_wAD, mean_ROI_wFA, mean_ROI_wMD, mean_ROI_wRD], patient_without_outliers, 88)
all_metric_MF = get_all_metric_typeIII([mean_ROI_mf_frac_csf, mean_ROI_mf_frac_ftot, mean_ROI_mf_fvf_tot, mean_ROI_mf_wfvf], patient_without_outliers, 88)

all_metric_DTI_NODDI = np.append(all_metric_DTI, all_metric_NODDI, axis=0)
all_metric_DIAMOND = np.append( all_metric_DIAMOND2, all_metric_DIAMOND1, axis=0)
all_metric_DTI_NODDI_DIAMOND = np.append( all_metric_DTI_NODDI, all_metric_DIAMOND, axis=0)
all_metric_together_typeIII = np.append( all_metric_DTI_NODDI_DIAMOND, all_metric_MF, axis=0)
print("Metric diffusion is done")

# elbow_graph(all_metric_together_typeIII)

patients_all = get_comportements(behavior, patient_without_outliers)
comportement_to_excel(patients_all)
a = get_all_comportements(file_path, patient_without_outliers, 9)
print("Metric comportementale is done")

ALL_without_outliers = np.append(all_metric_together_typeIII, a, axis=0)
print("Metric ALL is done")

nb_cluster_ALL = 3   ### 3 
y = get_kmeans(ALL_without_outliers, nb_cluster_ALL)
clusters_ALL = get_cluster(y, patient_without_outliers, nb_cluster_ALL)
print(clusters_ALL)

yV1 = get_PCA_Kmeans(ALL_without_outliers, nb_cluster_ALL)
clusters_ALL = get_cluster(yV1, patient_without_outliers, nb_cluster_ALL)
print(clusters_ALL)

yV2 = get_PCA_Standard_Kmeans(ALL_without_outliers, nb_cluster_ALL)
clusters_ALL = get_cluster(yV2, patient_without_outliers, nb_cluster_ALL)
print(clusters_ALL)


""" 
    Correlations entre données de diffusion et comportementales 
"""

def plot_correlation (IRM_data, COMP_data):
    
    """
        Plotter les correlations entre les données de diffusion et les données comportementales 
    """
    
    matrix = np.concatenate((IRM_data, COMP_data), axis=0)
    X = matrix.T
    name1 = []
    
    for i in range(len(IRM_data)): 
        name1.append(str(i))
        
    name2 = ["Unités", "Osmolalité", "BDI", "OCDS_modifie_Total", "Obsessions", "Compulsions", "STAI_YA", "MFI", "T2_Bearni"]
    names = []
    names.extend(name1)
    names.extend(name2)
    data = pd.DataFrame(X, columns =names)
    corr_data = data.corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_data[len(matrix)-len(COMP_data): len(matrix)])
    plt.xlim(0, len(IRM_data))
    plt.show()
    
    return

plot_correlation(all_metric_together_typeIII, a) 