from rest_framework import permissions


class VerifiedPermission(permissions.BasePermission):

    """
    Permission based on an Admin verifying a registration.

    On verifiyng User will be able to view score portal contents after sign-in.
    """

    def has_permission(self, request, view):
        verified = request.user.is_verified
        return verified