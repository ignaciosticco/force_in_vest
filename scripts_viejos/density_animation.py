'''
This script produces an animation of the temporal evolution of the density.
The input file is the configuration file (positions for every timestep). 

'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import pylab
import math

golden_mean = (math.sqrt(5)-1.0)/2.0        # Aesthetic ratio
fig_width = 3+3/8 			    			# width  in inches
fig_height = fig_width*golden_mean          # height in inches
fig_size =  [fig_width,fig_height]

params = {'backend': 'ps',
          'axes.titlesize': 8,
          'axes.labelsize': 9,
          'axes.linewidth': 0.5, 
          'axes.grid': True,
          'axes.labelweight': 'normal',  
          'font.family': 'serif',
          'font.size': 8.0,
          'font.weight': 'normal',
          'text.color': 'black',
          'xtick.labelsize': 8,
          'ytick.labelsize': 8,
          'text.usetex': True,
          'legend.fontsize': 8,
          'figure.dpi': 300,
          'figure.figsize': fig_size,
          'savefig.dpi': 600,
         }

pylab.rcParams.update(params)



######################### PARAMETER #########################
begin_corridor = 0.0
end_corridor =  27.0
wall_up = 24.0  
wall_down = 0.0
lenght_x = end_corridor-begin_corridor
lenght_y = wall_up-wall_down
#############################################################   


def main_loop(data):
    lista_grid_density = []
    lista_number_pedestrians=[]
    f=open(data, 'r')
    lines=f.readlines()
    line_number = 0
    while line_number<len(lines):
        line = lines[line_number].rstrip('\n')
        if(line=='ITEM: NUMBER OF ATOMS'):
            number_pedestrians=int(lines[line_number+1])
            x=[]
            y=[]
            first_line_table=line_number+7
            for j in range(first_line_table, first_line_table+number_pedestrians):
                row=lines[j].split(' ')
                x+=[float(row[1])]
                y+=[float(row[2])]
            
            grid_density=process_density(x,y)
            lista_grid_density+=[grid_density]
            lista_number_pedestrians+=[number_pedestrians]
            line_number+=number_pedestrians-1
        line_number+=1
    f.close()
    return lista_grid_density,lista_number_pedestrians




def process_density(x,y):
    grid_x = np.linspace(begin_corridor,end_corridor,end_corridor-begin_corridor)
    grid_y = np.linspace(wall_down,wall_up,wall_up-wall_down)
    grid_N = np.zeros((len(grid_y),len(grid_x)))

    for i in range(0,len(x)):
        if (x[i]<end_corridor):
            col=int((x[i]-begin_corridor)/(lenght_x)*(len(grid_x)))
            fil = int((y[i]-wall_down)/(lenght_y)*(len(grid_y)))
            grid_N[fil][col] += 1
    return grid_N


# animation function
def animate(i):
    global cont
    z = lista_grid_density[i]
    cont = plt.contourf(grid_x, grid_y, z, levels, cmap=plt.cm.jet,zorder=1)
    plt.title("Density map (p~m$^{-2}$) \t\t-\t\t N = %i" %lista_number_pedestrians[i]) 
    print(lista_number_pedestrians[i])
    return cont



data_config = input("Enter configurations file name:\n")
lista_grid_density,lista_number_pedestrians = main_loop(data_config)

grid_x = np.linspace(begin_corridor,end_corridor,end_corridor-begin_corridor)
grid_y = np.linspace(wall_down,wall_up,wall_up-wall_down)
grid_density0=lista_grid_density[0]

fig = plt.figure()
ax = plt.axes(xlim=(0, 28), ylim=(0, 24))

rect = patches.Rectangle((27,10.5),1,3,linewidth=1,edgecolor='g',facecolor='g')
ax.add_patch(rect)


levels=np.linspace(0,10,70,endpoint=True)
levbar=np.linspace(0,10,11,endpoint=True)
cont=plt.contourf(grid_x,grid_y,grid_density0, levels,cmap=plt.cm.jet)
plt.colorbar(ticks=levbar)
plt.xlabel('$x$-location~(m)',fontsize=8)
plt.ylabel('$y$-location~(m)',fontsize=8)
plt.yticks(np.linspace(0,wall_up,4), fontsize=8)
plt.xticks(fontsize=8)
plt.grid(False)
plt.subplots_adjust(bottom=0.19,right=1.02,left=0.15)

total_frames = len(lista_grid_density)

anim = animation.FuncAnimation(fig, animate, frames=total_frames, repeat=False)
anim.save('animation_density.mp4', writer=animation.FFMpegWriter())