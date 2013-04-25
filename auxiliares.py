# -*- encoding:utf-8 -*-
from IP import IP
import os

clear = lambda: os.system('cls') #Windows
# clear = lambda: os.system('cls') #Linux

def MSR(msr,clase):
	if clase is 'C': #Es clase C
		bits_sr = 8 - msr
		rango = range(0,8)
		rango.reverse()
		rango = rango[:bits_sr]
		mascara = 0
		for c in rango:
			mascara += pow(2,c)
		mascara = '255.255.255.' + str(int(mascara))
	elif clase is 'B':
		bits_sr = 16 - msr
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
	elif clase is 'A':
		bits_sr = 24 - msr
		octeto1 = 0
		octeto2 = 0
		octeto3 = 0

		if bits_sr > 16:
			bits_sr_octeto1 = bits_sr - 16
			bits_sr_octeto2 = 8
			bits_sr_octeto3 = 8
		elif bits_sr > 8:
			bits_sr_octeto1 = 0
			bits_sr_octeto2 = bits_sr - 8
			bits_sr_octeto3 = 8
		else:
			bits_sr_octeto1 = 0
			bits_sr_octeto2 = 0
			bits_sr_octeto3 = bits_sr

		rango = range(0,8)
		rango.reverse()
		rango1 = rango[:bits_sr_octeto1]
		rango2 = rango[:bits_sr_octeto2]
		rango3 = rango[:bits_sr_octeto3]

		for bit in rango1:
			octeto1 += pow(2,bit)

		for bit in rango2:
			octeto2 += pow(2,bit)

		for bit in rango3:
			octeto3 += pow(2,bit)

		mascara = '255.' +  str(int(octeto3)) + '.' + str(int(octeto2)) + '.' + str(int(octeto1))
	else:
		mascara = '255.ER.R.OR'

	return mascara

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

def getDeptos():
	deptos = []
	num_deptos = 1
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

		#Si no se desea agregar, deja de pedir departamentos
		if continuar is not 1:
			break

	return deptos