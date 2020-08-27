# Clase que implementa el concepto abstracto de un Device
# Un device es un objeto compuesto que debe tener las siguientes funcionalidades. 
#  - obtener lecturas
#	 - enviar mensajes
#  - mantener un loop con el que realizar lecturas y enviar los mensajes

import time
from datetime import datetime
import uuid

def unix_timestamp():
	# Devuelve un timestamp en formato unix
	return time.time()

def isoformat_timestamp():
	# devuelve un timestamp en isoformat utc
	t = time.time()
	return datetime.utcfromtimestamp(t).isoformat()

class Device():
	# IoT Device Model

	def __init__(self, reading_interval, messenger, sensor, uuid_ = None, format = 'isoformat'):
		#	Constructor del device. 
		#	Acá se hace la composición del device mediante la integración con objetos Messenger. 
		# Notar el uso del patrón de diseño Composite. 
		#	y Sensor. 
		# PARAMS
		#		reading_interval:float segundos entre lecturas y envíos de datos
		#   messenger:<Messenger Object> objeto Mensajero encargado de realizar el envío de datos a un servidor
		#		sensor:<Sensor Object> objeto Sensor encargado de realizar las lecturas de una variable
		#		format:string in ['unix', 'isoformat'] formato de timestamp en caso de que el sensor no sepa leer timestamps
		self.uuid = uuid_
		if uuid_ is None:
			self.uuid = str(uuid.uuid4())

		self.reading_interval = reading_interval
		self.messenger = messenger
		self.sensor = sensor
		if format == 'unix':
			self.timestamp = unix_timestamp
		else:
			self.timestamp = isoformat_timestamp

	def run(self):
		# loop-function encargada de hacer los llamados para obtener las lecturas y 
		# hacer el envío de la información

		while True:
			t1 = time.time()
			
			# Se realiza la lectura desde el sensor
			try:
				lectura, timestamp = self.sensor.get_reading()
			except Exception as inst:
				print("[INFO] Excepcion intentando realizar lectura del sensor: {}".format(str(inst)))
				lectura = None

			if lectura is not None:		
				# Se configura el timestamp en caso de que el sensor no sepa de timestamps
				if timestamp is None:
					timestamp = self.timestamp()

				# Se realiza el envío de la información
				try:
					self.messenger.send_data(lectura, timestamp, self.uuid)
				except Exception as inst:
					print("[INFO] Excepcion intentando enviar datos al servidor: {}".format(str(inst)))

			# se calcula el lag entre lectura y envío para compensar en la espera
			t2 = time.time()

			# se duerme el proceso durante el tiempo necesario para cumplir lo configurado
			time.sleep(self.reading_interval + t1 - t2)
