import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import RegularGridInterpolator,interp1d
import kitcolors as kit 
from scipy.interpolate import interp1d
from scipy.interpolate import RegularGridInterpolator
import os
def getcircles(data,n,radii):
    ny,nx = data.shape
    X = np.linspace(-1.5,1.5,nx+1)
    Y = np.linspace(-1.5,1.5,ny+1)
    Xcenters = (X[1:]+X[:-1])/2
    Ycenters = (Y[1:]+Y[:-1])/2

    my_interpolating_function = RegularGridInterpolator((Xcenters,Ycenters), data)
    
    sols = []
    for rad in radii:
    
        
        alpha = np.linspace(0,2*np.pi,n+1)[:-1]
        pointstoevaluate = np.zeros((n,2))
        pointstoevaluate[:,0] = np.cos(alpha)*rad
        pointstoevaluate[:,1] = np.sin(alpha)*rad
        sol = my_interpolating_function(pointstoevaluate)
        sols.append(sol)
    
    return sols

def getcuts(data,n):
    ny,nx = data.shape
    X = np.linspace(-1.5,1.5,nx+1)
    Y = np.linspace(-1.5,1.5,ny+1)
    Xcenters = (X[1:]+X[:-1])/2
    Ycenters = (Y[1:]+Y[:-1])/2

    my_interpolating_function = RegularGridInterpolator((Xcenters,Ycenters), data)
    
    pointstoevaluate = np.zeros((n,2))
    pointstoevaluate[:,0] = np.linspace(-1.4,1.4,n)
    pointstoevaluate[:,1] = np.linspace(-1.4,1.4,n)
    dia = my_interpolating_function(pointstoevaluate)

    pointstoevaluate = np.zeros((n,2))
    pointstoevaluate[:,0] = np.linspace(-1.4,1.4,n)
    verti = my_interpolating_function(pointstoevaluate)

    
    pointstoevaluate = np.zeros((n,2))
    pointstoevaluate[:,1] = np.linspace(-1.4,1.4,n)
    hori = my_interpolating_function(pointstoevaluate)

    
    return hori,verti,dia


def createrefsolution(nx,ny):
    ls = np.loadtxt("/home/qd4314/Software/camminapy/camminapy/exactLineSource.txt", delimiter=",")
    ls[0,0] = -2.5
    ls[-1,0] = 2.5
    x = np.linspace(-1.5,1.5,nx+1)
    x = (x[1:]+x[:-1])/2
    y = np.linspace(-1.5,1.5,ny+1)
    y = (y[1:]+y[:-1])/2
    xx,yy = np.meshgrid(x,y)
    r = (xx**2+yy**2)**0.5
    interpolant = interp1d(ls[:,0],ls[:,1])
    ref = interpolant(r)
    return ref 


def configfile2dict(configfilename):
    config = {}
    with open(configfilename, "r") as a_file:
        for line in a_file:
            stripped_line = line.strip()
            if len(stripped_line)>0:
                if not stripped_line[0] == "#":
                    try:
                        s = stripped_line.split("=")
                        config[s[0].strip()] = int(s[1].strip()) 
                    except:
                        pass
    return config
