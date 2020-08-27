# Realiza una prueba de envío de información al servidor SmartHydro
# Utiliza un mensajero tipo Http
from Devices import Device
from RandomSensor import RandomSensor
from HttpMessenger import HttpMessenger

sensor = RandomSensor()
reading_interval = 120 # segundos

dataEndpoint = 'https://smarthydro.central-iot.com/apirest/lecturas/'
messenger = HttpMessenger(dataEndpoint)

deviceUuid = "d73882fd-a29d-4b5d-9532-a2c257918f89"

device = Device(reading_interval, messenger, sensor, uuid_ = deviceUuid)
device.run()