from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action, permission_classes
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class DriverViewSet(ViewSet):
    pass
