#-*- encoding:utf-8 -*-
from auxiliares import MSR
class VLSM(object):
	"""Genera tabla"""
	def __init__(self,deptos,ip):
		#Ordena los departamentos de mayor a menos segun el numero de bits de host
		self.deptos = sorted(deptos, key=lambda k: k['hosts'],reverse = True)
		self.numero_deptos = len(deptos)
		self.ip = ip
		self.deptos_vlsm = []

	def add_deptos_libres(self,deptos):
		tipoIP = (self.ip).getTipo()
		#Determina el numero maximo de bits de hosts y agrega X cantidad para evitar errores
		if tipoIP is 'C':
			rango = 8
			bitex = 1
		elif tipoIP is 'B':
			rango = 16
			bitsex = 2
		elif tipoIP is 'A':
			rango = 24
			bitsex = 2
		else:
			print "Oh rayos! add_deptos_libres"
			exit(1)

		#Determina numero de hosts libres
		libres = ((self.ip).getHosts() + bitsex) - self.totalHosts()
		#Calcula subredes libres
		lbs = self.calculaLibres(libres,rango)

		deptos_libres = []
		#Genera el 'numero' de red libre 'al revés'
		libre_id = range(1,len(lbs)+1)
		libre_id.reverse()
		c = 0
		#Agrega configuracion basica a cada sred libre
		for l in lbs:
			deptos_libres.append({
				'nombre': 'Libre ' + str(libre_id[c]),
				'red': '',
				'broadcast': '',
				'hosts':l[0] - 2,
				'bits_host':l[1],
				'msr': ''
			})
			c += 1
		#Ordena de menor a mayor
		deptos_libres_sort = sorted(deptos_libres, key=lambda k: k['hosts'],reverse = False)
		#Agrega la subredes y su configuracion basica a 'todos los departamentos'
		for depto_libre in deptos_libres_sort:
			deptos.append(depto_libre)

		return deptos

	#Comprueba que se pueda realizar la operacion
	def validar(self):
		r = (self.ip).hostsDisponibles(self.totalHosts())
		self.deptos = self.add_deptos_libres(self.deptos)
		return r

	#Calcula el total de Host segundo los requerimientos dados
	def totalHosts(self):
		h = 0
		for d in self.deptos:
			h += pow(2,d['bits_host'])
		return h
	#Calcula la tabla de VLSM
	def calcula(self):
		tipo_ip = (self.ip).tipo
		#Calcula para IP clase C
		if tipo_ip is 'C':
			#Define ultimo broadcast por default 00000000
			ultimo_bc = '00000000'
			for d in self.deptos:
				bits_host = d['bits_host']
				
				#La porcion de red y broadcast se basa en el ultimo broadcast asignado menos los bits de host requeridos
				porcion_red = ultimo_bc[:-bits_host]
				porcion_broadcast = ultimo_bc[:-bits_host]
				#Por cada bit de host se agrega 0 ó 1 para IP de Red o Broadcast
				for bit in range(0,bits_host):
					porcion_red += '0'
					porcion_broadcast += '1'
				#Se forman IP's de Red y broadcast
				d['red'] = (self.ip).getOctetos(3) + '.' + str(int(porcion_red,2))
				d['broadcast'] = (self.ip).getOctetos(3) + '.' + str(int(porcion_broadcast,2))
				d['msr'] = MSR(d['bits_host'],(self.ip).getTipo())
				#Se cambia el último octeto de la última direccion de broadcast asignada
				ultimo_bc = bin(int(porcion_broadcast,2)+1)

		#Calcula para IP clase B
		elif tipo_ip is 'B':
			ultimo_bc_1 = '00000000'
			ultimo_bc_2 = '00000000'

			for d in self.deptos:
				bits_host = d['bits_host']

				if bits_host > 8:
					bits_octeto1 = bits_host - 8
					bits_octeto2 = 8
				else:
					bits_octeto1 = 0
					bits_octeto2 = bits_host

				if bits_octeto1 > 0:
					porcion_red_1 = ultimo_bc_1[:-bits_octeto1]
					porcion_broadcast_1 = ultimo_bc_1[:-bits_octeto1]
				else:
					porcion_red_1 = ultimo_bc_1
					porcion_broadcast_1 = ultimo_bc_1

				porcion_red_2 = ultimo_bc_2[:-bits_octeto2]
				porcion_broadcast_2 = ultimo_bc_2[:-bits_octeto2]

				for bit in range(0,bits_octeto1):
					porcion_red_1 += '0'
					porcion_broadcast_1 += '1'

				for bit in range(0,bits_octeto2):
					porcion_red_2 += '0'
					porcion_broadcast_2 += '1'


				ultimo_bc_1 = int(porcion_broadcast_1,2)
				ultimo_bc_2 = int(porcion_broadcast_2,2)

				d['red'] = (self.ip).getOctetos(2) + '.' + str(int(porcion_red_1,2)) + '.' + str(int(porcion_red_2,2))
				d['broadcast'] = (self.ip).getOctetos(2) + '.' + str(int(porcion_broadcast_1,2)) + '.' + str(int(porcion_broadcast_2,2))
				d['msr'] = MSR(d['bits_host'],(self.ip).getTipo())

				ultimo_bc_2 += 1

				if ultimo_bc_2 > 255:
					ultimo_bc_2 = 0
					ultimo_bc_1 += 1

				ultimo_bc_1 = bin(ultimo_bc_1)
				ultimo_bc_2 = bin(ultimo_bc_2)

		#Calcula para IP clase A
		elif tipo_ip is 'A':
			ultimo_bc_1 = '00000000'
			ultimo_bc_2 = '00000000'
			ultimo_bc_3 = '00000000'
			for d in self.deptos:
				bits_host = d['bits_host']

				if bits_host > 16:
					bits_octeto3 = bits_host - 16
					bits_octeto2 = 8
					bits_octeto1 = 8
				elif bits_host > 8:
					bits_octeto1 = 0
					bits_octeto2 = bits_host - 8
					bits_octeto3 = 8
				else:
					bits_octeto1 = 0
					bits_octeto2 = 0
					bits_octeto3 = bits_host
				
				if bits_octeto1 > 0:
					porcion_red_1 = ultimo_bc_1[:-bits_octeto1]
					porcion_broadcast_1 = ultimo_bc_1[:-bits_octeto1]
				else:
					porcion_red_1 = ultimo_bc_1
					porcion_broadcast_1 = ultimo_bc_1

				if bits_octeto2 > 0:
					porcion_red_2 = ultimo_bc_2[:-bits_octeto2]
					porcion_broadcast_2 = ultimo_bc_2[:-bits_octeto2]
				else:
					porcion_red_2 = ultimo_bc_2
					porcion_broadcast_2 = ultimo_bc_2

				porcion_red_3 = ultimo_bc_3[:-bits_octeto3]
				porcion_broadcast_3 = ultimo_bc_3[:-bits_octeto3]


				for bit in range(0,bits_octeto1):
					porcion_red_1 += '0'
					porcion_broadcast_1 += '1'

				for bit in range(0,bits_octeto2):
					porcion_red_2 += '0'
					porcion_broadcast_2 += '1'

				for bit in range(0,bits_octeto3):
					porcion_red_3 += '0'
					porcion_broadcast_3 += '1'


				ultimo_bc_1 = int(porcion_broadcast_1,2)
				ultimo_bc_2 = int(porcion_broadcast_2,2)
				ultimo_bc_3 = int(porcion_broadcast_3,2)

				ultimo_bc_1 += 1
				if ultimo_bc_1 > 255:
					ultimo_bc_1 = 0
					ultimo_bc_2 += 1
					if ultimo_bc_2 > 255:
						ultimo_bc_2 = 0
						ultimo_bc_3 += 1 

				d['red'] = (self.ip).getOctetos(1) + '.' + str(int(porcion_red_1,2)) + '.' + str(int(porcion_red_2,2)) + '.' + str(int(porcion_red_3,2))
				d['broadcast'] = (self.ip).getOctetos(1) + '.' + str(int(porcion_broadcast_1,2)) + '.' + str(int(porcion_broadcast_2,2)) + '.' + str(int(porcion_broadcast_3,2))
				d['msr'] = MSR(d['bits_host'],(self.ip).getTipo())

				ultimo_bc_1 = bin(ultimo_bc_1)
				ultimo_bc_2 = bin(ultimo_bc_2)
				ultimo_bc_3 = bin(ultimo_bc_3)

				print " %d.%d.%d" % (int(str(ultimo_bc_1),2),int(str(ultimo_bc_2),2),int(str(ultimo_bc_3),2),)
		#Calcula para ... ¿? No sé, seguramente un error
		else:
			print "Oh rayos! calcula: if = ? :"
			exit(1)

		#Despues de calcular imprime la tabla
		self.imprimir()

	#Cambia la IP
	def setIP(self,ip):
		self.ip = ip

	#Devuelve lista con subredes que quedan libres
	def calculaLibres(self,bitsL,rangoBits):
		#Lista que contiene numero de hosts que quedan libres
		libres = [bitsL]
		rlibres = []

		#Genera potencia maxima  que puede contener a los hosts libres en base a la clase de IP
		r = range(0,rangoBits)
		#Por cada libre que existra se calcula quien puede contenerlo
		for l in libres:
			prev = pow(2,rangoBits)
			flag = False
			#Por cada potencia de 2 en el rango, basado en el numero máximo de hosts según clase de IP
			for p in r:
				#Calcula potencia de 2
				this = pow(2,p)
				#Si al elevar fue exacto
				if this == l:
					#Numero de hosts
					bits = this
					#Potencia que contiene al numero de hosts
					pbits = p
					#La potencia fue exacta
					flag = True
					break
				#Se ha exedido la potencia que puede contenerlo
				if this > l:
					flag = False
					break
				#Si no hubo potencia exacta
				#Se guarda el anterior, es decir uno menor a este
				prev = this
				#Se guarda la potencia que genera [prev]
				pbits = p

			#Si hubo potencia exacta
			if flag:
				#En la lista de subredes libres, se agrega numero de hosts y potencia que le pueden contener
				rlibres.append((bits,pbits))
				del libres[0]
			else:
				#Elimina primer elemento de la lista (por el que se pasa actualmente)
				del libres[0]
				
				#Se guarda la informacion del anterior, pues es obvio que sera una potencia exacta
				rlibres.append((prev,pbits))
				#Agrega un 0 (puede ser cualqueir numero), para brincar el paso actual del ciclo
				libres.append(0)
				#Se agrega como hosts disponibles sin asignar una potencia cercana a la lista libres
				libres.append((l - prev))

		#print rlibres
		return rlibres

	#Imprime la 'tabla'
	def imprimir(self):
		for d in self.deptos:
			print 'ND: %s /%d \t \n\t|DSR: \t %s \t \n\t|DB: \t %s \t \n\t|MSR: \t %s '	% (d['nombre'],32-d['bits_host'],d['red'],d['broadcast'],d['msr'],)
