# from rest_framework import permissions

# class IsOwnerOrReadOnly(permissions.BasePermission):
#     """
#     객체의 소유자만 수정할 수 있도록 하는 권한
#     """
#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return obj == request.user

from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # GET 요청은 허용
        if request.method in ['GET']:
            return True
        # PUT, DELETE는 본인만 허용
        return obj.id == request.user.id