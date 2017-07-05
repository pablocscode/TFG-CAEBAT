# -*- coding: utf-8 -*-
'''
Creado por Pablo Castro
15/05/17

PARA CAEBAT 3.0
Objetivo:
Automatizar todo el proceso de simulacion con segmentos desde el terminal de linux

Acciones:
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

def leer_numero_segmentos(Nombre_simulacion):
    os.chdir('/home/batsim/caebat/vibe/examples/%s/input' %Nombre_simulacion)
    input_keyvalue = open('input_keyvalue','r')
    lineas = input_keyvalue.readlines()
    input_keyvalue.close()

    for linea in lineas:
        vector_linea = linea.strip('\n').split('=')
        if vector_linea[0]=='NUMSEG':
            break
    os.chdir('/home/batsim/caebat/vibe/examples/%s' %Nombre_simulacion)
    return int(vector_linea[1])
    

def eliminar_ultimo_segmento(Modelo,Nombre_simulacion):
    datos_conf = open(Modelo,'r')
    lineas_conf = datos_conf.readlines()
    datos_conf.close()
    
    datos_conf = open(Modelo,'w')
    for line in lineas_conf:
        vector_conf = line.strip('\n').split('=')
        if vector_conf[0]=='   VALUES ':
            vector_valores = vector_conf[1].split()
            vector_valores.pop()
            line = '   VALUES = '+' '.join(vector_valores)
        datos_conf.write(line)
    datos_conf.close()
    
    os.chdir('/home/batsim/caebat/vibe/examples/'+nombre+'/input')
    datos_input_keyvalue = open('input_keyvalue','r')
    lineas_input_keyvalue = datos_input_keyvalue.readlines()
    datos_input_keyvalue.close()
    
    datos_input_keyvalue = open('input_keyvalue','w')
    for line in lineas_input_keyvalue:
        vector_keyvalue = line.strip('\n').split('=')
        if vector_keyvalue[0]== 'NUMSEG':
            line = 'NUMSEG='+str(int(vector_keyvalue[1])-1)+'\n'
        elif vector_keyvalue[0]=='CURRDEN':
            vector_valores = vector_keyvalue[1].split(',')
            vector_valores.pop()
            line = 'CURRDEN=' + ','.join(vector_valores)+'\n'
        elif vector_keyvalue[0]=='MODESEG':
            vector_valores = vector_keyvalue[1].split(',')
            vector_valores.pop()
            line = 'MODESEG=' + ','.join(vector_valores)+'\n'
        elif vector_keyvalue[0]=='CUTOFFL':
            vector_valores = vector_keyvalue[1].split(',')
            vector_valores.pop()
            line = 'CUTOFFL=' + ','.join(vector_valores)+'\n'
        elif vector_keyvalue[0]=='CUTOFFH':
            vector_valores = vector_keyvalue[1].split(',')
            vector_valores.pop()
            line = 'CUTOFFH=' + ','.join(vector_valores)+'\n'
        datos_input_keyvalue.write(line)
    datos_input_keyvalue.close()
    os.chdir('/home/batsim/caebat/vibe/examples/'+nombre)
    

"""
INICIO DEL PROGRAMA
"""
#Seleccionamos desde el terminal nuestra carpeta de simulación
print('Introduce el nombre de la carpeta que quieres simular:')
nombre = raw_input()

#Iniciamos el contador de tiempo de ejecución
tiempo_inicial = time.time()

#Creamos la carpeta general que almacenará al resto de carpetas
fecha = time.strftime("%c")
nombre_carpeta_general = nombre + ' Segmentos ' + fecha
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

#Cambiamos el path a la carpeta seleccionada
os.chdir('/home/batsim/caebat/vibe/examples/'+nombre)

#Leemos el numero de segmentos del archivo input_keyvalue
numero_segmentos = leer_numero_segmentos(nombre)

#Ejectuamos la simulacion
for i in range(numero_segmentos-1):
    os.system('/home/batsim/caebat/ipsframework-code/install/bin/ips.py --simulation='+modelo+' --log=temp.log --platform=../config/batsim.conf -a')
    os.chdir('/home/batsim/caebat/vibe/examples')
    copiar_simulacion(nombre,nombre_carpeta_general)
    eliminar_carpetas(nombre)
    os.chdir('/home/batsim/caebat/vibe/examples/'+nombre)
    eliminar_ultimo_segmento(modelo,nombre)
    print('FIN DE SEGMENTO')

#Calculamos el tiempo de ejecucion
tiempo_final = time.time()
tiempo_ejecucion = str(tiempo_final - tiempo_inicial)

#Mensaje indicando el final del proceso
print('FIN DE LA SIMULACION')
print('TIEMPO EMPLEADO: %s minutos' %tiempo_ejecucion)
