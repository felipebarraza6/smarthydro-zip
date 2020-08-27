# Ejecuta una prueba de la funcionalidad de device usando un sensor aleatorio

from Devices import Device
from RandomSensor import RandomSensor
from ConsoleMessenger import ConsoleMessenger

sensor = RandomSensor()
messenger = ConsoleMessenger()
reading_interval = 5 # segundos

device = Device(reading_interval, messenger, sensor)
device.run()
