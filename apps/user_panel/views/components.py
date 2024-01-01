from django.http import HttpRequest
from django.shortcuts import render
from apps.admin_panel.models import User


# region user side bar


def user_side_bar_component(request: HttpRequest):
    user: User = User.objects.get_user_for_side_bar(request.user.id)
    return render(request, 'user_panel/components/user_side_bar.html', {
        'user': user
    })

# endregion
