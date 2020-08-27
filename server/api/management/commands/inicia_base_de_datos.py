from django.core.management.base import BaseCommand, CommandError
import json
from datetime import datetime
from datetime import timedelta
import random

from api.models import Variable, Unidad, Proyecto, Sensor, Lectura
from django.contrib.auth.models import User, Group 

class Command(BaseCommand):
	
	def add_arguments(self, parser):
		parser.add_argument('estadobase', type=str)
		#parser.add_argument('estaciones', type=str)

	def handle(self, *args, **options):
		try:
			with open(options['estadobase']) as f:
				data = json.load(f)    		
		except Exception as inst:
			# print("[INFO] No se pudieron cargar las redes: {}".format(str(inst)))
			raise(Exception("[INFO] No se pudo cargar el estado base: {}".format(str(inst))))

		# USERS
		for user in data["users"]:
			try:
				u = User(username = user['username'], password = user["password"])
				u.save()
			except Exception as inst:
				print(str(inst))

		# GROUPS
		for group in data["groups"]:
			try:
				g = Group(name = group)
				g.save()
			except Exception as inst:
				print(str(inst))

		# VARIABLE
		for var in data["variables"]:
			try:
				v = Variable(nombre = var["nombre"], descripcion = var["descripcion"])
				v.save()
			except Exception as inst:
				print(str(inst))

		# UNIDAD
		for uni in data["unidades"]:
			try:
				u = Unidad(abreviacion = uni["abreviacion"], nombre = uni["nombre"])
				u.save()
			except Exception as inst:
				print(str(inst))

		# PROYECTOS
		for proj in data["proyectos"]:
			try:
				user = User.objects.get(username = proj["propietario"])
				group = Group.objects.get(name = proj["grupo"])
				p = Proyecto(propietario = user, grupo = group, nombre = proj["nombre"])
				p.save()
			except Exception as inst:
				print(str(inst))
		
		# SENSORES
		for sen in data["sensores"]:
			try:
				proj = Proyecto.objects.get(nombre = sen["proyecto"])
				var = Variable.objects.get(nombre = sen["variable"])
				unit = Unidad.objects.get(abreviacion = sen["unidad"])
				s = Sensor(nombre = sen["nombre"], descripcion = sen["descripcion"], uuid = sen["uuid"], variable = var, unidad = unit, proyecto = proj)
				s.save()
			except Exception as e:
				print(str(e))

		# LECTURAS
		for s in Sensor.objects.all():
			try:
				lec = Lectura(sensor = s, medido = datetime.now(), valor = random.random())
				lec.save()
			except Exception as inst:
				print(str(inst))

