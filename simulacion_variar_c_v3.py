# -*- coding: utf-8 -*-
"""
Created on Thu May 11 17:29:37 2017

@author: Pablo
"""

"""
Simulacion variando los distintas intensidades del fichero input_keyvalue
Version 3.1 - Para CAEBAT 3.0
Carpeta propia para cada simulacion (No crea una según fecha -> ARREGLAR)
FUNCIONA PARA CORRIENTES MENORES DE 35A/m^2
"""
import os
import shutil
from datetime import datetime

def copiar_simulacion(Nombre_simulacion,Fecha_simulacion):
	#Calculamos la fecha en la que la carpeta fue creada
	fecha = os.stat(Nombre_simulacion).st_mtime
	
	#La convertimos a un formato legible y nombramos la nueva carpeta
	nombre_carpeta_copia = Nombre_simulacion + ' ' + str(datetime.fromtimestamp(fecha))
	shutil.copytree(Nombre_simulacion,nombre_carpeta_copia)
	shutil.move(nombre_carpeta_copia,'/home/batsim/Desktop/Mis simulaciones/'Nombre_simulacion+' Variar C-rate '+Fecha_simulacion)

#Funcion para eliminar las carpetas una vez acabada la simulacion
def eliminar_carpetas(Nombre_simulacion):
	shutil.rmtree('/home/batsim/caebat/vibe/examples/'+Nombre_simulacion+'/simulation_log')
	shutil.rmtree('/home/batsim/caebat/vibe/examples/'+Nombre_simulacion+'/simulation_results')
	shutil.rmtree('/home/batsim/caebat/vibe/examples/'+Nombre_simulacion+'/simulation_setup')
	shutil.rmtree('/home/batsim/caebat/vibe/examples/'+Nombre_simulacion+'/work')

#NO ES ÚTIL PARA ESTE SCRIPT

#Función para leer el primer dato de la fila y obviar los comentarios de dualfoil.in
def leer_dato(datos_readlines,fila):
    return datos_readlines[fila].split()[0].replace('d','e')

#Función para actualizar la intensidad (ACTUALIZADA A CAEBAT 3.0)
def cambio_intensidad(intensidad,datos_readlines):
    linea_simulacion = datos_readlines[19].split('=')
    linea_simulacion[1] = str(intensidad)
    datos_readlines[19] = '='.join(linea_simulacion)+'\n'
    return datos_readlines


"""
Inicio del programa
"""

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

#Distintos C rates (0.2, 0.5, 1, 2 , 3, 5)
intensidades = [35*0.2, 35*0.5, 35, 35*2, 35*3, 35*5]

#Creamos una carpeta dentro de Mis simulaciones donde guardar los distintos resultados
Fecha_simulacion = datetime.datetime.now()
os.mkdir('/home/batsim/Desktop/Mis simulaciones/' +nombre+ ' Variar C-rate '+ Fecha_simulacion)
print('Carpeta de simulacion creada')
#Bucle en el que actualizamos el valor de la intensidad y simulamos
for intensidad in intensidades:
    #Cambiamos el path a la carpeta seleccionada
    os.chdir('/home/batsim/caebat/vibe/examples/'+nombre+'/input')

    #Leemos los datos del fichero
    key_value = open('input_keyvalue','r')
    datos = key_value.readlines()
    key_value.close()
    
    #Actualizamos el valor de la intensidad
    datos = cambio_intensidad(intensidad,datos)
    #Sobreescribimos el fichero
    key_value = open('input_keyvalue','w')
    for line in range(len(datos)):
        key_value.write(str(datos[line]))
    key_value.close()
    
    #Volvemos a la carpeta de simulacion
    os.chdir('/home/batsim/caebat/vibe/examples/'+nombre)
    #Ejectuamos la simulacion
    os.system('/home/batsim/caebat/ipsframework-code/install/bin/ips.py --simulation='+modelo+' --log=temp.log --platform=../config/batsim.conf -a')
    print('Simulación finalizada')
    os.chdir('/home/batsim/caebat/vibe/examples')
    copiar_simulacion(nombre,Fecha_simulacion)
    print('Simulación copiada en Mis simulaciones')
    eliminar_carpetas(nombre)
    print('Carpetas repetidas eliminadas')

print('Fin de las simulaciones')
