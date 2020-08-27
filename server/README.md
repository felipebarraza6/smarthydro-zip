# OVERVIEW

Proyecto base para la implementación de un servidor IoT. Se crea en Django y Django Rest Framework para tener un kickstart real. 
Cuenta con un método de autenticación básico a nivel de dispositivo, un esquema de base de datos también básico y un procotolo de comunicación mediante HTTP. 

Si bien DRF viene con un sistema de vistas habilitadas para Browser, la idea de este backend es que sea utilizado como un API consumible por otro cliente, permitiendo desarrollos de frontend en cualquier otro framework. Particularmente, este proyecto viene con un cliente hermano, IoT-client, el cual está construido en Angular. 

## Características incluidas

+ Websockets (Django Channels)
+ Serializers
+ Esquema BD básico
+ Autenticación de API usando django standard. 
+ Autenticación de dispositivos usando API-KEY
+ Rest Framework (Django Rest Framework)
+ Corsheaders (Django Corsheaders)


# INSTALACIÓN

El único requisito necesario de configurar a mano previo al uso del proyecto, incluso en entorno de desarrollo, es Redis.  

$ TODO: AGREGAR INSTRUCCIONES PARA REDIS

```
$ git clone
$ cd iot-server
$ mkvirtualenv iot-server
$ pip install -r requirements.txt
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver
```
En este punto ya se puede acceder a las vistas de browser de DRF. Ir al navegador y probar http://localhost:8000/sensors/. 
Śi todo funciona correctamente, debería exigir credenciales. Las del usuario admin deberían bastar.

## Usando un device-simulator


# INSTALACIÓN EN ENTORNO PRODUCTIVO

## Integrando motor de base de datos

## Integrando con gunicorn

## Integrando con Nginx

### staticfiles



# TODO

+ Autenticación de API-USER utilizando API-KEY o TOKENS
+ Autenticación de DRF-Browser usando Django ble
+ Configuracion en producción con algun tipo de seguridad


