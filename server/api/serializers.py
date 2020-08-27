from rest_framework import serializers
from .models import Sensor, TEMP_CHOICES, Proyecto, Lectura
from django.contrib.auth.models import User, Group

class UserSerializer(serializers.ModelSerializer):
	proyectos = serializers.HyperlinkedRelatedField(many=True, queryset=Proyecto.objects.all(), view_name='proyecto-detail')

	class Meta:
		model = User
		fields = ('id', 'username', 'proyectos', 'url')

class GroupSerializer(serializers.ModelSerializer):
	proyectos = serializers.HyperlinkedRelatedField(many=True, queryset=Proyecto.objects.all(), view_name='proyecto-detail')

	class Meta:
		model = Group
		fields = ('id', 'name', 'proyectos', 'url')

from rest_framework.reverse import reverse
class ProyectoSerializer(serializers.ModelSerializer):
	propietario = UserSerializer(read_only=True)
	grupo = GroupSerializer(read_only=True)
	
	# sensors = serializers.SerializerMethodField()# many=True

	# sensor = serializers.HyperlinkedRelatedField(many=True, queryset=Sensor.objects.all(), view_name='sensor-detail')
	def get_sensors(self, obj):
		request = self.context.get('request')
		aux = {'sensor-url': request.build_absolute_uri(reverse('sensor-detail',  kwargs={'pk': obj.id}))}
		return aux
		
		# eturn 
	class Meta:
		model = Proyecto
		fields = ('id', 'nombre', 'propietario', 'grupo', 'url')

class SensorSerializer(serializers.HyperlinkedModelSerializer):
	proyecto = ProyectoSerializer(read_only=True)
	variable = serializers.ReadOnlyField(source='variable.nombre')
	unidad = serializers.ReadOnlyField(source='unidad.nombre')
	uuid = serializers.ReadOnlyField()
	# proyecto = serializers.HyperlinkedIdentityField(view_name='proyecto-detail')
	# variable_nombre = serializers.ReadOnlyField(source="variable", read_only=True)

	class Meta:
		model = Sensor
		fields = ('url','creado', 'nombre', 'descripcion', 'uuid', 'variable', 'unidad', 'proyecto', 'logging', 'last_received_value', 'last_received_ts')

class LecturaSerializer(serializers.ModelSerializer):
	sensor = serializers.HyperlinkedRelatedField(view_name='sensor-detail', read_only=True)
	# valor = serializers.ReadOnlyField()
	# recibido = serializers.ReadOnlyField()
	# medido = serializers.ReadOnlyField()
	
	
	class Meta:
		model = Lectura
		fields = ('id', 'sensor', 'recibido', 'medido', 'valor')

from .models import Alerta
class AlertaSerializer(serializers.ModelSerializer):
	sensor = SensorSerializer()
	lectura = LecturaSerializer()
	verificando = serializers.ReadOnlyField()
	descripcion = serializers.ReadOnlyField()
	timestamp = serializers.ReadOnlyField()
	umbral = serializers.ReadOnlyField()

	class Meta:
		model = Alerta
		fields = ('sensor', 'lectura', 'verificando', 'descripcion', 'timestamp', 'umbral')

#########################
## SERIALIZERS ESPECIALES
#########################
class ResumenSensorSerializer(serializers.Serializer):
   sensor = SensorSerializer()
   resumen = serializers.DictField()

class ResumenUsuarioSerializer(serializers.Serializer):
	user = UserSerializer()
	proyecto = ProyectoSerializer(many=True)
	sensor = SensorSerializer(many = True)