Developing.md

## Agregando jwt. 

$ pip install djangorestframweork-jwt

Se agrega esta linea a default_ auth de DRF
'rest_framework_jwt.authentication.JSONWebTokenAuthentication',

Se agrega lo siguiente a setting
JWT_AUTH = {
    'JWT_ALLOW_REFRESH': True,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=3600),
}

Lo siguiente a urls
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
path(r'api-token-auth/', obtain_jwt_token),
path(r'api-token-refresh/', refresh_jwt_token),




#######################
## STREAMING VS LOGGING
#######################

Stream es simplemente una canal de mediciones
Logging es especificamente una propiedad del servidor en relacion al que hacer con los datos: ¿Los guardo o solo los muestro en tiempo real?

Se implementará una funcionalidad que hace que especificamente se almacene en DB si se desea guardar los datos del sensor, y cada cuanto. 
Se implementará a nivel de modelo del sensor. Además se guardará en el mismo modelo el ultimo valor guardado, ultimo valor recibido, y timestamps de ambos valores


############
# TIMESTAMPS 
############

Seconds since epoch vs DateTime ???
hay 50-50 de preferencias. 
Cada uno tiene sus cosas buenas y sus cosas malas. 

Como ya se tiene implementado mucha funcionalidad con DateTimes, se mantiene. 
OJO! Algo de mucha utilidad!
datetime.datetime(2012,4,1,0,0).timestamp() unix timestamps



#########
# ALERTAS
#########

NOTIFICACION/ALERTA/UMBRAL

Un umbral es un sistema básico de monitoreo en el cual se comparan dos valores y en base a una lógica se ejecutan distintas acciones. 

Por ej:
  valor1: ultimo valor medido por sensor A
  valor2: ultimo valor medido por sensor B

Regla (o condicion logica:
	valor1 > valor2 entonces accion

La gracia es que los valores pueden ser configurados a gusto! (Esto es casi como crear un cellsheet... cuidado!)
	
Un valor puede ser calculado
Un valor puede ser definido como algo absoluto

Un umbral tiene nombre... 

Las acciones que se generan en base a un umbral (o regla) es generar una notificación. 

Esto se llama monitoreo? 




