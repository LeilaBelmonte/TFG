import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import csv
from matplotlib import cm


print(" ")
print("######################################################")
print(" ")
print("A continuación se pedirà que introduzca por pantalla una serie de datos.")
print(" ")

#imagen=input("Escriba el nombre de la imagen (incluyendo la extensión .png): ")
archivo=input("Escriba el nombre del archivo de datos (incluyendo la extensión .csv): ")
tif=int(input("Introduzca la dimensión de la imagen tif (píxeles): "))
box=float(input("Introduzca la dimensión de las cajas (píxeles): "))
azimutal=float(input("Introduzca el ángulo azimutal: "))

file=open(archivo,'r')
type(file)
csvreader=csv.reader(file)

numero=[]
mean=[]
angle=[]

for row in csvreader:
	numero.append(row[0])
	mean.append(row[1])

numero.pop(0)
mean.pop(0)

maxim=65535.0
l=len(mean)				# nombre de caixes total
for i in range(0,l):
	phi=180*(1-float(mean[i])/maxim)
	alpha=azimutal+phi
	angle.append(alpha)

n=int(tif/box)         # nombre de caixes per fila

fig=plt.figure()
ax=Axes3D(fig)

#plano
X=np.linspace(-n,n,1000)
Y=np.linspace(-n,n,1000)
Z=np.linspace(0,2*n,1000)
Y,Z=np.meshgrid(Y,Z)

xp=-X*np.sin(np.radians(azimutal))
yp=Y*np.cos(np.radians(azimutal))
zp=Z

#flechas
xa=0.0
ya=0.0
za=float(n)

u1 = 12.0*np.cos(np.radians(azimutal))
v1 = 12.0*np.sin(np.radians(azimutal))
w1 = 0.0

u2 = 12.0
v2 = 0.0
w2 = 0.0

mapa = cm.get_cmap('jet')
jet2 = mapa(np.linspace(0,1,180))


for i in range(0,n):
	for j in range(0,n):
		alpha=angle[n*i+j]
		print(alpha)

		xs=-(2*j-n+1.0)*np.sin(np.radians(azimutal))
		ys=(2*j-n+1.0)*np.cos(np.radians(azimutal))
		zs=(2*n-1-2*i)

		us=2.0*np.cos(np.radians(alpha))
		vs=2.0*np.sin(np.radians(alpha))
		ws=0.0

		color=round(alpha-azimutal)

		q=ax.quiver(xs,ys,zs,us,vs,ws, color=jet2[color], cmap='jet')


ax.quiver(xa,ya,za,u1,v1,w1, color='red')
ax.quiver(xa,ya,za,u2,v2,w2, color='green')

ax.set_xlim(-20,20)
ax.set_ylim(-20,20)
ax.set_zlim(0,40)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.colorbar(q, shrink=0.5)
plt.show()


