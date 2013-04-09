# -*- encoding:utf-8 -*-
import os,time
from math import pow
from IP import IP
from VLSM import VLSM

deptos = []
num_deptos = 1

#Limpia la pantalla
clear = lambda: os.system('cls') #Windows

# clear = lambda: os.system('cls') #Linux

#Obtiene IP y la valida
def getIP():
	while True:
		ip = raw_input("Introduce la IP: \t")
		ip = IP(ip)

		#Si la IP no es valida la vuelve a solicitar
		if not ip.validar():
			print "IP no válida"
			continue

		break
	return ip

#Obtiene IP inicial
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
	#Solo clase C

		#Calcula el numero octetos que dejará libres el numero de bits de host
	octetos = msr/8
		#Obtiene el numero de bits de subred que prestara
	

	#Solo Clase C ^^^^

	#Calcula Mascara de Subred para IP de clase C
	#!  Warning: ¿Funciona si quiero cambiar la IP por otra clase?
	if ip.getTipo() is 'C': #Es clase C
		bits_sr = msr%8
		rango = range(0,8)
		rango.reverse()
		rango = rango[:bits_sr]
		mascara = 0
		for c in rango:
			mascara += pow(2,c)
		mascara = '255.255.255.' + str(int(mascara))
	elif ip.getTipo() is 'B':
		bits_sr = msr - 16

		octeto1 = 0
		octeto2 = 0

		if bits_sr > 8:
			bits_sr_octeto2 = bits_sr - 8
			bits_sr_octeto1 = 8
		else:
			bits_sr_octeto1 = bits_sr
			bits_sr_octeto2 = 0

		rango = range(0,8)
		rango.reverse()
		rango1 = rango[:bits_sr_octeto1]
		rango2 = rango[:bits_sr_octeto2]

		for bit in rango1:
			octeto1 += pow(2,bit)

		for bit in rango2:
			octeto2 += pow(2,bit)

		mascara = '255.255.' +  str(int(octeto1)) + '.' + str(int(octeto2))
	else:
		mascara = '255.0.0.0'

	#Guarda el numero departamento con su información
	deptos.append({
		'nombre':nombre_depto,
		'red': '',
		'broadcast': '',
		'hosts':numero_hosts,
		'bits_host':bits,
		'msr': mascara
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




