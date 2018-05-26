from rest_framework import permissions


class IsAccountOfPlayer(permissions.BasePermission):
    def has_object_permission(self, request, view, player):
        if request.user:
            return player.account == request.user
        return False