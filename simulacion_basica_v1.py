# -*- coding: utf-8 -*-
'''
Creado por Pablo Castro
28/03/17
Objetivo:
Automatizar todo el proceso de simulacion desde el terminal de linux.
Funciona para CAEBAT 1.0

Como usarlo:
1- Se situa el script en la carpeta 'examples'.
2- Se crea una carpeta llamada 'Mis simulaciones' en el escritorio.
3- Se ejecuta normalmente desde la terminal: 'python simulacion_basica.py'
4- El programa te pide el nombre exacto de la carpeta a simular.

Acciones:
-Ejecutar la simulacion de un caso que elijamos
-Copiar la carpeta con los resultados de la simulaciones en otra carpeta
 situada en el escritorio y ponerle un nombre segun el caso simulado y la fecha de simulacion.
-Despues de realizar esto, eliminamos las carpetas generadas por la simulacion
 en la carpeta ejemplo.
'''

import os
import shutil
from datetime import datetime

def copiar_simulacion(Nombre_simulacion):
	#Calculamos la fecha en la que la carpeta fue creada
	fecha = os.stat(Nombre_simulacion).st_mtime
	
	#La convertimos a un formato legible y nombramos la nueva carpeta
	nombre_carpeta_copia = Nombre_simulacion + ' ' + str(datetime.fromtimestamp(fecha))
	shutil.copytree(Nombre_simulacion,nombre_carpeta_copia)
	shutil.move(nombre_carpeta_copia,'/home/batsim/Desktop/Mis simulaciones/')


def eliminar_carpetas(Nombre_simulacion):
	shutil.rmtree('/home/batsim/caebat/vibe/examples/'+Nombre_simulacion+'/simulation_log')
	shutil.rmtree('/home/batsim/caebat/vibe/examples/'+Nombre_simulacion+'/simulation_results')
	shutil.rmtree('/home/batsim/caebat/vibe/examples/'+Nombre_simulacion+'/simulation_setup')
	shutil.rmtree('/home/batsim/caebat/vibe/examples/'+Nombre_simulacion+'/work')

#Seleccionamos desde el terminal nuestra carpeta de simulacion
print('Introduce el nombre de la carpeta que quieres simular:')
nombre = raw_input()

#Seleccionamos el archivo .conf que vamos a simular
if nombre == 'case2':
	modelo = 'thermal_electrical_chartran_cell_twoway.conf'
elif nombre == 'case3':
	modelo = 'thermal_electrical_chartran_battery_twoway.conf'
elif nombre == 'case6':
	modelo = 'thermal_electrical_chartran_farasis.conf'
elif nombre == 'case7':
	modelo = 'thermal_electrical_chartran_module_4P.conf'
else:
	print('Error al introducir el nombre de la carpeta')
	quit()

#Cambiamos el path a la carpeta seleccionada
os.chdir('/home/batsim/caebat/vibe/examples/'+nombre)


#Ejectuamos la simulacion
os.system('/home/batsim/caebat/oas/install/bin/ips.py --simulation='+modelo+' --log=temp.log --platform=../config/batsim.conf -a')
os.chdir('/home/batsim/caebat/vibe/examples')
copiar_simulacion(nombre)
eliminar_carpetas(nombre)
print('Fin de la simulación')
