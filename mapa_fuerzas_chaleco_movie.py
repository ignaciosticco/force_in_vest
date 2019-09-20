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

################### PARAMETERS ###################
xi = 0.0
xf = 1.0
rows = 3
yi = 0.0
yf = 1.0
cols = 4
output_filename = 'chaleco1'
##################################################



def animate(i):
	'''
	Animation function
	'''
	global cont
	z = lista_grilla_fuerzas[i]
	cont = plt.contourf(grid_x, grid_y, z, levels, cmap=plt.cm.jet,zorder=1)
	plt.title('Force map in the back ',fontsize=10)
	return cont


def grafica_bordes_chaleco():
  '''
  Grafica los bordes y las mangas del chaleco
  '''

  # Manga izquierda
  x1, y1 = [-0.5, -0.01], [0.8, 1]
  x2, y2 = [-0.5, -0.01], [0.6, 0.8]
  plt.plot(x1, y1, x2, y2, linewidth=1.5,color='k')
  # Manga derecha
  x1, y1 = [1.01, 1.5], [1, 0.8]
  x2, y2 = [1.01, 1.5], [0.8, 0.6]
  plt.plot(x1, y1, x2, y2, linewidth=1.5,color='k')
  # Borde derecho
  plt.axvline(x=1,ymin=0.0,ymax=0.67,linewidth=1.5, color='k')
  # Borde izquierdo
  plt.axvline(x=0,ymin=0.0,ymax=0.67,linewidth=1.5, color='k')



def asigna_fuerzas(s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12):
  '''
  Actualiza la grilla de fuerzas con los valores de las fuerzas
  reportados por cada sensor
  '''
  
  grilla_fuerzas= np.zeros((rows,cols)) # Inicializa con ceros 
  grilla_fuerzas[2,0]=s1
  grilla_fuerzas[2,1]=s2
  grilla_fuerzas[2,2]=s3
  grilla_fuerzas[2,3]=s4
  grilla_fuerzas[1,0]=s5
  grilla_fuerzas[1,1]=s6
  grilla_fuerzas[1,2]=s7
  grilla_fuerzas[1,3]=s8
  grilla_fuerzas[0,0]=s9
  grilla_fuerzas[0,1]=s10
  grilla_fuerzas[0,2]=s11
  grilla_fuerzas[0,3]=s12

  # Faltan los sensores de los hombros.

  return grilla_fuerzas


################ MAIN ######################3


sensor1=[100,120,130]
sensor2=[110,130,110]
sensor3=[170,140,130]
sensor4=[180,110,150]
sensor5=[140,120,150]
sensor6=[120,130,190]
sensor7=[110,180,160]
sensor8=[130,150,130]
sensor9=[150,120,103]
sensor10=[107,103,120]
sensor11=[150,180,130]
sensor12=[130,160,150]
sensor13=[100,140,190]
sensor14=[190,170,110]


lista_grilla_fuerzas = []
for time in range(0,len(sensor1)):
  
  grilla_fuerzas = asigna_fuerzas(sensor1[time],sensor2[time],sensor3[time],sensor4[time],
  sensor5[time],sensor6[time],sensor7[time],sensor8[time],
  sensor9[time],sensor10[time],sensor11[time],sensor12[time])

  lista_grilla_fuerzas+=[grilla_fuerzas]

total_frames = len(lista_grilla_fuerzas)
grid_x = np.linspace(xi,xf,cols)
grid_y = np.linspace(yi,yf,rows) 
grid_density0=lista_grilla_fuerzas[0]

fig = plt.figure()
ax = plt.axes(xlim=(-1, 1), ylim=(0, 1.2))
grafica_bordes_chaleco()

levels=np.linspace(90,np.max(grilla_fuerzas),70,endpoint=True)
levbar=np.linspace(20,np.max(grilla_fuerzas),12,endpoint=True)
cont=plt.contourf(grid_x,grid_y,grid_density0, levels,cmap=plt.cm.jet)
plt.colorbar(ticks=levbar)
plt.grid(False)
plt.xlabel('$x$-location~(m)',fontsize=10)
plt.ylabel('$y$-location~(m)',fontsize=10)
plt.xlim(-0.5,1.5)
plt.ylim(0,1.2)
plt.subplots_adjust(bottom=0.29,right=0.98,left=0.15)

anim = animation.FuncAnimation(fig, animate, frames=total_frames, repeat=False)
anim.save('{}.mp4'.format(output_filename), writer=animation.FFMpegWriter())
