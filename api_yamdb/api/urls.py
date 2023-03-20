from django.urls import include, path

from .v1 import urls as v1_urls

urlpatterns = [
    path('api/v1/', include(v1_urls)),
]
