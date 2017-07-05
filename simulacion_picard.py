# -*- coding: utf-8 -*-
'''
Creado por Pablo Castro
15/05/17

PARA CAEBAT 3.0
Objetivo:
Automatizar todo el proceso de simulacion con aproximaciones de Picard desde el terminal de linux

Acciones:
-Elegir simulación
-Leer el número de tiempos a simular
-Ejecutar la simulacion de un caso que elijamos
-Copiar la carpeta con los resultados de la simulaciones en otra carpeta
 situada en el escritorio y ponerle un nombre segun el caso simulado y la fecha de simulacion.
-Despues de realizar esto, eliminamos las carpetas generadas por la simulacion
 en la carpeta ejemplo.
-Eliminamos el ultimo segmento y repetimos el proceso tantas veces como segmentos haya

FUNCIONA
'''

import os
import shutil
import numpy as np
from datetime import datetime
import time

def copiar_simulacion(Nombre_simulacion,Nombre_carpeta_general):
	#Calculamos la fecha en la que la carpeta fue creada
	fecha = os.stat(Nombre_simulacion).st_mtime
	
	#La convertimos a un formato legible y nombramos la nueva carpeta
	nombre_carpeta_copia = Nombre_simulacion + ' ' + str(datetime.fromtimestamp(fecha))
	shutil.copytree(Nombre_simulacion,nombre_carpeta_copia)
	shutil.move(nombre_carpeta_copia,'/home/batsim/Desktop/Mis simulaciones/'+Nombre_carpeta_general)


def eliminar_carpetas(Nombre_simulacion):
	shutil.rmtree('/home/batsim/caebat/vibe/examples/'+Nombre_simulacion+'/simulation_log')
	shutil.rmtree('/home/batsim/caebat/vibe/examples/'+Nombre_simulacion+'/simulation_setup')
	shutil.rmtree('/home/batsim/caebat/vibe/examples/'+Nombre_simulacion+'/work')
	shutil.rmtree('/home/batsim/caebat/vibe/examples/'+Nombre_simulacion+'/simulation_results')

def iteracion_picard(tiempos_picard,iteracion,modelo):
    datos_conf = open(modelo,'r')
    lineas_conf = datos_conf.readlines()
    datos_conf.close()
    
    datos_conf = open(modelo,'w')
    for line in lineas_conf:
        vector_conf = line.strip('\n').split('=')
        if vector_conf[0]=='   VALUES ':
            vector_tiempos = [str(tiempos_picard[0]),str(tiempos_picard[iteracion])]
            line = '   VALUES = '+' '.join(vector_tiempos)
            print(line)
        datos_conf.write(line)
    datos_conf.close()
    

"""
INICIO DEL PROGRAMA
"""
#Seleccionamos desde el terminal nuestra carpeta de simulación
print('Introduce el nombre de la carpeta que quieres simular:')
nombre = raw_input()

#Seleccionamos la duración de la simulación y el número de puntos
print('Introduce la duración y el número de puntos a simular.')
print('Duración: ')
duracion = float(raw_input())
print('Numero de puntos: ')
numero_puntos = float(raw_input())

tiempos_picard = np.linspace(0.0,duracion,numero_puntos)

#Iniciamos el contador de tiempo de ejecución
tiempo_inicial = time.time()

#Creamos la carpeta general que almacenará al resto de carpetas
fecha = time.strftime("%c")
nombre_carpeta_general = nombre + ' Picard ' + fecha
os.mkdir('/home/batsim/Desktop/Mis simulaciones/'+nombre_carpeta_general)

#Seleccionamos el archivo .conf que vamos a simular
if nombre == 'case1':
	nombre == 'thermal_chartran_cell_twoway.conf'
elif nombre == 'case2':
	modelo = 'thermal_electrical_chartran_cell_twoway.conf'
elif nombre == 'case3':
	modelo = 'thermal_electrical_chartran_battery_twoway.conf'
elif nombre == 'case6':
	modelo = 'thermal_electrical_chartran_farasis.conf'
elif nombre == 'case7':
	modelo = 'thermal_electrical_chartran_module_4P.conf'
elif nombre == 'case10':
	modelo = 'thermal_chartran_battery_hppc.conf'
elif nombre == 'caso_propio1':
	modelo = 'thermal_electrical_chartran_cell_twoway.conf'
else:
	print('Error al introducir el nombre de la carpeta')
	quit()


#Ejectuamos las simulaciones
iteracion = 0
for iteracion in range(1,len(tiempos_picard)):
    #Cambiamos el path a la carpeta seleccionada
    os.chdir('/home/batsim/caebat/vibe/examples/'+nombre)
    iteracion_picard(tiempos_picard,iteracion,modelo)
    os.system('/home/batsim/caebat/ipsframework-code/install/bin/ips.py --simulation='+modelo+' --log=temp.log --platform=../config/batsim.conf -a')
    os.chdir('/home/batsim/caebat/vibe/examples')
    copiar_simulacion(nombre,nombre_carpeta_general)
    eliminar_carpetas(nombre)
    print('FIN DE PUNTO DE TIEMPO')

#Calculamos el tiempo de ejecucion
tiempo_final = time.time()
tiempo_ejecucion = str(tiempo_final - tiempo_inicial)

#Mensaje indicando el final del proceso
print('FIN DE LA SIMULACION')
print('TIEMPO EMPLEADO: %s minutos' %tiempo_ejecucion)
