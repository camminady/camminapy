import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from colorspacious import cspace_converter
import numpy as np

def mycmap(darkcolor=(0,0,0),brightcolor=(1,1,1),nbins=10):
    colors = [darkcolor,brightcolor]
    cmap = LinearSegmentedColormap.from_list("", colors, N=nbins)    

    # Convert RGB to LAB
    x = np.linspace(0,1,nbins)
    rgb = cmap(x)[np.newaxis, :, :3]
    lab = cspace_converter("sRGB1", "CAM02-UCS")(rgb)
    
    lightness = lab[0,:,0] # So far, lightness is increasing but has no constant derivative.
#    lightness = lightness-np.min(lightness)
#    lightness /= np.max(lightness)
#    lightness *= 50
#    lightness += 50

    lightness_corrected = np.linspace(lightness[0],lightness[-1],len(lightness))
    lab[0,:,0] = lightness_corrected # Now it has.
    
    # Convert back to RGB.
    rgb = cspace_converter("CAM02-UCS","sRGB1")(lab)
    rgb = np.clip(rgb,0,1)
    rgb = np.squeeze(rgb,axis = 0) # Force all values to [0,1] (which might not be the case due to round-off errors)
    rgblist = list(map(tuple,rgb))
    
    
    # Create colormap based on corrected RGB values.
    cmap = LinearSegmentedColormap.from_list("", rgblist, N=nbins)
    return cmap

def mycmapdiv(darkcolorleft=(0,0,0),brightcolor=(1,1,1),darkcolorright=(0,0,0),nbins=10):
    colors = [darkcolorleft,brightcolor,darkcolorright]
    cmap = LinearSegmentedColormap.from_list("", colors, N=nbins)    

    # Convert RGB to LAB
    x = np.linspace(0,1,nbins)
    rgb = cmap(x)[np.newaxis, :, :3]
    lab = cspace_converter("sRGB1", "CAM02-UCS")(rgb)
    
    lightness = lab[0,:,0] # So far, lightness is increasing but has no constant derivative.

    start = (lightness[0]+lightness[-1])/2 # both shall have same lightness

    if len(lightness) % 2 == 0:
        lightness_corrected_left = np.linspace(start,np.max(lightness),len(lightness)//2)
        lightness_corrected_right = np.linspace(np.max(lightness),start,len(lightness)//2)
        lightness_corrected = np.hstack((lightness_corrected_left,lightness_corrected_right))
    else:
        lightness_corrected_left = np.linspace(start,np.max(lightness),len(lightness)//2+1)[:-1]
        lightness_corrected_right = np.linspace(np.max(lightness),start,len(lightness)//2+1)[1:]
        lightness_corrected = np.hstack((lightness_corrected_left,np.max(lightness),lightness_corrected_right))
    
    
    lab[0,:,0] = lightness_corrected # Now it has.
    
    # Convert back to RGB.
    rgb = cspace_converter("CAM02-UCS","sRGB1")(lab)
    rgb = np.clip(rgb,0,1)
    rgb = np.squeeze(rgb,axis = 0) # Force all values to [0,1] (which might not be the case due to round-off errors)
    rgblist = list(map(tuple,rgb))
    
    
    # Create colormap based on corrected RGB values.
    cmap = LinearSegmentedColormap.from_list("", rgblist, N=nbins)
    return cmap



def plot_cmap(cmap):
    fig, axs = plt.subplots(1,2,figsize=(6,2))
    gradient = np.linspace(0, 1, 256)
    gradient = np.vstack((gradient, gradient))
    axs[0].imshow(gradient,cmap = cmap,aspect="auto")
    axs[0].set_axis_off()
    
    
    x = np.linspace(0.0, 1.0, cmap.N+1)
    x = (x[1:]+x[:-1])/2
    rgb = cmap(x)[np.newaxis, :, :3]
    lab = cspace_converter("sRGB1", "CAM02-UCS")(rgb)
    L = lab[0,:,0]
    axs[1].plot(x,lab[0,:,0],color = "k",zorder = +1)
    axs[1].scatter(x,lab[0,:,0],c = cmap(x))
    dL = 1/(x[1]-x[0])*np.abs(np.diff(lab[0,:,0]))
    axs[1].plot(x[:-1],dL,c="k",ls="--")
    axs[1].set_ylabel(r"L (solid) & $\Delta$ L (dashed)");
