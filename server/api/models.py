from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.
TEMP_CHOICES = [('C', '° Celcis'), ('F', '° Farenheit'), ('K', 'Kelvin')]

class Variable(models.Model):
	"""
	Modelo para variables fisicas como Temperatura,... 
	Cosas medibles a distintas unidades. 
	"""
	creado = models.DateTimeField(auto_now_add=True)
	nombre = models.CharField(max_length=100, unique=True)
	descripcion = models.TextField()

	def __str__(self):
		return self.nombre

	class Meta:
		ordering = ('creado',)
	
	

class Unidad(models.Model):
		"""
		Unidad de medicion de variable
		"""
		abreviacion = models.CharField(max_length=100, unique=True)
		nombre = models.CharField(max_length=100, unique=True)
		
		def __str__(self):
			return self.nombre

		class Meta:
				ordering = ('nombre',)


class Proyecto(models.Model):
		"""
		Tiene usuario owner, tiene grupo, tiene sensores pero estos se asocian en su definicion
		"""
		propietario = models.ForeignKey(User, related_name='proyectos', on_delete=models.SET_NULL, null=True)
		grupo = models.ForeignKey(Group, related_name='proyectos', on_delete=models.SET_NULL, null=True)
		nombre = models.CharField(max_length=200, unique = True)

		def __str__(self):
			return self.nombre + self.propietario.username

		class Meta:
				ordering = ('nombre',)

class Sensor(models.Model):
	"""
	Modelo de sensor.
	logging: Indica si se estan almacenando los valores recibidos
	log_interval: Indica cada cuanto hay que almacenar los valores recibidos. Simplemente calcula el delta de tiempo entre el ultimo recibido y el actual y verifica que sea mayor a log_interval.
		A nivel de BD log_interval puede tener cualquier valor, pero en la práctica se verifica que sea mayor a 1 segundo, valor que más adelante debería ser una carácteristica del plan del usuario!

	"""	
	creado = models.DateTimeField(auto_now_add=True)
	nombre = models.CharField(max_length=100, blank=True, default='')
	descripcion = models.TextField()
	uuid = models.CharField(max_length=40, blank=True, null=True, unique=True)
	unidad = models.ForeignKey(Unidad, related_name="sensores", on_delete=models.SET_NULL, null=True)
	variable = models.ForeignKey(Variable, related_name="sensores", on_delete=models.SET_NULL, null=True)
	fabricante = models.CharField(max_length=200, blank=True)
	link = models.CharField(max_length=200, blank=True)
	proyecto = models.ForeignKey(Proyecto, related_name="sensores", on_delete=models.SET_NULL, null=True)
	estado = models.BooleanField(default = True)
	logging = models.BooleanField(default = True)
	log_interval = models.FloatField(default = 10)
	last_received_ts = models.DateTimeField(blank = True, null = True)
	last_received_value = models.FloatField(blank = True, null = True)
	last_logged_ts = models.DateTimeField(blank = True, null = True)
	last_logged_value = models.FloatField(blank = True, null = True)

	def __str__(self):
		return "{} - {} - {} - {}".format(self.proyecto.nombre, self.nombre, self.variable.abreviacion, self.uuid[:8])
 
	class Meta:
		ordering = ('creado',)

class Lectura(models.Model):
		"""
		Lectura de un sensor
		"""
		sensor = models.ForeignKey(Sensor,related_name="lecturas", on_delete=models.SET_NULL, null=True)
		recibido = models.DateTimeField(auto_now_add=True)
		medido = models.DateTimeField(blank=True)
		valor = models.FloatField(default = -1270.0)

		def __str__(self):
			return "{} - {} ".format(self.sensor, self.valor)

		class Meta:
				ordering = ('recibido',)

from polymorphic.models import PolymorphicModel
class Regla(PolymorphicModel):
	# Una regla determina las verificaciones que hay que realizar al momento de recibir una nueva lectura.
	# La verificación matemática de una regla es sencilla y tiene la siguiente forma:
	#   VERIFICANDO ? UMBRAL -> boolean
	# El valor verificando es el promedio de las lecturas previas que caen dentro de los minutos indicados por data_range. 
	# 	NOTA: Si no existen lecturas dentro de los minutos en data_range, las verificaciones daran por defecto True!
	#   NOTA: Si data_range == 0, se considera una verificación instantánea, es decir, solo se considera el valor de la última lectura. 
	# El valor umbral se configura por el usuario. 
	# La operación ? puede ser las típicas matemáticas de comparación (==, +>,...) pero es un método abstracto, que debe ser definido en las subclases. 
	# 	NOTA: Todas las subclases deben implementar el método verificar(Lectura lectura)
	# MENSAJERIAS
	# La regla puede propagarse usando mensajeros. 

	sensor = models.ForeignKey(Sensor, related_name='reglas', on_delete=models.CASCADE, null=True)
	dataRange = models.IntegerField(default = 0)
	descripcion = models.TextField()
	umbral = models.FloatField(default = 0.0)

	def obtenerLecturasPrevias(self, lectura):
		# Funcion que permite calcular el valor a verificar.
		return None

	def obtenerValorAVerificar(self, lectura):
		# Si dataRange == 0, se devuelve el valor de la última lectura
		if self.dataRange == 0:
			return lectura.valor

		lecturasPrevias = self.obtenerLecturasPrevias(lectura)
		# calcular el promedio
		valor = None
		return valor

	def __str__(self):
		return self.descripcion + ' - ' + self.sensor.nombre

#	class Meta:
#		abstract = True


class Mensajero(PolymorphicModel):
	# Un mensajero es un protocolo de propagación de las alertas que se generen en el sistema. 
	# Se implementa como clase abstracta para poder generalizar y que las subclases determinen la forma de efectuar sus mensajes. 
	# 	NOTA: todas las subclases deben implementar el método enviarMensaje()
	descripcion = models.TextField()
	regla = models.ForeignKey(Regla, related_name='mensajeros', on_delete=models.CASCADE)
	premensaje = models.TextField()

	def __str__(self):
		return self.descripcion + ' - ' + self.regla.sensor.nombre
#	class Meta:
#		abstract = True


class MayorOIgualRegla(Regla):
	# Una regla de mayor o igual, verifica que el valor calculado en base a data_range sea mayor o igual al umbral. 

	def verificar(self, lectura):
		# obtener el valor a verificar
		verificando = self.obtenerValorAVerificar(lectura)

		# realizar la operación matemática
		resultado = verificando >= self.umbral
		return resultado, verificando

	def __str__(self):
		return "alertar {} mayor que {}".format(self.sensor.nombre, self.umbral)

class MenorOIgualRegla(Regla):
	# Una regla de menor o igual, verifica que el valor calculado en base a data_range sea memor o igual al umbral. 

	def verificar(self, lectura):
		# obtener el valor a verificar
		verificando = self.obtenerValorAVerificar(lectura)

		# realizar la operación matemática
		resultado = verificando <= self.umbral
		return resultado, verificando

	def __str__(self):
		return "Alertar {} menor que {}".format(self.sensor.nombre, self.umbral)

class ConsolaMensajero(Mensajero):
	# Un mensajero consola simplemente imprime en la consola de la aplicación el resultado de la verificación. 
	# El mensaje se especifica al momento de crear el mensajero. 
	

	def crearMensaje(self, verificando):
		# Funcion que crea el mensaje para ser enviado al usuario
		mensaje = "{} - Verificando: {}, umbral: {}".format(self.premensaje, verificando, self.regla.umbral)
		return mensaje 

	def enviarMensaje(self, mensaje, clientes):
		# @param clientes:diccionario conteniendo la información de clientes de mensajería.
		print("[INFO] Mensajero: {}".format(mensaje))
		return "Mensaje envíado a consola"


class SmsMensajero(Mensajero):
	# Un mensajero sms envía una alerta al número específicado
	# OJO! No se agrega una validación al número!
	# La configuración del cliente twilio se carga previamente. 
	destinatario = models.TextField()

	def enviarMensaje(self, mensaje, clientes):
		# Funcion para realizar el envío del mensaje SMS
		# @param clientes:dict es un diccionario conteniendo la información de los posibles clientes a usar 
		#    clientes: { 'clientSms': <Twilio-SMS-Client>, 'fromSMS': NUM_CONF, ...}
		# @param mensaje:string es el mensaje que se desea enviar por sms
		clienteTwilio = clientes['clienteSms']
		numFrom = clientes['fromSMS']
		message = clienteTwilio.messages.create(body = mensaje, from_ = numFrom, to = self.destinatario)
		return message.sid

	def crearMensaje(self, verificando):
		# Funcion que crea el mensaje para ser enviado al usuario. 
		# Como se trata de un SMS es necesario ser conciso. 
		# Solo se incluye el mensaje de configuración y el valor verificando. 
		mensaje = "{}. {}".format(self.premensaje, verificando)
		return mensaje


from sendgrid.helpers.mail import Mail
class EmailMensajero(Mensajero):
	# Un mensajero email envía la alerta al email especificado a traves de sendgrid
	destinatario = models.TextField()

	def crearMensaje(self, verificando):
		mensaje = "<strong> Se ha generado una alerta en un sensor. {}. Valor registrado: {}</strong>".format(self.premensaje, verificando)
		return mensaje

	def enviarMensaje(self, mensaje, clientes):
		# Funcion para realizar el envío de un email
		# @param mensaje:string es el mensaje que se desea envíar por email
		# @param clientes:dict es un diccionario conteniendo la información de los posibles clientes a usar
		#    clientes: {'clientEmail': SENDGRID_CLIENT, 'fromEmail': SENDGRID_FROM}
		fromEmail = clientes['fromEmail']
		clienteEmail = clientes['clienteEmail']
		subject = "ALERTA en medición de sensor"
		message = Mail(from_email = fromEmail, to_emails = self.destinatario, subject = subject, html_content = mensaje)
		response = clienteEmail.send(message)
		return response


class Alerta(models.Model):
	# Una alerta se genera cuando se activa una regla.
	# Sin embargo se referencian los sensores y los parámetros de la regla en vez de la regla en sí al momento de crear la instancia
	sensor = models.ForeignKey(Sensor, related_name='alertas', on_delete=models.CASCADE, null=True)
	descripcion = models.TextField()
	verificando = models.FloatField()
	umbral = models.FloatField( default = 0.0)
	lectura = models.ForeignKey(Lectura, related_name='lecturas', on_delete = models.SET_NULL, null = True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		if self.sensor is None:
			nombre = "None"
		else:
			nombre = str(self.sensor.nombre)
		return  nombre + ' - ' + str(self.timestamp)




