import random
from Sensor import Sensor

class RandomSensor(Sensor):

	def get_reading(self):
		return random.random(), None

