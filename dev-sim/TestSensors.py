"""
Para ejecutar los test tenemos las siguientes opciones
python -m unittest TestClass.py
python -m unittest TestClass.TestSubmodule
python -m unittest TestClass.TestSubmodule.test_function
"""
import unittest

from Sensor import Sensor
class TestSensor(unittest.TestCase):
	# Se prueban las funcionalidades básicas de un sensor
	
	def test_sensor(self):
		sensor = Sensor()
		reading, timestamp = sensor.get_reading()
		self.assertEqual(reading, None)
		self.assertEqual(timestamp, None)

	def test_transform(self):
		sensor = Sensor()
		res = sensor.transform(5) # un sensor sin especificacón de transformación devuelve la función identidad
		self.assertEqual(res, 5)

		sensor = Sensor(transformRule = 'x*5')
		res = sensor.transform(5)
		self.assertEqual(res, 25)	

from RandomSensor import RandomSensor
class TestRandomSensor(unittest.TestCase):

	def test_random_sensor(self):
		sensor = RandomSensor()
		reading, timestamp = sensor.get_reading()
		self.assertEqual(timestamp, None)

	def test_transform(self):
		sensor = RandomSensor()
		reading, timestamp = sensor.get_reading()
		res = sensor.transform(reading)
		self.assertEqual(res, res)

		sensor = RandomSensor(transformRule = 'x*5')
		reading, timestamp = sensor.get_reading()
		res = sensor.transform(reading)
		self.assertEqual(res, reading*5)

from NovusSensor import NovusSensor
class TestNovusSensor(unittest.TestCase):

	def test_novus_sensor(self):
		sensor = NovusSensor("cik", "alias")
		transformRule = sensor.transformRule
		print(transformRule)
		self.assertEqual(transformRule, "x") # un sensor sin especificacon de transformación debería entregar "x"
		res = sensor.transform(5)
		self.assertEqual(res, 5)

		sensor = NovusSensor("cik", "alias", transformRule="2+x")
		res = sensor.transform(5)
		self.assertEqual(res, 7)

		sensor = NovusSensor("cik", "alias", transformRule="5.31*(1.6-x)")
		res = sensor.transform(5)
		self.assertEqual(res, 5.31*(1.6-5))		