from django.core.exceptions import PermissionDenied

class UserIsOverMixin:
    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.creator != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)