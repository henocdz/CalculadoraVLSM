# -*- encoding:utf-8 -*-

class IP(object):
	"""Define un objeto IP con metodos utilizados en otras clases"""
	def __init__(self,ip='0.0.0.0'):
		self.ip = ip
		self.clasificacion = {
			'A': {'i': '00000000', 'f':'01111111','hosts': pow(2,24) - 2 },
			'B': {'i': '10000000', 'f':'10111111','hosts': pow(2,16) - 2 },
			'C' : {'i': '11000000','f':'11011111','hosts': pow(2,8) - 2 }
		}

	#Validar ip dada
	def validar(self):
		self.octetos = (self.ip).split('.')
		if len(self.octetos) != 4:
			return False
		for o in self.octetos:
			try:
				o = int(o)
			except:
				return False
			if o > 255 or o < 0:
				return False

		#Octeto que sirve para clasificar IP
		oc = int(self.octetos[0])
		clas = self.clasificacion
		for c in clas:
			if  oc >= int(clas[c]['i'],2) and oc <= int(clas[c]['f'],2):
				self.tipo = c
				break
			else:
				self.tipo = None

		self.glue()
		return True


	#Devuelve el tipo de clasificacion que tiene la IP
	def getTipo(self):
		return self.tipo
	
	#Devuelve el numero de host que soporta el tipo de clasificación que es la IP
	def getHosts(self):
		return int(self.clasificacion[self.tipo]['hosts'])

	#Comprueba que los host totales necesarios para este cálculo 'quepan' en el tipo de IP
	#De no ser suficiente esta IP devuelve la clasificacion recomendada
	def hostsDisponibles(self,hosts):
		if hosts < int(self.getHosts()):
			return {'valid':True,'ip_clase':self.tipo}
		else:
			for c in self.clasificacion:
				if hosts < int(self.clasificacion[c]['hosts']):
					return {'valid':False,'ip_clase':c}
			return {'valid':False,'ip_clase':'?'}

	#Devuelve los N primeros octetos de la IP
	def getOctetos(self,octetos = 4):
		ip = ''
		for o in range(0,octetos):
			ip += self.octetos[o] + '.'
		return ip[:-1]

	#Devuelve un octeto de la IP dada en decimal
	def octeto_decimal(self,octeto = 4):
		return int(self.octetos[octeto])

	#Cambiar uno de los octetos de la IP
	def setOcteto(self,octeto,valor):
		if (octeto > 4 or octeto < 1) and (valor > 255 or valor < 0):
			return False

		self.octetos[octeto] = str(valor)
		self.glue()
		return True

	#Genera una sola cadena con el valor de la IP
	def glue(self):
		self.ip = ''
		for octeto in self.octetos:
			self.ip += octeto

	#Convierte a binario la IP
	def toBinary(self):
		self.ip_bin = ''
		#Recorre los octetos guardados y convierte a binario
		for octeto in self.octetos:
			self.ip_bin += bin(int(octeto)) + '.'

		#Elimina último (.) de la IP
		self.ip_bin = self.ip_bin[:-1]
		print self.ip_bin