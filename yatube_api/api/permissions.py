"""
Provides a set of pluggable permission policies.
"""
from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    """
    Allows access only to author.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Allows list to all, change only to author.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsFollower(permissions.BasePermission):
    """
    Allows access only to follower.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
