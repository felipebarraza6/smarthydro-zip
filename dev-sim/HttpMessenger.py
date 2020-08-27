# Clase Mensajera que envía las lecturas al servidor de smarthydro
# Configura el metodo POST segun el formato que recibe el servidor
import requests as rq

class HttpMessenger():

	def __init__(self, dataEndpoint):
		# Constructor
		# PARAMS
		# 	dataEndpoint:string URL a la cual se envían las lecturas
		self.dataEndpoint = dataEndpoint

	def send_data(self, reading, timestamp, uuid):
		# SE CONFIGURA PAYLOAD Y HEADERS
		# En el headers uno ingresa el identificador del sensor
		payload = {}
		payload['valor'] = reading
		payload['medido'] = timestamp

		headers = {}
		headers['UUID'] = uuid


		print("[INFO] headers {}".format(headers))
		print("[INFO] sending data: {}".format(payload))

		try:
			r = rq.post(self.dataEndpoint, data=payload, headers=headers)
			print("[INFO]: response {}".format(r.text))
		except Exception as inst:
			print("[INFO]: Exception caught sending data: {}".format(str(inst)))