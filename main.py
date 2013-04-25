# -*- encoding:utf-8 -*-
import os,time
from math import pow
from VLSM import VLSM
from auxiliares import MSR,getIP,getDeptos
from IP import IP
#Limpia la pantalla
clear = lambda: os.system('cls') #Windows
# clear = lambda: os.system('cls') #Linux

#Obtiene IP valida inicial
#ip = getIP()

#Obtiene departamentos
deptos = getDeptos()

#################r###
ip = IP()

V  = VLSM(deptos,ip)

ip_s = V.autoIP()
ip = IP(ip_s)

print ip_s

if ip.validar() is True:
	V.setIP(ip)
else:
	exit()

#IP valida para numero de hosts dados
Vvalido = V.validar()
#Si el numero de hosts excede el valor permitido
while Vvalido['valid'] is False:
	clear()
	print 'La IP no es valida para el numero de hosts ['+ str(V.totalHosts()) +'], se recomienda IP de clase: ' +  Vvalido['ip_clase']

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

#La IP soporta el numero de hosts requeridos por el diseño y calcula tabla de VLSM
V.calcula()




