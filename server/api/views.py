from .serializers import SensorSerializer, UserSerializer
from rest_framework import generics
from rest_framework import permissions
from .authentication import SensorAuthentication
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

############################
## CONFIGURACION DE CLIENTES
############################
from django.conf import settings
# twilio - sms
from twilio.rest import Client 
numFrom = settings.TWILIO_SMS_FROM
accSid = settings.TWILIO_SMS_SID
token = settings.TWILIO_TOKEN
clienteTwilio = Client(accSid, token)

# sendgrid - email
from sendgrid import SendGridAPIClient
sendgridKey = settings.SENDGRIDKEY
sendgridFrom = settings.SENDGRID_EMAIL_FROM
sg = SendGridAPIClient(sendgridKey)
CLIENTES = {'clienteSms': clienteTwilio, 'fromSMS': numFrom, 'clienteEmail': sg, 'fromEmail': sendgridFrom}


#################
## SENSOR - VIEWS
#################
from .models import Sensor
class SensorList(generics.ListAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	queryset = Sensor.objects.all()
	serializer_class = SensorSerializer

	def get_queryset(self):
		# se deben obtener los sensores asociados al usuario autenticado. 
		# un sensor pertenece a un proyecto, y los proyectos a usuarios. 
		# ojo, en este caso no se devuelven los sensores de todo un GRUPO de personas. 
		user = self.request.user
		return Sensor.objects.filter(proyecto__propietario = user)

	def list(self, request):
		# ESTE METODO NO INCLUYE PAGINACION!
		# Note the use of `get_queryset()` instead of `self.queryset`
		queryset = self.get_queryset()
		print("[INFO]: user = {}".format(request.user.username))
		print("[INFO] queryset: {}".format(queryset))
		serializer = SensorSerializer(queryset, many=True, context={'request': request}) # , context= {'request', request}
		return Response(serializer.data)
	
from .permissions import IsSensorOwner
class SensorDetail(generics.RetrieveUpdateAPIView):
	permission_classes = (permissions.IsAuthenticated,IsSensorOwner)
	queryset = Sensor.objects.all()
	serializer_class = SensorSerializer


##################
### ALERTA - VIEWS
##################
# Una alerta se genera en sistema, por lo tanto no es necesario habilitar los métodos post. 
from .models import Alerta 
from .serializers import AlertaSerializer
class AlertaList(generics.ListAPIView):   # ESTA VISTA ES FILTRADA SEGUN LOS SENSORES ASOCIADOS AL USUARIO
	permissions_classes = (permissions.IsAuthenticated,)
	queryset = Alerta.objects.all()
	serializer_class = AlertaSerializer

	def get_queryset(self):
		user = self.request.user
		sensores = Sensor.objects.filter(proyecto__propietario = user)
		alertas = Alerta.objects.filter(sensor__in = sensores)
		return alertas 

	def list(self, request):
		# para bypasear la paginacion
		queryset = self.get_queryset()
		serializer = AlertaSerializer(queryset, many = True, context = {'request': request})
		return Response(serializer.data)

###############
## USER - VIEWS
###############
from django.contrib.auth.models import User
class UserList(generics.ListAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	queryset = User.objects.all()
	serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	queryset = User.objects.all()
	serializer_class = UserSerializer

#################
### GROUP - VIEWS
#################
from .serializers import GroupSerializer
from django.contrib.auth.models import Group
class GroupList(generics.ListAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	queryset = Group.objects.all()
	serializer_class = GroupSerializer


class GroupDetail(generics.RetrieveAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	queryset = Group.objects.all()
	serializer_class = GroupSerializer

####################
### PROYECTO - VIEWS
####################
from .serializers import ProyectoSerializer
from .models import Proyecto
class ProyectoList(generics.ListCreateAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	queryset = Proyecto.objects.all()
	serializer_class = ProyectoSerializer


class ProyectoDetail(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	queryset = Proyecto.objects.all()
	serializer_class = ProyectoSerializer

####################
### LECTURA - VIEWS
####################
from .serializers import LecturaSerializer
from .models import Lectura
class LecturaList(generics.ListCreateAPIView):
	authentication_classes = (SensorAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)
	queryset = Lectura.objects.all()
	serializer_class = LecturaSerializer

	def perform_create(self, serializer):
		channel_layer = get_channel_layer()
		sensor_channel_name = "sensor_"+self.request.user.sensor.uuid
		print("[INFO]: creando lectura. Revisando sensor_channel_name: {}".format(sensor_channel_name))
		if self.request.user.sensor.logging:
			lectura = serializer.save(sensor=self.request.user.sensor)
			self.request.user.sensor.last_logged_value = serializer.data['valor']
			self.request.user.sensor.last_logged_ts = serializer.data['medido']
		self.request.user.sensor.last_received_value = serializer.data['valor']
		self.request.user.sensor.last_received_ts = serializer.data['medido']
		
		# Verificacion de reglas
		for regla in self.request.user.sensor.reglas.all():
			alertar, verificando = regla.verificar(lectura)
			if alertar:
				alerta = Alerta(sensor = self.request.user.sensor, lectura = lectura, verificando = verificando, descripcion = regla.descripcion, umbral = regla.umbral)
				alerta.save()
				for mensajero in regla.mensajeros.all():
					mensaje = mensajero.crearMensaje(verificando)
					respuesta = mensajero.enviarMensaje(mensaje, CLIENTES)
					print("[INFO] Respuesta de mensajero: {}".format(respuesta))

		self.request.user.sensor.save()

		#print(type(serializer.data['valor']))
		#print(type(serializer))
		message = json.dumps({"lectura": serializer.data})
		# async_to_sync(channel_layer.group_send)(sensor_channel_name, {"type": "chat.message", "message": message})

class LecturaDetail(generics.RetrieveAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	queryset = Lectura.objects.all()
	serializer_class = LecturaSerializer

##########################
### ROOT FOR BROWSABLE API
##########################
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
	return Response({
		'users': reverse('user-list', request=request, format=format),
		'sensors': reverse('sensor-list', request=request, format=format),
		'groups': reverse('group-list', request=request, format=format),
		'lecturas': reverse('lectura-list', request=request, format=format)
	})


####################
## VISTAS DE RESUMEN
####################
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ResumenSensorSerializer
from datetime import datetime
from datetime import timedelta
import pandas as pd

class ResumenSensorDetail(APIView):
	"""
	Devuelve una hoja con el resumen de un sensor
	"""
	permission_classes = (permissions.AllowAny,)
	def get(self, request, uuid, format=None):
		# OBTENCION DEL SENSOR
		sensor = Sensor.objects.get(uuid=uuid)

		# # CALCULO DE LAS VARIABLES
		# fechahora = datetime.now()
		# ultimalectura = Lectura.objects.filter(sensor = sensor).latest('medido')
		# print("[INFO] ulima lectura ")
		# print(ultimalectura)

		# ultimo = {'valor': ultimalectura.valor, 'datetime': ultimalectura.medido}

		# resumen_hora = obtener_data_sensor_ultima_hora(sensor)
		# resumen_dia = obtener_data_sensor_ultimo_dia(sensor)
		# resumen_semana = obtener_data_sensor_ultima_semana(sensor)
		# resumen_mes = obtener_data_sensor_ultimo_mes(sensor)
		
		# mydict = {
		# 	'ultimo': ultimo,
		# 	'resumen_hora': resumen_hora,
		# 	'resumen_dia': resumen_dia,
		# 	'resumen_semana': resumen_semana,
		# 	'resumen_mes': resumen_mes
		# }
		# data = {
		# 	"sensor": sensor, 
		# 	'resumen': mydict
		# }
		# serializer = ResumenSensorSerializer(data, context={'request': request})
		serializer = obtener_resumen_sensor(sensor, request)
		return Response(serializer.data)

# Funcion de descarga de datos
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def downloadSensor(request, uuid):
	sensor = Sensor.objects.get(uuid = uuid)
	user = request.user
	if not sensor.proyecto.propietario == user:
		return Response()

	print("[INFO] user: {}".format(user.username))
	qs = Lectura.objects.filter(sensor = sensor)
	qs = qs.values('medido', 'valor')
	print("[INFO] queryset")
	print(qs)
	df = pd.DataFrame.from_records(qs)
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename=filename.csv'

	df.to_csv(path_or_buf=response,sep=',',float_format='%.6f',index=False,decimal=".")
	return response

from .serializers import UserSerializer, ResumenUsuarioSerializer
class ResumenUsuario(APIView):
	"""
	Devuelve los datos de resumen para un usuario
	"""
	permission_classes = (permissions.IsAuthenticated,)
	def get(self, request, format=None):
		user = request.user
		serializer = obtener_resumen_usuario(user, request) #UserSerializer(user, context = {'request': request})
		# print(user)
		return Response(serializer.data)

def obtener_resumen_usuario(user, request):
	"""
	Funcion que devuelve el objeto serializer con la informacion resumen de un usuario
	"""
	data = {}
	data["user"] = user
	projects = Proyecto.objects.filter(propietario = user)
	data["proyecto"] = projects
	
	s = Sensor.objects.none()
	for p in projects:
		s = s | p.sensores.all()
	data["sensor"] = s
	serializer = ResumenUsuarioSerializer(data, context = {"request": request})
	return serializer

def obtener_resumen_sensor(sensor, request):
	"""
	Funcion que devuelve el objeto serializer con la informacion resumen de un sensor
	"""
	fechahora = datetime.now()
	lecturas = Lectura.objects.filter(sensor = sensor)
	if lecturas.count() == 0:
		ultimo = {'valor': None, 'datetime': None}
	else:	
		ultimalectura = Lectura.objects.filter(sensor = sensor).latest('medido')
		ultimo = {'valor': ultimalectura.valor, 'datetime': ultimalectura.medido}
		print("[INFO] ulima lectura ")
		print(ultimalectura)


	resumen_hora = obtener_data_sensor_ultima_hora(sensor)
	resumen_dia = obtener_data_sensor_ultimo_dia(sensor)
	resumen_semana = obtener_data_sensor_ultima_semana(sensor)
	resumen_mes = obtener_data_sensor_ultimo_mes(sensor)
	
	mydict = {
		'ultimo': ultimo,
		'resumen_hora': resumen_hora,
		'resumen_dia': resumen_dia,
		'resumen_semana': resumen_semana,
		'resumen_mes': resumen_mes
	}
	data = {
		"sensor": sensor, 
		'resumen': mydict
	}
	serializer = ResumenSensorSerializer(data, context={'request': request})
	return serializer

def obtener_data_sensor(sensor):
	"""
	Funcion para obtener todas las lecturas realizadas por un sensor
	en formato [[timestamp: datetime, lectura: float]]
	"""
	lecturas = Lectura.objects.filter(sensor = sensor)
	res = [[lec.medido, lec.valor] for lec in lecturas]
	return res

def obtener_data_sensor_por_rango(sensor, desde, hasta):
	"""
	Funcion para obtener las lecturas de un sensor 
	en un rango de datetimes
	"""
	lecturas = Lectura.objects.filter(sensor = sensor, medido__range=(desde, hasta))
	return lecturas

def resamplear_datos_a_dataframe(queryset, freq):
	"""
	Funcion que resamplea los datos de un queryset a un dataframe usando la frecuencia dada
	Se asume que el queryset tiene los campos 'medido' y 'valor'
	freq debe ser una frecuencia en estilo '5T', 'H', ...
	"""
	if queryset.count() == 0:
		return {'xdata': [], 'ydata': []}
	qs = queryset.values('medido', 'valor')
	print("[INFO] queryset")
	print(qs)
	df = pd.DataFrame.from_records(qs)
	#print("[INFO] dataframe")
	#print(df)
	df['datetime'] = pd.to_datetime(df['medido'])
	df = df.set_index('datetime')
	# df.drop(['medido'], axis=1, inplace=True)
	print("[INFO]: max, min")
	maxpoint = {
		'datetime': df[df['valor']==df['valor'].max()].index.tolist()[0],
		'valor': df[df['valor']==df['valor'].max()]['valor'].values.tolist()[0]
	}
	minpoint = {
		'datetime': df[df['valor']==df['valor'].min()].index.tolist()[0],
		'valor': df[df['valor']==df['valor'].min()]['valor'].values.tolist()[0]
	}
	# print(df[df['valor']==df['valor'].max()])
	print(maxpoint)
	df = df.resample(freq).mean()
	df = df.where(pd.notnull(df), None)
	print(df['valor'].values.tolist())
	return {'xdata': df.index.tolist(), 'ydata': df['valor'].values.tolist(), 'maxpoint': maxpoint, 'minpoint': minpoint}

def obtener_data_sensor_ultima_hora(sensor):
	"""
	Funcion para obtener las lecturas de la ultima hora de un sensor.
	Ordenadas en intervalos de 5 minutos. 
	"""
	hasta = datetime.now()
	intervalo = timedelta(days = 0, hours = 1, minutes = 0)
	desde = hasta - intervalo
	lecturas = obtener_data_sensor_por_rango(sensor, desde, hasta)
	return resamplear_datos_a_dataframe(lecturas, '5T')


def obtener_data_sensor_ultimo_dia(sensor):
	"""
	Funcion para obtener las lecturas del ultimo dia de un sensor
	"""
	hasta = datetime.now()
	intervalo = timedelta(days = 1, hours = 0, minutes = 0)
	desde = hasta - intervalo
	lecturas = obtener_data_sensor_por_rango(sensor, desde, hasta)
	return resamplear_datos_a_dataframe(lecturas, '30T') 

def obtener_data_sensor_ultima_semana(sensor):
	"""
	Funcion para obtener las lecturas del ultimo dia de un sensor
	"""
	hasta = datetime.now()
	intervalo = timedelta(days = 7, hours = 0, minutes = 0)
	desde = hasta - intervalo
	lecturas = obtener_data_sensor_por_rango(sensor, desde, hasta)
	return resamplear_datos_a_dataframe(lecturas, '12H') 

def obtener_data_sensor_ultimo_mes(sensor):
	"""
	Funcion para obtener las lecturas del ultimo mes de un sensor
	"""
	hasta = datetime.now()
	intervalo = timedelta(days = 30, hours = 0, minutes = 0)
	desde = hasta - intervalo
	lecturas = obtener_data_sensor_por_rango(sensor, desde, hasta) 
	return resamplear_datos_a_dataframe(lecturas, 'D')

