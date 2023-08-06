import numpy as np
import matplotlib.colors as clr
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

from utils import *

# BPT classification

class SDSSGalaxy(object):
    def __init__(
        self,
        top: int = 10
    ):

        with open('query_task1.txt', 'r') as file:
            query = file.read().replace('\n', ' ') ## input is a single string
            if top != 50000:
                query = query.replace('50000', str(top))
        
        self.df = query_table(query)
        

    def bpt_classify(self):
        self.df['x_BPT'] = np.log10(self.df['nii_6584_flux']/self.df['h_alpha_flux'])
        self.df['y_BPT'] = np.log10(self.df['oiii_5007_flux']/self.df['h_beta_flux'])
        self.df['class_Kauffmann'] = np.where((self.df['y_BPT'] <= kauffman(self.df['x_BPT'])), "SFG", "QSO")
        self.df['class_Kewley'] = np.where((self.df['y_BPT'] <= kewley(self.df['x_BPT'])), "SFG", "QSO")
        self.df['class_BPT'] = np.where(((self.df['class_Kauffmann']=='SFG')&(self.df['class_Kewley']=='SFG')), "SFG", 
                                        np.where(((self.df['class_Kauffmann']=='QSO')&(self.df['class_Kewley']=='QSO')), "AGN", 
                                                "composite"))
        return self.df

    def bpt_plot(self):

        fig = plt.figure()

        x = self.df['x_BPT']
        y = self.df['y_BPT']
        xy = np.vstack([x,y])
        self.df["kde"] = gaussian_kde(xy)(xy)

        class_dict = {'SFG': plt.cm.Blues, 
                    'composite': plt.cm.Greens, 
                    'AGN': plt.cm.Oranges
                    }
        
        for class_gal in class_dict.keys():
            self.df_sub = self.df[self.df['class_BPT'] == class_gal]
            x_sub = self.df_sub['x_BPT']
            y_sub = self.df_sub['y_BPT']
            z_sub = self.df_sub['kde']
            normalize = clr.Normalize(vmin=-1, vmax=1)
            plt.scatter(x_sub, y_sub, c=z_sub, s=5, edgecolor=None,
                        cmap=class_dict[class_gal], norm=normalize)
        
        x = np.linspace(np.min(self.df['x_BPT']),np.max( self.df['x_BPT']), 1000)
        plt.plot(x, kauffman(x), 'k--', label="Kauffmann")
        plt.plot(x, kewley(x), 'k:', label="Kewley")

        scatter1 = plt.scatter([], [], c='cornflowerblue', label="SFG")
        scatter2 = plt.scatter([], [], c='green', label="composite")
        scatter3 = plt.scatter([], [], c='darkorange', label="AGN")
        plt.title('BPT diagram')
        plt.legend((scatter3, scatter2, scatter1), ["QSO", "composite", "SFG"], 
                loc='lower left', title="BPT classification", fontsize='medium')
        plt.xlabel(r"log [NII]$\lambda$6584/H$\alpha$", fontsize=12)
        plt.ylabel(r"log [OIII]$\lambda$5007/H$\beta$", fontsize=12)
        plt.subplots_adjust(hspace=.0)
        
        return fig