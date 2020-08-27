import json
#from NovusSensor import NovusSensor
from TransformableRandomSensor import TransformableRandomSensor
from HttpMessenger import HttpMessenger
from Devices import Device
# Se espera un archivo json con el siguiente formato!
"""
[
	{
		"nombre": "IDENTIFICADOR SOLO PARA AYUDA-MEMORIA",
		"dataEndpoint": "ENDPOINT",
		"deviceUuid": "SMARTHYDRO_UUID",
		"transform":  "VALID_FORMULA",
		"readingInterval": "INTERVALO"
	},
	...
]
"""
# VALID FORMULA: Por ej: "5*x", "1.34*x*x"
# En general se tolera un polinomio!

with open('random-sensors.json', "r") as tf:
	data = json.load(tf)

devices = []
for sensorData in data:
	#novusSensor = NovusSensor(sensorData['sensorCik'], sensorData['dataAlias'], transformRule = sensorData['transform'])
	sensor = TransformableRandomSensor(transformRule = sensorData['transform'])
	readingInterval = sensorData['readingInterval']
	messenger = HttpMessenger(sensorData['dataEndpoint'])
	deviceUuid = sensorData['deviceUuid']

	device = Device(readingInterval, messenger, sensor, uuid_ = deviceUuid)
	devices.append(device)

import threading
for dev in devices:
	dev_thread = threading.Thread(target = dev.run) 
	dev_thread.start()