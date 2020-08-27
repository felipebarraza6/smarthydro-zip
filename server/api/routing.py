# chat/routing.py
from django.urls import path

from . import consumers

websocket_urlpatterns = [
    #url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
    path('ws/chat/<str:uuid>', consumers.ChatConsumer )
]

# path('lecturas/<int:pk>/', views.LecturaDetail.as_view(), name="lectura-detail"),