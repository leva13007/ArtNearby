from django.core.exceptions import PermissionDenied

class UserIsOverMixin(object):
    def dispatch(self, request, *args, **kwargs):
        instance = self.get.object()
        if instance.creator != self.request.user:
            raise PermissionDenied
        return super().dispatch(*args, **kwargs)