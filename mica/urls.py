from django.urls import path, include
from  mica.views import index
urlpatterns = [
    path('game/', include('game.urls')),
    path("index",index)
]
