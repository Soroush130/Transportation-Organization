from django.urls import path, include
from rest_framework import routers
from .views import LoginViewSet

router = routers.DefaultRouter()
router.register(r'accounts', LoginViewSet, basename='accounts')

urlpatterns = [
    path('', include(router.urls)),
]