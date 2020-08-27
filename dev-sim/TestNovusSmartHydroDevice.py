# Realiza una prueba de envío de información al servidor SmartHydro y solciitando la información a un 
# sensor Novus
# Utiliza un mensajero tipo Http
from Devices import Device
from NovusSensor import NovusSensor
from HttpMessenger import HttpMessenger

sensorCik = "0ac895fd338ee2a303461a2c1d73ed2ad14f2bb0" 
dataAlias = "3GRECUC1V"
novusSensor = NovusSensor(sensorCik, dataAlias)

reading_interval = 300 # segundos

dataEndpoint = 'https://smarthydro.central-iot.com/apirest/lecturas/'
messenger = HttpMessenger(dataEndpoint)

deviceUuid = "ed538cb3-4db8-4aa8-ad49-da88ce196f4a"

device = Device(reading_interval, messenger, novusSensor, uuid_ = deviceUuid)
device.run()