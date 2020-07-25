import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import RegularGridInterpolator, interp1d

from .getvalues import configfile2dict, createrefsolution
from .plotcollection import plotall



def lspp(folder):
    if True:
        data = np.loadtxt(folder + "/data/rhofinal.txt", delimiter=",")[2:-2, 2:-2]
        ref = createrefsolution(*data.shape)
        weights = np.loadtxt(folder + "/data/quadweights.txt", delimiter=",")

        config = configfile2dict(folder + "/config.txt")

        title = (
            r"r${}_"
            + "{"
            + str(config["rotationmagnitude"])
            + "}"
            + "$S${}_"
            + "{"
            + str(config["quadratureorder"])
            + "}"
            + "$, $n_q={}$".format(len(weights))
        )
        saveprefix = folder+"/{}r{}S{}nx{}".format(
            config["nx"], config["rotationmagnitude"], config["quadratureorder"],config["nx"]
        )
        print(saveprefix)
        plotall(data, saveprefix, title, config["testcaseid"])
        plt.close("all")
    #except:
    #    print("No data found in {}. Continue.".format(folder))
    #    pass

