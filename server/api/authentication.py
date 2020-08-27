from .models import Sensor
from rest_framework import authentication 
from django.contrib.auth.models import AnonymousUser 
from rest_framework.exceptions import AuthenticationFailed 

class SensorUser(AnonymousUser):

    def __init__(self, sensor):
        self.sensor = sensor 

    @property 
    def is_authenticated(self):
        return True 


class SensorAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        # print("Intentando autenticar con HTTP_X_UUID")
        uuid = request.META.get("HTTP_UUID", None)
        # print("[INFO] META: {}".format(request.META))
        print("[INFO] uuid: {}".format(str(uuid)))
        if not uuid:
            raise AuthenticationFailed("Invalid UUID")

        try:
            sensor = Sensor.objects.get(uuid=uuid)
        except Sensor.DoesNotExist:
            raise AuthenticationFailed("Invalid UUID")

        if not sensor.estado:
            raise AuthenticationFailed("Device is inactive or deleted")

        request.sensor = sensor
        return (SensorUser(sensor), None)