'''
Este script genera un grafico de mapa de fuerzas.
Esta pensado para graficar las fuerzas que se aplican sobre el chaleco.  
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




def main():

	sensor1=[100,200,300]
	sensor2=[90,80,100]
	sensor3=[120,330,70]
	sensor4=[89,90,77]
	sensor5=[112,200,300]
	sensor6=[90,80,100]
	sensor7=[50,330,70]
	sensor8=[87,90,77]
	sensor9=[4,200,300]
	sensor10=[0,80,100]
	sensor11=[0,330,70]
	sensor12=[12,90,77]


	time = 0 
	output_filename = 'chaleco1'
	
	grid_x = np.linspace(0,1,4)
	grid_y = np.linspace(0,1,3)	
	grilla_fuerzas = asigna_fuerzas(sensor1[time],sensor2[time],sensor3[time],sensor4[time],
		sensor5[time],sensor6[time],sensor7[time],sensor8[time],
		sensor9[time],sensor10[time],sensor11[time],sensor12[time])

	grafica_bordes_chaleco()
	grafica_chaleco(grid_x,grid_y,grilla_fuerzas,output_filename)

def asigna_fuerzas(s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12):
	'''
	Actualiza la grilla de fuerzas con los valores de las fuerzas
	reportados por cada sensor
	'''
	
	grilla_fuerzas= np.zeros((3,4))
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

	return grilla_fuerzas


def grafica_bordes_chaleco():
	'''
	Grafica los bordes y las mangas del chaleco
	'''

	# Lado derecho
	plt.axvline(x=1,ymin=0.0,ymax=0.67,linewidth=1.5, color='k')
	# Lado izquierdo
	plt.axvline(x=0,ymin=0.0,ymax=0.67,linewidth=1.5, color='k')

	# Manga izquierda
	x1, y1 = [-0.5, -0.01], [0.8, 1]
	x2, y2 = [-0.5, -0.01], [0.6, 0.8]
	plt.plot(x1, y1, x2, y2, linewidth=1.5,color='k')
	# Manga derecha
	x1, y1 = [1.01, 1.5], [1, 0.8]
	x2, y2 = [1.01, 1.5], [0.8, 0.6]
	plt.plot(x1, y1, x2, y2, linewidth=1.5,color='k')



def grafica_chaleco(grid_x,grid_y,grilla_fuerzas,output_filename):	
	'''
	Grafica la grilla que representa el mapa de fuerzas
	'''

	levels=np.linspace(10,np.max(grilla_fuerzas),70,endpoint=True)
	levbar=np.linspace(10,np.max(grilla_fuerzas),12,endpoint=True)
	plt.contourf(grid_x,grid_y,grilla_fuerzas, levels,cmap=plt.cm.jet,zorder=1)
	plt.colorbar(ticks=levbar)
	plt.grid(False)
	plt.xlabel('$x$-location~(m)',fontsize=10)
	plt.ylabel('$y$-location~(m)',fontsize=10)
	plt.title('Force map in the back ',fontsize=10)
	plt.xlim(-0.5,1.5)
	plt.ylim(0,1.2)
	pylab.savefig('{}.png'.format(output_filename), bbox_inches='tight')




if __name__=='__main__':
	main()