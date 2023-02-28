from rest_framework import permissions


class IsFactory(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == 'factory'
        )


class IsOwnerProduct(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and
            request.user.role == 'factory'
        )

    def has_object_permission(self, request, view, obj):
        return obj.factory_company == request.user


class IsFreight(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == 'freight'
        )


class IsDriver(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == 'driver'
        )
