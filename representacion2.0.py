# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 10:14:31 2017
@author: Pablo

Objetivos:
-Representar de forma dinámica los resultados del archivo profiles.out para cualquier tiempo

Guía:
-Este script debe encontrarse en la misma carpeta que los archivos profiles.out y halfcells.out
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

#Leemos todas las líneas del archivo
archivo = open('profiles.out','r')
lineas = archivo.readlines()
archivo.close()

#Calculamos el número de filas del archivo para cada tiempo
i = 4 #Empieza a haber datos a partir de la línea 4
num_distancias = 0
#Se aumenta el contador con cada línea distinta de cero de la primera matriz de
#tiempos
while lineas[i] != '  \n':
    num_distancias += 1
    i += 1

#Calculamos el número de tiempos del archivo
datos_halfcells = open('halfcells.out','r')
lineas_halfcells = datos_halfcells.readlines()
datos_halfcells.close()
num_tiempos = len(lineas_halfcells)-1 #la primera linea no tiene datos

#Declaramos los vectores que contendrán los valores de las columnas
distancia = np.zeros((num_tiempos,num_distancias))
C_Elec = np.zeros((num_tiempos,num_distancias))
C_Sol_Surf = np.zeros((num_tiempos,num_distancias))
Liq_Pot = np.zeros((num_tiempos,num_distancias))
Solid_Pot = np.zeros((num_tiempos,num_distancias))
J_main = np.zeros((num_tiempos,num_distancias))

tiempo = np.zeros(num_tiempos)


#Inicializamos para empezar el ciclo for
fila =0
columna = 0
#Cada línea (fila) representa los datos para un tiempo concreto
for j in range(4,(num_distancias+6)*num_tiempos,num_distancias+6):
    for i in range(j,j+num_distancias):  #Empieza a haber datos a partir de la línea 4
        #Cada elemento de "lineas" es un línea entera que convertimos en un vector
        linea = lineas[i].split(',')
        #A cada variable le vamos asignando su valor de cada línea que leemos
        distancia[fila,columna] = float(linea[0])
        C_Elec[fila,columna] = float(linea[1])
        C_Sol_Surf[fila,columna] = float(linea[2])
        Liq_Pot[fila,columna] = float(linea[3])
        Solid_Pot[fila,columna] = float(linea[4])
        J_main[fila,columna] = float(linea[5])
        columna = columna +1
     
    #Asignamos el tiempo de cada gráfica
    linea = lineas[j-1].split()
    tiempo[fila] = float(linea[2])
    
    #Al final del ciclo for pasamos a la siguiente fila y ponemos a cero las columnas
    fila = fila+1
    columna = 0
    
    
    
#Representamos los resultados
#Figura 1
fig1 = plt.figure(1)
ax1 = fig1.add_subplot(1,1,1)
#plt.axis([0, 1, -10, 10])
plt.subplots_adjust(left=0.25, bottom=0.25)
axi1  = plt.axes([0.2, 0.15, 0.65, 0.03])
si1 = Slider(axi1, 'Tiempo', 0, 100, valinit=0)

#Figura 2
fig2 = plt.figure(2)
ax2 = fig2.add_subplot(1,1,1)
#plt.axis([0, 1, -10, 10])
plt.subplots_adjust(left=0.25, bottom=0.25)
ax2.set_ylim([0, 0.9])
ax2.set_xlim([0, 100])
axi2  = plt.axes([0.2, 0.15, 0.65, 0.03])
si2 = Slider(axi2, 'Tiempo',0,num_tiempos-1,valinit = 0)



def plot1(val):
    i = int(si1.val)
    ax1.clear()
    ax1.plot(C_Elec[i])

def plot2(val):
    i = int(si2.val)
    ax2.clear()
    ax2.set_ylim([0, 0.9])
    ax2.set_xlim([0, num_distancias])
    ax2.plot(C_Sol_Surf[i])
    
si1.on_changed(plot1)
si2.on_changed(plot2)

