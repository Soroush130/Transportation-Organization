from django.urls import path, include
from rest_framework import routers
from .views import DriverViewSet

router = routers.DefaultRouter()
router.register(r'drivers', DriverViewSet, basename='drivers')

urlpatterns = [
    path('', include(router.urls)),
]