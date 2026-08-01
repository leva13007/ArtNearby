from django.core.exceptions import PermissionDenied
from functools import wraps
from django.shortcuts import redirect

def company_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # Or raise PermissionDenied
        elif request.user.profile.user_type != 'company':
            return redirect('index')
        return view_func(request, *args, **kwargs)
    return _wrapped_view