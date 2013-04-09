#-*- encoding:utf-8 -*-
from auxiliares import MSR
class VLSM(object):
	"""Genera tabla"""
	def __init__(self,deptos,num_deptos,ip):
		#Ordena los departamentos de mayor a menos segun el numero de bits de host
		self.deptos = sorted(deptos, key=lambda k: k['hosts'],reverse = True)
		self.numero_deptos = len(deptos)
		self.ip = ip
		self.deptos_vlsm = []

	def deptoss(self,deptos):
		libres = 256 - self.totalHosts()
		lbs = self.calculaLibres(libres)

		c = 0
		t = 0
		for l in lbs:
			t += l[0]
			c += 1
			deptos.append({
				'nombre': 'Libre ' + str(c),
				'red': '',
				'broadcast': '',
				'hosts':l[0],
				'bits_host':l[1],
				'msr': '255.255.255.0'
			})

		print t

		return sorted(deptos, key=lambda k: k['hosts'],reverse = True)

	#Comprueba que se pueda realizar la operacion
	def validar(self):
		r = (self.ip).hostsDisponibles(self.totalHosts())
		self.deptos = self.deptoss(self.deptos)
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
				pass
				
				
				print " %s.%s.%s" % (int(ultimo_bc_1,2),int(ultimo_bc_2,2),int(ultimo_bc_3,2),)
		#Calcula para ... ¿? No sé, seguramente un error
		else:
			pass

		#Despues de calcular imprime la tabla
		self.imprimir()

	#Cambia la IP
	def setIP(self,ip):
		self.ip = ip

	def calculaLibres(self,bitsL):
		clase = 'C'

		if clase is 'C':
			libres = [bitsL]
			rlibres = []
			r = range(0,8)
			for l in libres:
				prev = 255
				flag = False
				for p in r:
					this = pow(2,p)

					if this == l:
						bits = this
						pbits = p
						flag = True
						break
					if this > l:
						flag = False
						break
					
					prev = this
					pbits = p

				if flag:
					rlibres.append((bits,pbits))
					del libres[0]
					print libres
				else:
					del libres[0]
					
					rlibres.append((prev,pbits))
					libres.append(0)
					libres.append((l - prev))

			return rlibres

	#Imprime la 'tabla'
	def imprimir(self):
		for d in self.deptos:
			print 'ND: %s /%d \t \n\t|DSR: \t %s \t \n\t|DB: \t %s \t \n\t|MSR: \t %s '	% (d['nombre'],32-d['bits_host'],d['red'],d['broadcast'],d['msr'],)
