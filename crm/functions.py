import json

from accounts.models import Log


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def logs(action, old_data, request, model_name):

    if action == 'add':
        Log.objects.create(user=request.user, url=request.get_full_path(),
                           new_data=json.dumps(request.POST),
                           ip_address=get_client_ip(request), model_name=model_name, action='add')
    elif action == 'edit':
        Log.objects.create(user=request.user, url=request.get_full_path(),
                           new_data=json.dumps(request.POST),
                           old_data=old_data.__dict__,
                           ip_address=get_client_ip(request), model_name=model_name,
                           action='edit')
    elif action == 'delete':
        Log.objects.create(user=request.user, url=request.get_full_path(),
                           old_data=old_data.__dict__,
                           ip_address=get_client_ip(request), model_name=model_name,
                           action='delete')
