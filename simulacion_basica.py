'''
Creado por Pablo Castro
28/03/17

MODIFICADO 11/05/17 PARA CAEBAT 3.0
Objetivo:
Automatizar todo el proceso de simulacion desde el terminal de linux

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
from time import time

def copiar_simulacion(Nombre_simulacion):
	#Calculamos la fecha en la que la carpeta fue creada
	fecha = os.stat(Nombre_simulacion).st_mtime	

	#La convertimos a un formato legible y nombramos la nueva carpeta
	nombre_carpeta_copia = Nombre_simulacion + ' ' + str(datetime.fromtimestamp(fecha))
	shutil.copytree(Nombre_simulacion,nombre_carpeta_copia)
	shutil.move(nombre_carpeta_copia,'/home/batsim/Desktop/Mis simulaciones/')

def eliminar_carpetas(Nombre_simulacion):
	shutil.rmtree('/home/batsim/caebat/vibe/examples/'+Nombre_simulacion+'/simulation_log')
	shutil.rmtree('/home/batsim/caebat/vibe/examples/'+Nombre_simulacion+'/simulation_setup')
	shutil.rmtree('/home/batsim/caebat/vibe/examples/'+Nombre_simulacion+'/work')
	shutil.rmtree('/home/batsim/caebat/vibe/examples/'+Nombre_simulacion+'/simulation_results')



#Seleccionamos desde el terminal nuestra carpeta de simulacion
print('Introduce el nombre de la carpeta que quieres simular:')
nombre = raw_input()

#Iniciamos el contador de tiempo de ejecucion
tiempo_inicial = time()

#Seleccionamos el archivo .conf que vamos a simular
if nombre == 'case1':
	modelo = 'thermal_chartran_cell_twoway.conf'
elif nombre == 'case2':
	modelo = 'thermal_electrical_chartran_cell_twoway.conf'
elif nombre == 'case3':
	modelo = 'thermal_electrical_chartran_battery_twoway.conf'
elif nombre == 'case6':
	modelo = 'thermal_electrical_chartran_farasis.conf'
elif nombre == 'case7':
	modelo = 'thermal_electrical_chartran_module_4S.conf'
elif nombre == 'case10':
	modelo = 'thermal_chartran_battery_hppc.conf'
elif nombre == 'caso_propio1':
	modelo = 'thermal_electrical_chartran_cell_twoway.conf'
else:
	print('Error al introducir el nombre de la carpeta')
	quit()

#Cambiamos el path a la carpeta seleccionada
os.chdir('/home/batsim/caebat/vibe/examples/'+nombre)

#Ejectuamos la simulacion
os.system('/home/batsim/caebat/ipsframework-code/install/bin/ips.py --simulation='+modelo+' --log=temp.log --platform=../config/batsim.conf -a')
os.chdir('/home/batsim/caebat/vibe/examples')
copiar_simulacion(nombre)
eliminar_carpetas(nombre)

#Calculamos el tiempo de ejecucion
tiempo_final = time()
tiempo_ejecucion = str((tiempo_final - tiempo_inicial)/60)

#Mensaje indicando el final del proceso
print('FIN DE LA SIMULACION')
print('TIEMPO EMPLEADO: %s minutos' %tiempo_ejecucion)
