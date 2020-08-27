from api.models import Sensor, Unidad, Proyecto, Lectura, Variable
from django.contrib.auth.models import User, Group
from datetime import datetime
from datetime import timedelta
import random
"""
#################
## LIMPIEZA DE BD
#################

# Borramos instancias de modelos explicitamente definido, no es necesario eliminar ni usuarios ni grupos


#
Sensor.objects.all().delete()
Unidad.objects.all().delete()
Proyecto.objects.all().delete()
Lectura.objects.all().delete()
Variable.objects.all().delete()

### VARIABLES
v1=Variable(nombre="Temperatura", descripcion="Medición de actividad cinemática molecular")
v1.save()
v2=Variable(nombre="Luminosidad", descripcion="Medición de cantidad de flujo de luz")
v2.save()
v3=Variable(nombre="Ultrasonido", descripcion="Medicion de distancia usando ondas de ultrasonido")
v3.save()
Variable(nombre="CO2", descripcion="Medicion de presencia de CO2 disuelto").save()
Variable(nombre="O2", descripcion="Medicion de presencia de oxígeno disuelto").save()
v4=Variable(nombre="Flujo", descripcion="Medicion del paso de un volumen de un fluido por unidad de tiempo")
v4.save()
Variable(nombre="Velocidad", descripcion="Medicion de una distancia recorrida por unidad de tiempo").save()
Variable(nombre="Presión", descripcion="Medicion de unidad de Fuerza por unidad de superficie").save()

### UNIDADES
u1=Unidad(abreviacion="°C", nombre="Grados Centígrados")
u1.save()
Unidad(abreviacion="°F", nombre="Grados Farenheit").save()
Unidad(abreviacion="PPM", nombre="Partes por millón").save()
u2=Unidad(abreviacion="m", nombre="metros")
u2.save()
u3=Unidad(abreviacion="Lt/s", nombre="Litros por segundo")
u3.save()
Unidad(abreviacion="m/s", nombre="metros por segundo").save()
u4=Unidad(abreviacion="lx", nombre="Lux")
u4.save()
Unidad(abreviacion="Pa", nombre="Pascales").save()
Unidad(abreviacion="Psi", nombre="Pounds per square inch").save()
Unidad(abreviacion="bar", nombre="Bares").save()

### PROYECTOS
# Necesario obtener usuarios
gus = User.objects.all()[0]
print(gus.username)
ussadmin = User.objects.all()[1]
print(ussadmin.username)

# Necesario obtener grupos
quasar = Group.objects.all()[0]
uss = Group.objects.all()[1]

p1 = Proyecto(nombre="Quasar-Santiago-City", propietario=gus, grupo=quasar)
p1.save()
p2 = Proyecto(nombre="USS-CampusCentral", propietario=ussadmin, grupo=uss)
p2.save()

### SENSORES
UUID1 = "3432bc26-8950-4317-a6fb-b2231810c760"
UUID2 = "19994c8d-0720-4ef1-9d8b-91eeb6bbb456"
UUID3 = "283b8f83-2ca6-4e98-8429-52e2b7400595"
UUID4 = "925730b2-4d1f-46f9-aea4-37ba785b8774"
UUID5 = "54f50b5d-7230-47d5-a17d-a41b538140c9"
UUID6 = "a52e242d-0f10-4bca-9b23-d2afcc9eb358"
UUID7 = "d7e632c5-00a2-41aa-972b-a371ae5acd34"
UUID8 = "d98e4a51-1173-4761-aa92-6078a1231184"
UUID9 = "72c1f25f-8a68-438a-a78a-2f8d1332c5e0"
UUID10 = "e12a6ee7-17aa-4e2c-8b6f-3687ded424c3"
s1.save()
s2 = Sensor(nombre="HLT Temp", descripcion="Temperatura de Hot liquor tank", uuid=UUID2, unidad=u1, variable=v1, proyecto=p1)
s2.save()
s3 = Sensor(nombre="HLT Profundidad", descripcion="Profundidad de agua en HLT", uuid=UUID3, unidad=u2, variable=v3, proyecto=p1)
s3.save()
s4 = Sensor(nombre="Vorlauf Pump", descripcion="Flujo en bomba de recirculado", uuid=UUID4, unidad=u3, variable=v4, proyecto=p1)
s4.save()
s5 = Sensor(nombre="Fermentador 1 Temp", descripcion="Temperatura en fermentador 1", uuid=UUID5, unidad=u1, variable=v1, proyecto=p1)
s5.save()
s6 = Sensor(nombre="Lux Sala Oriente", descripcion="Luminosidad en Sala Oriente", uuid=UUID6, unidad=u4, variable=v2, proyecto=p2)
s6.save()
s7 = Sensor(nombre="Lux Sala Poniente", descripcion="Luminosidad en Sala Poniente", uuid=UUID7, unidad=u4, variable=v2, proyecto=p2)
s7.save()

# print(Sensor.objects.all())
"""

## LECTURAS
s1 = Sensor.objects.all()[0]# (nombre="Boil Kettle Temp", descripcion="Termometro en el fondo del boil kettle", uuid=UUID1, unidad=u1, variable=v1, proyecto=p1)
s2 = Sensor.objects.all()[1]
s3 = Sensor.objects.all()[2]
s4 = Sensor.objects.all()[3]
s5 = Sensor.objects.all()[4]

interval = timedelta(days=0, hours=0, minutes=2)
INICIO = datetime.now()-timedelta(days=30, hours=0, minutes=0)
FIN = datetime.now()
aux = INICIO
while aux < FIN:
	aux += interval
	Lectura(sensor=s1, recibido=datetime.now(), medido=aux, valor=random.random()).save()
	Lectura(sensor=s2, recibido=datetime.now(), medido=aux, valor=random.random()).save()
	Lectura(sensor=s3, recibido=datetime.now(), medido=aux, valor=random.random()).save()
	Lectura(sensor=s4, recibido=datetime.now(), medido=aux, valor=random.random()).save()
	Lectura(sensor=s5, recibido=datetime.now(), medido=aux, valor=random.random()).save()
	# Lectura(sensor=s6, recibido=datetime.now(), medido=aux, valor=random.random()).save()
	# Lectura(sensor=s7, recibido=datetime.now(), medido=aux, valor=random.random()).save()







