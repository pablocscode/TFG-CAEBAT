# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 18:44:45 2017
@author: Pablo

Objetivos:
-Lectura y representación de los archivos profiles.out y halfcells.out
-La lectura debe ser capaz de leer los archivos sin importar su longitud

Guía:
-Ambos archivos deben encontrarse en la misma carpeta que este script
"""

import numpy as np
import matplotlib.pyplot as plt

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
distancia = np.zeros((num_tiempos,num_distancias))  #Cada columna tiene 101 filas
C_Elec = np.zeros((num_tiempos,num_distancias))
C_Sol_Surf = np.zeros((num_tiempos,num_distancias))
Liq_Pot = np.zeros((num_tiempos,num_distancias))
Solid_Pot = np.zeros((num_tiempos,num_distancias))
J_main = np.zeros((num_tiempos,num_distancias))

tiempo = np.zeros(num_tiempos)

V_neg = np.zeros(num_tiempos)
V_pos = np.zeros(num_tiempos)
Heat_gen = np.zeros(num_tiempos)


#Datos profiles.in
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
 
#Datos halfcells.out
for i in range(1,num_tiempos+1):
    linea = lineas_halfcells[i].split()

    V_neg[i-1] = linea[1]
    V_pos[i-1] = linea[2]
    Heat_gen[i-1] = linea[5] 
    
#Representamos los resultados
def plot(numero):
    plt.figure(1)
    plt.plot(distancia[numero],C_Elec[numero],'o')
    plt.plot(distancia[0],C_Elec[0],'o')
    plt.ylabel('Concentración Electrolito')
    plt.title(tiempo[numero])
    plt.xlabel('Distancia')

    plt.figure(2)
    plt.plot(distancia[numero],C_Sol_Surf[numero],'o')
    plt.plot(distancia[0],C_Sol_Surf[0],'o')
    plt.ylabel('Concentración Sólido')
    plt.xlabel('Distancia')
    plt.title(tiempo[numero])

    plt.figure(3)
    plt.plot(distancia[numero],Liq_Pot[numero],'o')
    plt.plot(distancia[0],Liq_Pot[0],'o')
    plt.ylabel('Potencial en el líquido')
    plt.xlabel('Distancia')
    plt.title(tiempo[numero])

    plt.figure(4)
    plt.plot(distancia[numero],Solid_Pot[numero],'o')
    plt.plot(distancia[0],Solid_Pot[0],'o')
    plt.ylabel('Potencial en el sólido')
    plt.xlabel('Distancia')
    plt.title(('Tiempo =', tiempo[numero],' min'))
    
    plt.figure(5)
    plt.plot(tiempo,V_pos-V_neg)
    plt.ylabel('Voltaje celda (V)')
    plt.xlabel('Tiempo (s)')
    
"""
    plt.figure(6)
    plt.plot(distancia[numero],J_main[numero],'o')
    plt.ylabel('J main')
    plt.xlabel('Distancia')
"""
#Representamos los resultados para el último tiempo
plot(num_tiempos-1)
