import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.widgets import RangeSlider


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
yinitial = [20000,40000]
yu = max(yinitial)
yl = min(yinitial)

fig, ax = plt.subplots()

for i in range(len(mean_value)):
    lower_ci.append(mean_value[i] - 1.96*(std_dev[i]/np.sqrt(len(df))))
    upper_ci.append(mean_value[i] + 1.96*(std_dev[i]/np.sqrt(len(df))))
    conf_int.append(upper_ci[i] - lower_ci[i])
conf_int

# If y = scalar value >> symmetric error (value - lower / upper - lower)
# If y = array >> assymetric error >> yerr = [lower_errors, upper_errors] 
#   upper_errors & lower_error are a list of values

colors = ['white', 'mistyrose','peachpuff','lightsalmon','coral','tomato',
          'orangered','firebrick','maroon']

cmap = ListedColormap(colors)
sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0, 1))
sm.set_array([])  # You can set an array here to explicitly specify the range

for i in range(len(df.columns)):
    if yu < lower_ci[i] or yl > upper_ci[i]:
        norm_distance = 0
    elif yu > upper_ci[i] and yl < lower_ci[i]:
        norm_distance = 1
    elif yu < upper_ci[i] and yl < lower_ci[i]:
        norm_distance = (yu - lower_ci[i]) / (upper_ci[i] - lower_ci[i])
    elif yu > upper_ci[i] and yl > lower_ci[i]:
        norm_distance = (upper_ci[i] - yl) / (upper_ci[i] - lower_ci[i])
    else:
        norm_distance = (yu - yl)/(upper_ci[i] - lower_ci[i])
    bar = ax.bar(i, mean_value[i], yerr=(upper_ci[i] - mean_value[i]), align = 'center', capsize=5, edgecolor = 'grey', 
                 color = sm.to_rgba(norm_distance))
    bars.append(bar[0])


ax.set_xticks(range(len(df.columns)), df.columns) 
ax.set_xlabel('Year')
ax.set_ylabel('Mean')
ax.set_title('Hardest Option')
ax.set_xlim(-1,4)
ax.axhline(yu, zorder=0, alpha = 0.8, linewidth=1, linestyle='dashed', color = 'grey')
ax.axhline(yl, zorder=0, alpha = 0.8, linewidth=1, linestyle='dashed', color = 'grey')
fill = ax.fill_between(range(-1, len(df.columns)+1), yu, yl, alpha = 0.25, color = 'grey')
ax.spines[['right', 'top']].set_visible(False)

#txt = ax.text(-0.3, 48000, f'y = {int(y)}', bbox=dict(facecolor='white', edgecolor = 'black', boxstyle = 'square'))

# Add a slider for adjusting the y-value range
axcolor = 'lightgoldenrodyellow'
axrange = plt.axes([0.1, 0.01, 0.65, 0.03], facecolor=axcolor)
y_range_slider = RangeSlider(axrange, 'Y-Range', 0,50000)


sm = plt.cm.ScalarMappable(cmap=cmap) #, norm=plt.Normalize(0, 1)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, pad=0.1, orientation = 'horizontal', shrink = 0.9,aspect = 22)
cbar.set_label('Amount of Data Covered')
plt.tight_layout()

def update(val):
    global bars

    # Get the current y-value range from the slider
    y_min, y_max = y_range_slider.val
    
    # Update the fill_between
    dummy = ax.fill_between(range(-1, len(df.columns)+1), y_max, y_min, alpha = 0, color = 'grey')
    dp = dummy.get_paths()[0]
    dummy.remove()
    fill.set_paths([dp.vertices])

    # Update the position of the horizontal lines
    ax.lines[-1].set_ydata(y_min)
    ax.lines[-2].set_ydata(y_max)

    # Update bar colors based on the y-value range
    for i in range(len(df.columns)):
            if y_max < lower_ci[i] or y_min > upper_ci[i]:
                norm_distance = 0
            elif y_max > upper_ci[i] and y_min < lower_ci[i]:
                norm_distance = 1
            elif y_max < upper_ci[i] and y_min < lower_ci[i]:
                norm_distance = (y_max - lower_ci[i]) / (upper_ci[i] - lower_ci[i])
            elif y_max > upper_ci[i] and y_min > lower_ci[i]:
                norm_distance = (upper_ci[i] - y_min) / (upper_ci[i] - lower_ci[i])
            else:
                norm_distance = (y_max - y_min)/(upper_ci[i] - lower_ci[i])
            bars[i].set_color(sm.to_rgba(norm_distance))
            bars[i].set_edgecolor('grey')

    
    # Redraw the figure
    fig.canvas.draw_idle()

# Attach the update function to the slider
y_range_slider.on_changed(update)

plt.show()

