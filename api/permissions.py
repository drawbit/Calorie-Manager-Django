from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
  def has_permission(self, request, view):
    return request.user.role == 'admin'

class IsManager(permissions.BasePermission):
  def has_permission(self, request, view):
    return request.user.role == 'manager'

class IsUser(permissions.BasePermission):
  def has_permission(self, request, view):
    return request.user.role == 'user'

class IsAdminOrManager(permissions.BasePermission):
  def has_permission(self, request, view):
    return request.user.role == 'admin' or request.user.role == 'manager'

  def has_object_permission(self, request, view, obj):
    return request.method == 'GET' or request.user.id != obj.id

class IsAdminOrUser(permissions.BasePermission):
  def has_permission(self, request, view):
    return request.user.role == 'admin' or request.user.role == 'user'

  def has_object_permission(self, request, view, obj):
    return request.user.role == 'admin' or request.user == obj.user
