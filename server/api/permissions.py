from rest_framework import permissions

class IsSensorOwner(permissions.BasePermission):
	# for view permission
 	#def has_permission(self, request, view):
	#	return request.user and request.user.is_authenticated

	# for object level permissions
	def has_object_permission(self, request, view, sensor_obj):
		# request.user.id
		return sensor_obj.proyecto.propietario.id == request.user.id