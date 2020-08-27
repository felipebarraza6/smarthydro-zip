from NovusWrapper import NovusWrapper

sensorCik = "0ac895fd338ee2a303461a2c1d73ed2ad14f2bb0" 
dataAlias = "3GRECUC1V"

novusWrapper = NovusWrapper()

response = novusWrapper.requestDataFromNovus(sensorCik, dataAlias)
data = response.text
value, timestamp, isoformat = novusWrapper.parseNovusResponse(data)
print("value: {}, date: {}, isoformat: {}".format(value, timestamp, isoformat))