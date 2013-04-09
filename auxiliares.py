# -*- encoding:utf-8 -*-
from IP import IP
def MSR(msr,clase):
	if clase is 'C': #Es clase C
		bits_sr = msr%8
		rango = range(0,8)
		rango.reverse()
		rango = rango[:bits_sr]
		mascara = 0
		for c in rango:
			mascara += pow(2,c)
		mascara = '255.255.255.' + str(int(mascara))
	elif clase is 'B':
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