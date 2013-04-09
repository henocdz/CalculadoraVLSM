# -*- encoding:utf-8 -*-
import os,time
from math import pow
from VLSM import VLSM
from auxiliares import MSR,getIP

deptos = []
num_deptos = 1

#Limpia la pantalla
clear = lambda: os.system('cls') #Windows

# clear = lambda: os.system('cls') #Linux

#Obtiene IP valida inicial
ip = getIP()



#Obtiene departamentos
while True:

	nombre_depto = raw_input("Introduce el nombre de departamento %d : " % num_deptos)
	numero_hosts = raw_input("Numero de hosts: ")

	#Valida que numero de hosts sea entero positivo
	try:
		numero_hosts = int(numero_hosts)
	except:
		print "Debes introducir un numero entero"
		continue

	#Numero de IPs totales necesarias para la subred (incluye direccion de red y broadcast)
	numero_ips = numero_hosts + 2
	
	potencia = 0
	#Obtiene el numero de bits de host necesarios para soportar el numero de IPs requeridas
	while potencia >= 0:
		bits_cercanos = pow(2,potencia)
		#Si el numero IPs es menor al siguiente valor de la potencia de 2 obtiene bits de hosts
		if numero_ips <= bits_cercanos:
			bits = potencia
			break
		potencia += 1

	msr = 32 - bits # Notacion abreviada de Mascara de Subreds

	#Calcula Mascara de Subred para IP de clase C
	#!  Warning: ¿Funciona si quiero cambiar la IP por otra clase?
	
	mascara = MSR(msr,ip.getTipo())

	#Guarda el numero departamento con su información
	deptos.append({
		'nombre':nombre_depto,
		'red': '',
		'broadcast': '',
		'hosts':numero_hosts,
		'bits_host':bits,
		'msr': ''
	})

	#Contador para entorno gráfico
	num_deptos += 1
	
	#Pregunta si se desea agregar otro departamento
	while True:
		continuar = 0
		try:
			continuar = int(raw_input("\n\tAgregar otro departamento [0 .. 1]? \t"))
			break
		except:
			print "Opcion no válida"

	clear()

	#Si no se desea agregar sale de esta parte
	if continuar is not 1:
		break

V  = VLSM(deptos,num_deptos,ip)

#IP valida para numero de hosts dados
Vvalido = V.validar()
#Si el numero de hosts excede el valor permitido
if Vvalido['valid'] is False:
	clear()
	print 'La IP no es valida para el numero de hosts, se recomienda IP de clase: ' +  Vvalido['ip_clase']

	while True:
		cambiar = raw_input('Desea cambiar la IP? [0/1] \t ')
		try:
			cambiar = int(cambiar)
			break
		except:
			continue

	#Sale del programa si no se desea cambiar IP, no se puede realizar calculo
	if cambiar is not 1:
		exit()

	#Obtiene una nueva IP valida
	ip = getIP()
	#Cambia la IP en el motor de VLSM
	V.setIP(ip)
	#time.sleep(3)
else:
	#La IP soporta el numero de hosts requeridos por el diseño y calcula tabla de VLSM
	print V.calcula()




