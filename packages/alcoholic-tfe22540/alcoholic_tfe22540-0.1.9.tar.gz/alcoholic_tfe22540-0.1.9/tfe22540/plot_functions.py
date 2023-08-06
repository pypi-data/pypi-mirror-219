"""
Created on Fri Mar 18 09:45:14 2022

@author: Fauston
"""

import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D

from tfe22540.perso_path import perso_path_string


perso_path, excel_path, subjects_path, patients_path, plot_path, atlas_path = perso_path_string() 


# =============================================================================
# DTI
# =============================================================================

def histo_hori(mean_atlas_corr, names_corr, color, namefig, title, display, save):
    if (display == True): 
        plt.style.use('seaborn')
        fig, ax = plt.subplots(figsize = (14.5,8))
        ax.grid(axis = 'x', linestyle = '--')
        ax.grid(axis = 'y', linestyle = '--')
        ax.set_title(title)
        ax.barh(range(len(mean_atlas_corr)), width = mean_atlas_corr, tick_label = names_corr, color = color)
        ax.set_ylim(-1,len(mean_atlas_corr))
        ax.set_xlabel('Variation [%]')
        fig.tight_layout()

    if (save == True):
        fig.savefig(plot_path + namefig + ".pdf")
   
    
def boxplot_dti(df, namefig, title, display, save):
    if (display == True):
        plt.style.use('seaborn')
        fig, ax = plt.subplots()
        ax.set_title(title)
        
        if(len(df.index) != 0):
            ax.grid(axis = 'x', linestyle = '--')
            ax.grid(axis = 'y', linestyle = '--')
            ax.boxplot(np.array(df).T, labels = df.index, vert = False)    
            ax.set_xlabel('Variation [%]')
            
        fig.tight_layout() 

    if (save == True):
        fig.savefig(plot_path + namefig + ".pdf")
    
    
# =============================================================================
# NODDI
# =============================================================================

def histo_multicomp(noddi_means, noddi_names, namefig, title, lab, display, save):
    if (display == True): 
        plt.style.use('seaborn')
        fig, ax = plt.subplots(figsize = (14.5,8))
        ax.grid(axis = 'x',linestyle = '--')
        ax.set_title(title)

        indent = 0
        for i in range(noddi_means.shape[1]):
            if indent == 0:
                ax.bar(np.arange(noddi_means.shape[0]) + indent, noddi_means[:,i], tick_label = noddi_names, width = 0.25)
            else: 
                ax.bar(np.arange(noddi_means.shape[0]) + indent, noddi_means[:,i], width = 0.25)
            indent += 0.25
        
        ax.legend(labels = lab)
        ax.set_ylabel('Variation [%]')
        ax.set_xticks(np.arange(noddi_means.shape[0]))
        ax.set_xticklabels(noddi_names, ha='right', rotation_mode = 'anchor', rotation = 60)
        plt.axhline(y = 0, linestyle = "--", color="gray")
        fig.tight_layout()
        
    if (save == True):
        fig.savefig(plot_path + namefig + ".pdf")


# =============================================================================
# FA
# =============================================================================
def histo_FA_odi(noddi_means, noddi_names, namefig, title, lab, display, save):
    if (display == True): 
        plt.style.use('seaborn')
        fig, ax = plt.subplots(figsize = (14.5,8))
        ax.grid(axis = 'x',linestyle ='--')
        ax.set_title(title)
        
        indent = 0
        for i in range(noddi_means.shape[1]):
            if indent == 0:
                ax.bar(np.arange(noddi_means.shape[0]) + indent, noddi_means[:,i], tick_label = noddi_names, width = 0.25)
            else: 
                ax.bar(np.arange(noddi_means.shape[0]) + indent, noddi_means[:,i], width = 0.25)
            indent += 0.25
    
        ax.legend(labels = lab)
        ax.set_ylabel('Variation [%]')
        ax.set_xlabel('Atlas')
        ax.set_xticks(np.arange(noddi_means.shape[0]))
        ax.set_xticklabels(noddi_names, ha = 'right', rotation_mode = 'anchor', rotation = 60) 
        plt.axhline(y = 0, linestyle = "--", color = "gray")
        fig.tight_layout()
        
    if (save == True):
        fig.savefig(plot_path + namefig + ".pdf")
        
# =============================================================================
# 
# =============================================================================
def plot_all_matter(means, names, colors, namefig, title, display, save):
    labels_noms = []
    colors_label = []
    plt.style.use('seaborn')
    pops = []
    if("coral" in colors):
        labels_noms.append("WM")
        colors_label.append("coral")
        pop_a = mpatches.Patch(color = 'coral', label = 'WM')
        pops.append(pop_a)
    
    if("gold" in colors):
        labels_noms.append("Subcortical")
        colors_label.append("gold")
        pop_a = mpatches.Patch(color = 'gold', label = 'Subcortical')
        pops.append(pop_a)
    
    if("yellowgreen" in colors):
        labels_noms.append("GM")
        colors_label.append("yellowgreen")
        pop_a = mpatches.Patch(color = 'yellowgreen', label = 'GM')
        pops.append(pop_a)
    
    if("dodgerblue" in colors):
        labels_noms.append("Cerebellum")
        colors_label.append("dodgerblue")
        pop_a = mpatches.Patch(color = 'dodgerblue', label = 'Cerebellum')
        pops.append(pop_a)
    
    if("plum" in colors):
        labels_noms.append("Lobes")
        colors_label.append("plum")
        pop_a = mpatches.Patch(color = 'plum', label = 'Lobes')
        pops.append(pop_a)
    
    if (display == True):
        fig, ax = plt.subplots(figsize = (14.5,8))
        ax.grid(axis = 'x',linestyle = '--')
        ax.grid(axis = 'y',linestyle = '--')
        ax.set_title(title)
        ax.tick_params(axis = 'x')
        ax.barh(range(len(means)), width = means, tick_label = names, color = colors)
        ax.set_ylim(-1,len(means))
        ax.set_xlabel('Variation [%]')
        plt.legend(colors_label, labels_noms)
        plt.legend(handles = pops)
        fig.tight_layout()  
        
    if (save == True):
        fig.savefig(plot_path + namefig + ".pdf")
        
        
# =============================================================================
# Cluster plot 
# =============================================================================
def cluster_plot(clusters, name_cluster, colors, get_all_metrics, metric1, atlas1, metric2, atlas2, metric3, atlas3, namefig, title, d3, save):
    pops = []
    plt.close()
    
    if (d3 == True):
        fig = plt.figure(figsize = (15, 12))
        plt.style.use('classic')
        ax = Axes3D(fig, rect = [0, 0, 0.95, 1], elev = 10, azim = 124)
        pops = []
        
        for cluster, couleur, nom_clust in zip(clusters, colors, name_cluster):
            x = []
            y = []
            z = []
            for j in cluster:
                x.append(get_all_metrics[metric1, j]) #metric1
                z.append(get_all_metrics[metric2, j]) #metric2
                y.append(get_all_metrics[metric3, j]) #metric3
            
            ax.scatter(x, y, z, color = couleur, s = 100)
            
            pop_a = mpatches.Patch(color = couleur, label = nom_clust)
            pops.append(pop_a)
            
        ax.legend(handles = pops, fontsize = 12)
        
        ax.set_title(title)
        ax.set_xlabel(atlas1, fontsize = 13)
        ax.set_zlabel(atlas2, fontsize = 13)
        ax.set_ylabel(atlas3, fontsize = 13)
        fig.tight_layout()
        
        if (save == True):
            fig.savefig(plot_path + namefig + ".pdf")
    
    else:
        plt.style.use('seaborn')
        for cluster,couleur,nom_clust in zip(clusters,colors,name_cluster):
            x = []
            y = []
            
            for j in cluster:
                y.append(get_all_metrics[metric1,j]) #metric1
                x.append(get_all_metrics[metric2,j]) #metric2
    
            plt.scatter(x, y, color = couleur)
            pop_a = mpatches.Patch(color = couleur, label = nom_clust)
            pops.append(pop_a)
            plt.xlabel(atlas1)
            plt.ylabel(atlas2)
            plt.title(title)
            plt.legend(handles=pops)
            fig.tight_layout()
            
            if (save == True):
                fig.savefig(plot_path + namefig + ".pdf")