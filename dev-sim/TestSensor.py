from Sensor import Sensor

sensor = Sensor(transformRule="5*x - 2*x*x")
print(sensor.transform(5))