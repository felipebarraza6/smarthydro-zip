class Sensor:

	def __init__(self, transformRule = "x"):
		# Un sensor en su nivel más bajo solo sabe como transformar un input de lectura. 
		# Esto sirve para poder implementar transformaciones en caso de utilizas sensores análogicos
		# como por ejemplo, pasar desde Voltaje a Tensión. 
		# También puede ser usado para realizar transformaciónes pseudo-geometricas como pasar desde un
		# sensor de profundidad a una medición de Caudal (como sería en el caso de un canal hídrico)
		self.transformRule = transformRule

	def transform(self, x):
		# NOTA: Funcion que en teoría puede exponer vulnerabilidades si se ocupa erroneamente. 
		# No obstante, se asume que el usuario corresponde a un administrador responsable, que no incluirá 
		# evaluaciones peligrosas en 'eval'
		# Se decide implementar de esta forma para permitir generalización de la fórmula de transformación.
		# NOTA2: Sólo se permite evaluar funciones polinómicas explícitas!
		x = float(x)
		res = eval(self.transformRule,{"__builtins__":None},{"x":x})
		return res

	def get_reading(self):
		# Una subclase de sensor debería implementar esta función. 
		# De alguna forma, deben saber como obtener una lectura y un timestamp
		reading = None
		timestamp = None 
		return reading, timestamp