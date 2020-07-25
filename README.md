# camminapy
A collection of (useful) Python scripts. 

## Overview

Create a colormap from `darkcolor` to `brightcolor`:
```python
mycmap(darkcolor=(0,0,0),brightcolor=(1,1,1),nbins=10)
```


Create a diverging colormap from `darkcolorleft` to `brightcolor`
to `darkcolorright`:
```python
mycmapdiv(darkcolorleft=(0,0,0),brightcolor=(1,1,1),darkcolorright=(0,0,0),nbins=10)
```


Visualize the colormap:
```python
plot_cmap(cmap)
```


Create overview plots for the line-source problem and receive a dictionary that contains the config file:
```python
configdict = lspp(folder) # folder contains config.txt
```


To create a dataframe that stores all the relevant configs:
```python
import numpy as np
import pandas as pd 
import os
import numpy as np 
from camminapy import lspp
prefix = "/path/to/the/correct/folder/goes/here"
sf = [x for x in os.listdir(prefix)]
df = pd.DataFrame()
for i, folder in enumerate(sf):
    foldername = prefix + "/" + folder
    config = lspp(foldername)
    df = df.append(config, ignore_index=True)

# Make sure to select only one class of problems (i.e., always the same nx,nq)
df = df[df["nx"]==200.0] 
```

Given a dataframe `df` with all the L2 errors, create a heatmap:
```python
createheatmap(df,nx,nq,safetyfactor=1.05,filename="tmp.pdf"):
```

