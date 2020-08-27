# Ejecuta una prueba del device usando un sensor Novus

from Devices import Device
from NovusSensor import NovusSensor
from ConsoleMessenger import ConsoleMessenger

sensorCik = "0ac895fd338ee2a303461a2c1d73ed2ad14f2bb0" 
dataAlias = "3GRECUC1V"

novusSensor = NovusSensor(sensorCik, dataAlias)
messenger = ConsoleMessenger()
reading_interval = 5 # segundos

device = Device(reading_interval, messenger, novusSensor)
device.run()
