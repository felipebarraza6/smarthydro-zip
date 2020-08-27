from NovusWrapper import NovusWrapper
from Sensor import Sensor

class NovusSensor(Sensor):

	def __init__(self, sensorCik, dataAlias, transformRule = "x", novusWrapper = None): 
		super(NovusSensor, self).__init__( transformRule = transformRule) # para poder hacer uso de la transformación
		self.sensorCik = sensorCik
		self.dataAlias = dataAlias
		if novusWrapper is None:
			self.novusWrapper = NovusWrapper()
		else:
			self.novusWrapper = novusWrapper

	def get_reading(self):
		novusResponse = self.novusWrapper.requestDataFromNovus(self.sensorCik, self.dataAlias)
		data = novusResponse.text
		reading, timestamp, isoformat = self.novusWrapper.parseNovusResponse(data)

		reading = self.transform(reading)
		return reading, isoformat

	
