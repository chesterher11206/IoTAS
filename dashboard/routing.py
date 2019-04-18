from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/display/<str:room_name>/', consumers.DisplayConsumer),
    # path('ws/search/<str:room_name>/', consumers.SearchConsumer)
]