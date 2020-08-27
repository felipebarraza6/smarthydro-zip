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
	