from django.urls import path, include
from rest_framework import routers
from .views import ProductViewSet, BarViewSet

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'bars', BarViewSet, basename='bars')

urlpatterns = [
    path('', include(router.urls)),
]