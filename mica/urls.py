from django.urls import path, include
from .views import index

urlpatterns = [
    path('game/', include('game.urls')),
    path('', index),
]
