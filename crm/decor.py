from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

'''
def allowed_users(allowed_roles=[]):
    def wrapper(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('you are not authorized to visit this page')

        return wrapper_func

    return wrapper'''


def custom_permission_required(perm):
    def wrapper(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.has_perm(perm):
                return view_func(request, *args, **kwargs)
            else:
                return render(request, '403.html')

        return wrapper_func

    return wrapper



