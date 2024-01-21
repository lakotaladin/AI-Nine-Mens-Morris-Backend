from django.urls import path, include
from  mica.views import index
# from django.conf.urls.static import static
# from django.conf import settings

urlpatterns = [
    path('game/', include('game.urls')),
    path("index",index)
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)