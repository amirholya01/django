from django.shortcuts import redirect
from django.urls import reverse


def redirect_if_logged_in():
    def decorator(function):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(reverse('user_dashboard_page'))
            return function(request, *args, **kwargs)

        return wrapper

    return decorator
