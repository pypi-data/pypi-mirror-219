import numpy as np
from astroquery.sdss import SDSS

# BPT classification

def kauffman(x):
    ## x lim was calculated for a y of -1.5
    return [0.61/(i-0.05) + 1.3 if (i < (0.61/(-1.5-1.3))+0.05) else -np.inf for i in x] 

def kewley(x):
    ## x lim was calculated for a y of -1.5 
    return [0.61/(i-0.47) + 1.19 if (i < (0.61/(-1.5-1.19))+0.47) else -np.inf for i in x]

def query_table(query):
    return SDSS.query_sql(query, timeout=500, data_release=18).to_pandas()