from Sensor import Sensor
import random

class TransformableRandomSensor(Sensor):

	def __init__(self, transformRule = "x"): 
		super(TransformableRandomSensor, self).__init__( transformRule = transformRule) # para poder hacer uso de la transformación

	def get_reading(self):
		reading = random.random()
		reading = self.transform(reading)
		return reading, None