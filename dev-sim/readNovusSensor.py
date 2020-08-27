# script de ejemplo para mostrar como se extrae el último dato envíado por un device al servidor de novus

import requests as rq 
import json
from datetime import datetime
import pytz

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

def requestDataFromNovus(sensorCik, dataAlias, url = "http://m2.exosite.com/onep:v1/rpc/process"):
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

	response = rq.request("POST", url, data=payload, headers=headers)
	return response

sensorCik = "0ac895fd338ee2a303461a2c1d73ed2ad14f2bb0" 
dataAlias = "3GRECUC1V"

response = requestDataFromNovus(sensorCik, dataAlias)
data = response.text
value, timestamp, isoformat = parseNovusResponse(data)
print("value: {}, date: {}, isoformat: {}".format(value, timestamp, isoformat))

#parseResponse = json.loads(response.text)
#data = parseResponse[0]
#print(data)
#print(response.text)

