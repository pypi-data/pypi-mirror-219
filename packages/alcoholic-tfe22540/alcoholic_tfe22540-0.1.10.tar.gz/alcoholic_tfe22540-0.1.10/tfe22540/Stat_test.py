"""
Created on Thu Mar 24 14:18:48 2022

@author: Fauston

"""

import numpy as np
import pandas as pd
from scipy import stats


# =============================================================================
# T-TEST FUNCTION
# =============================================================================

def get_ttest(E1, E2, altern):
    
    """
        Parameters
        ----------
        E1 : Dataframe
            Matrix of means at E1.
        E2 : Dataframe
            Matrix of means at E2.
        altern : String
            Type of T-test.
    
        Returns
        -------
        ttest_results_df : Dataframe
            Results of the t-test containing stats and p-values.
        significant : Matrix of int
            Summarizing only the significant results so the ones with a p-value < 0.05.
        E1_bis : List 
            List of significant mean (based on p-value < 0.05) at E1 and their corresponding atlas.
        E2_bis : List 
            List of significant mean (based on p-value < 0.05) at E2 and their corresponding atlas.
    """
    
    atlas_name = E1.index
    E1 = E1.to_numpy()
    E2 = E2.to_numpy()
    E1_bis = []
    E2_bis = []
    ttest_results = np.zeros((E1.shape[0],2)) 
    for i in range(E1.shape[0]):
        tstat, pvalue = stats.ttest_rel(E1[i,:],E2[i,:], alternative = str(altern))
        
        if(pvalue<=0.05):
            E1_bis.append([atlas_name[i],E1[i,:]])
            E2_bis.append([atlas_name[i],E2[i,:]])
        
        
        ttest_results[i,0] = tstat
        ttest_results[i,1] = pvalue
        

    ttest_results_df = pd.DataFrame(ttest_results, columns = ["tstat", "pvalue"]) 
    significant = ttest_results[ttest_results[:,1] <= 0.05] 
    
    return ttest_results_df, significant, E1_bis, E2_bis

