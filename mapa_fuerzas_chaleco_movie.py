'''
Este programa produce una animacion que representa la evolucion 
temporal del mapa de fuerzas. 
'''

################### LIBRARIES & PLOT SETTINGS ###################
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import pylab
import math
import pandas as pd

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
input_filename = 'datos_subteB_16-9.txt'
output_filename = 'chaleco1'
timestep_min = 5040
timestep_max = 5090
xi = 0.0
xf = 1.0
rows = 3
yi = 0.0
yf = 1.0
cols = 4

################ FUNCTIONS ######################
def animate(i):
	'''
	Animation function
	'''

	global cont
	z = lista_grilla_fuerzas[i]
	cont = plt.contourf(grid_x, grid_y, z, levels, cmap=plt.cm.jet,zorder=1)
	plt.title("Force map in the back \t\t-\t\t timestep = %i" %i,fontsize=10)
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



def asigna_fuerzas(s0,s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11):
  '''
  Actualiza la grilla de fuerzas con los valores de las fuerzas
  reportados por cada sensor
  '''
  
  grilla_fuerzas = np.zeros((rows,cols)) # Inicializa con ceros 
  grilla_fuerzas[2,0] = s0
  grilla_fuerzas[2,1] = s1
  grilla_fuerzas[2,2] = s6
  grilla_fuerzas[2,3] = s7
  grilla_fuerzas[1,0] = s2
  grilla_fuerzas[1,1] = s3
  grilla_fuerzas[1,2] = s8
  grilla_fuerzas[1,3] = s9
  grilla_fuerzas[0,0] = s4
  grilla_fuerzas[0,1] = s5
  grilla_fuerzas[0,2] = s10
  grilla_fuerzas[0,3] = s11

  # To do:Faltan los sensores de los hombros.

  return grilla_fuerzas

def importa_dataset(input_filename):
	df = pd.read_csv("{}".format(input_filename),delimiter=' ',engine="python") 
	return df

def crea_lista_grilla_fuerzas(timestep_min,timestep_max):
	'''
	Crea una lista de grillas, cada elemento de la lista corresponde
	a una grilla de fuerzas en un determinado timestep. 
	'''

	lista_grilla_fuerzas = []
	for time in range(timestep_min,timestep_max+1):
	  
	  grilla_fuerzas = asigna_fuerzas(serie_s0[time],serie_s1[time],serie_s2[time],serie_s3[time],
	  serie_s4[time],serie_s5[time],serie_s6[time],serie_s7[time],
	  serie_s8[time],serie_s9[time],serie_s10[time],serie_s11[time])

	  lista_grilla_fuerzas += [grilla_fuerzas]
	return lista_grilla_fuerzas

################ MAIN ######################


##### LOAD DATA #####
df = importa_dataset(input_filename)
serie_s0 = df.iloc[:,1].tolist()
serie_s1 = df.iloc[:,2].tolist()
serie_s2 = df.iloc[:,3].tolist()
serie_s3 = df.iloc[:,4].tolist()
serie_s4 = df.iloc[:,5].tolist()
serie_s5 = df.iloc[:,6].tolist()
serie_s6 = df.iloc[:,7].tolist()
serie_s7 = df.iloc[:,8].tolist()
serie_s8 = df.iloc[:,9].tolist()
serie_s9 = df.iloc[:,10].tolist()
serie_s10 = df.iloc[:,11].tolist()
serie_s11 = df.iloc[:,12].tolist()

##### SETTINGS #####
lista_grilla_fuerzas = crea_lista_grilla_fuerzas(timestep_min,timestep_max)

##### SETTINGS #####
total_frames = len(lista_grilla_fuerzas)
grid_x = np.linspace(xi,xf,cols)
grid_y = np.linspace(yi,yf,rows) 
grid_density0 = lista_grilla_fuerzas[0]

##### PLOT #####
fig = plt.figure()
ax = plt.axes(xlim=(-1, 1), ylim=(0, 1.2))
grafica_bordes_chaleco()
levels = np.linspace(10,np.max(lista_grilla_fuerzas),70,endpoint=True)
levbar = np.linspace(10,np.max(lista_grilla_fuerzas),8,endpoint=True)
cont = plt.contourf(grid_x,grid_y,grid_density0, levels,cmap=plt.cm.jet)
plt.colorbar(ticks=levbar)
plt.grid(False)
plt.xlabel('$x$-location~(m)',fontsize=10)
plt.ylabel('$y$-location~(m)',fontsize=10)
plt.xlim(-0.5,1.5)
plt.ylim(0,1.2)
plt.subplots_adjust(bottom=0.29,right=0.98,left=0.15)

##### ANIMATION #####
anim = animation.FuncAnimation(fig, animate, frames=total_frames, repeat=False)
anim.save('{}.mp4'.format(output_filename), writer=animation.FFMpegWriter())