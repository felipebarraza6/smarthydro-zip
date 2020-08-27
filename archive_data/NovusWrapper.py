# Clase NovusWrapper
# Incorpora funcionalidades para realizar peticiones al servidor Novus 

import requests as rq 
import json
from datetime import datetime
import pytz

class NovusWrapper:

	def __init__(self, url = "http://m2.exosite.com/onep:v1/rpc/process"):
		# Constructor de la clase
		# PARAMS
		# 	url:string Url del webservice de Novus con el que se solicita el último valor leído
		self.url = url

	@staticmethod
	def parseNovusResponse(responseText):
		# Funcion que parsea lo que devuelve el servicio de Novus cuando se solicita el último dato de un sensor. 
		# PARAMS 
		# 	responseText:string es un string que tiene el siguiente formato (según se ha investigado)
		# 			responseText = "[{'id': 0, 'result': [[1573908263, -3200.0]], 'status': 'ok'}]"
		# 		En caso de que el servidor haya encontrado un error, se ha visto el siguiente formato de respuesta
		# 			responseText = "[{'error': {'message': 'Can not apply Arguments to Procedure', 'code': 501}, 'id': 0}]"	
		# 		En cuaquier caso puede ser parseado como un json
		# OUTPUT
		# 	value:number valor de la lectura leída por NOVUS
		# 	timestamp:UNIX-TIMESTAMP from epoch
		# 	isoformat:timestamp en isoformat UTC
		# RAISES
		# 	"Formato de respuesta Novus no identificado": El formato del texto no es JSON o no es tipo array
		#		"Dato no pudo ser leido por Novus: {NOVUS-MSG}": El envío a novus no fue correcto
		#		"Formato interno de respuesta no identificado":  novus respondió correctamente pero no se pudo parsear el contenido interno

		try:
			data = json.loads(responseText)
		except:
			raise Exception("Formato de respuesta Novus no identificado")

		if 'error' in data:
			raise Exception("Dato no pudo ser leido por Novus: {}".format(data['error']['message']))

		try:
			data = data[0]
			value = data['result'][0][1]
			timestamp = data['result'][0][0]
			isoformat = datetime.fromtimestamp(timestamp, pytz.utc).isoformat()
		except:
			raise Exception("Formato interno de respuesta no identificado")

		return value, timestamp, isoformat

	def requestDataFromNovus(sensorCik, dataAlias):
		# Funcion que realiza un request POST al servicio de NOVUS para leer el último dato leído por un sensor
		# PARAMS
		# 	sensorCik:string CIK del sensor (obtenible en portal NOVUS)
		# 	dataAlias:string ALIAS del dato que se quiere leer (obtenible en portal NOVUS)
		# 	url:string URL hacia el servicio de NOVUS. Por defecto se usa la última URL funcional.
		# OUTPUT
		# 	response:<requests response Object>
		# NOTA: No incorpora manejo de excepciones en el request
		payload = {
			"auth": {
				"cik": sensorCik},
			"calls":[
				{
					"procedure":"read",
					"arguments":[
						{
							"alias": dataAlias
						},
						{}],
					"id": 0
				}]
		}

		payload = json.dumps(payload)
		headers = {
		    'content-type': "application/json; charset=utf-8",
		    'cache-control': "no-cache"
		    }

		response = rq.request("POST", self.url, data=payload, headers=headers)
		return response

