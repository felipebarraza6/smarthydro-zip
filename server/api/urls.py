from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
	path('', views.api_root),
  path('sensors/', views.SensorList.as_view(), name="sensor-list"),
  path('sensors/<int:pk>/', views.SensorDetail.as_view(), name="sensor-detail"),
  path('users/', views.UserList.as_view(), name="user-list"),
	path('users/<int:pk>/', views.UserDetail.as_view(), name="user-detail"),
	path('groups/', views.GroupList.as_view(), name="group-list"),
	path('groups/<int:pk>/', views.GroupDetail.as_view(), name="group-detail"),
	path('proyectos/', views.ProyectoList.as_view(), name="proyecto-list"),
	path('proyectos/<int:pk>/', views.ProyectoDetail.as_view(), name="proyecto-detail"),
	path('lecturas/', views.LecturaList.as_view(), name="lectura-list"),
	path('lecturas/<int:pk>/', views.LecturaDetail.as_view(), name="lectura-detail"),
	path('resumen-sensor/<str:uuid>/', views.ResumenSensorDetail.as_view(), name="resumen-sensor"),
	path('download-sensor/<str:uuid>/', views.downloadSensor, name="download-sensor"),
	path('resumen-usuario/', views.ResumenUsuario.as_view(), name="resumen-usuario"),
	path('alertas/', views.AlertaList.as_view(), name="alerta-list")

]

urlpatterns = format_suffix_patterns(urlpatterns)