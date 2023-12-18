import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

#from ipywidgets import interact
#import ipywidgets as widgets

np.random.seed(12345)

df = pd.DataFrame([np.random.normal(32000,200000,3650), 
                   np.random.normal(43000,100000,3650), 
                   np.random.normal(43500,140000,3650), 
                   np.random.normal(48000,70000,3650)], 
                  index=[1992,1993,1994,1995])

df = df.T
df

mean_value = list(df.mean())
std_dev = list(df.std())
conf_int = []
lower_ci = []
upper_ci = []
bars = []
y = 40000

fig, ax = plt.subplots()

for i in range(len(mean_value)):
    lower_ci.append(mean_value[i] - 1.96*(std_dev[i]/np.sqrt(len(df))))
    upper_ci.append(mean_value[i] + 1.96*(std_dev[i]/np.sqrt(len(df))))
    conf_int.append(upper_ci[i] - lower_ci[i])
conf_int

# If y = scalar value >> symmetric error (value - lower / upper - lower)
# If y = array >> assymetric error >> yerr = [lower_errors, upper_errors] 
#   upper_errors & lower_error are a list of values

colors = ['navy', 'blue','royalblue','cornflowerblue','lightcyan','white',
          'peachpuff','sandybrown','tomato','brown','maroon']
#cmap = plt.get_cmap('seismic')

cmap = ListedColormap(colors)
sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0, 1))
sm.set_array([])  # You can set an array here to explicitly specify the range

for i in range(len(df.columns)):
    if y > upper_ci[i]:
        norm_distance = 0
    elif y < lower_ci[i]:
        norm_distance = 1
    else:
        norm_distance = (upper_ci[i] - y) / (upper_ci[i] - lower_ci[i])

    bar = ax.bar(i, mean_value[i], yerr=(upper_ci[i] - mean_value[i]), align = 'center', capsize=5, edgecolor = 'grey', 
                 color = sm.to_rgba(norm_distance))
    bars.append(bar[0])

ax.set_xticks(range(len(df.columns)), df.columns) 
ax.set_xlabel('Year')
ax.set_ylabel('Mean')
ax.set_title('Harder Option')
ax.axhline(y, zorder=0, alpha = 0.8, linewidth=1, color = 'black')
ax.spines[['right', 'top']].set_visible(False)
txt = ax.text(-0.3, 48000, f'y = {int(y)}', bbox=dict(facecolor='white', edgecolor = 'black', boxstyle = 'square'))

sm = plt.cm.ScalarMappable(cmap=cmap) #, norm=plt.Normalize(0, 1)
sm.set_array([])  # You can set an array here to explicitly specify the range
cbar = plt.colorbar(sm, ax=ax, pad=0.1, orientation = 'horizontal', shrink = 0.9,aspect = 22)
cbar.set_label('Amount of Data Covered')
plt.tight_layout()


def on_click(event):
    global bars
    if event.inaxes == ax:
        ax.lines[-1].remove()
        y = event.ydata 
        ax.axhline(y, zorder=0, alpha = 0.8, linewidth=1, color = 'black')
        txt.set_text(f'y = {int(y)}')
        for i in range(len(df.columns)):
            if y >= upper_ci[i]:
                norm_distance = 0
            elif y <= lower_ci[i]:
                norm_distance = 1
            else:
                norm_distance = (upper_ci[i] - y) / (upper_ci[i] - lower_ci[i])
            bars[i].set_color(sm.to_rgba(norm_distance))
            bars[i].set_edgecolor('grey')

    plt.draw()

fig.canvas.mpl_connect('button_press_event', on_click)

plt.show()

