import numpy as np
from tkinter import *
from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib.image as img
import csv

print(" ")
print("######################################################")
print(" ")
print("A continuación se pedirà que introduzca por pantalla una serie de datos.")
print(" ")


archivo=input("\n Escriba el nombre del archivo de datos (incluyendo la extensión .csv): ")
imagen=input("\n Escriba el nombre de la imagen (incluyendo la extensión .png): ")
particula=input("\n Cual és el nombre de la partícula? ")
# d=int(input("\n Dimensión de la imagen base: "))
tif=int(input("\n Dimensión de la imagen tif (píxeles): "))
# box=float(input("\n Dimensión de las cajas (píxeles): "))
azimutal=float(input("\n Angulo azimutal: "))

file=open(archivo,'r')
type(file)
csvreader=csv.reader(file)

numero=[]
mean=[]
angle=[]
proyeccion=[]

for row in csvreader:
	numero.append(row[0])
	mean.append(row[1])

numero.pop(0)
mean.pop(0)

maxim=65535.0
imanacion=0
m=len(mean)				# nombre de caixes total
for i in range(0,m):
	phi=180*(1-float(mean[i])/maxim)
	imanacion=imanacion+np.cos(np.radians(phi))
	alpha=azimutal-phi
	angle.append(alpha)

d=840
box=2

n=int(tif/box)         # nombre de caixes per fila
lbox=d/n               # amplada de la caixa (quadrada)
cbox=lbox/2            # centre de la caixa
total=imanacion/m

fig=plt.figure()
ax=fig.add_subplot(111)

background=img.imread(imagen)
ax.imshow(background)
norm=cm.colors.Normalize(vmin=0,vmax=180)


for i in range(0,n):
	for j in range(0,n):
		alpha=angle[n*i+j]
		print(alpha)
		phi=alpha+azimutal

		if phi <= 90.0:
			proyec=np.abs( (float(mean[i])/maxim)*np.cos(np.radians(alpha)) )
		else:
			proyec=np.abs( (1-float(mean[i])/maxim)*np.cos(np.radians(alpha)) )

		xs=cbox+j*lbox
		ys=cbox+i*lbox

		us=10.0*proyec*np.cos(np.radians(alpha))
		vs=10.0*proyec*np.sin(np.radians(alpha))

		q=ax.quiver(xs,ys,us,vs,alpha,
					width=0.003,
					scale=100,
					cmap='jet',norm=norm)

text="Imanación = " + str(total) + "\n Tamaño = "

ax.set_title(str(particula) + "\t $\\theta$=" + str(azimutal))
fig.text(0.4,0.05,text, fontsize=12)
plt.colorbar(q, cmap=plt.cm.jet)
plt.axis('off')
plt.show()


