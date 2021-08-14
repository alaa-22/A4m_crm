import os
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import default_storage
from django.core.paginator import Paginator

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .filters import UserFilter, LogFilter
from .form import UserCreateform, Profileform, UserGroupForm, Userform
from .models import Profile, SiteSettings, Log
from django.contrib.auth.models import User, Permission, Group
from django.contrib.auth.decorators import login_required
from tasks.models import ActivityModel
from crm.decor import custom_permission_required
from crm.functions import logs


# Create your views here.
def test(request):
    return render(request, "pages/landing.html")


def login1(request):
    if request.user.is_authenticated:
        return redirect('company:dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password1')
            var = authenticate(request, username=username, password=password)
            if var is not None:
                if var.is_active:
                    login(request, var)
                    return redirect('company:dashboard')
                else:
                    messages.error(request, "user is inactive")
    return render(request, "account/login.html")


@login_required
@custom_permission_required("auth.view_user")
def list_users(request):
    user = User.objects.all()
    myfilter = UserFilter(request.GET, queryset=user)
    user = myfilter.qs
    paginator = Paginator(user, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'users': page_obj, 'myfilter': myfilter}
    if request.GET.get('type') == "view":
        return render(request, "pages/list_user.html", context)
    else:
        return render(request, "pages/list_user.html", context)


@login_required
@custom_permission_required("auth.add_user")
def add_user(request):
    if request.method == 'POST':
        userform = UserCreateform(request.POST)
        if userform.is_valid():
            u = userform.save(commit=False)
            u.is_staff = 1
            u.save()
            logs('add', None, request, User)
            messages.success(request, "user added Successfully")
            return redirect('account:list_user')
        else:
            print(userform.errors)
            messages.error(request, userform.errors)
    else:
        userform = UserCreateform()
    context = {'userform': userform}
    return render(request, "pages/add_user.html", context)


@login_required
@custom_permission_required("auth.change_user")
def edit_user(request, pk):
    user = User.objects.get(id=pk)
    userform = Userform(instance=user)
    if request.method == 'POST':
        userform = Userform(request.POST, instance=user)
        if userform.is_valid():
            userform.save()
            logs('edit', user, request, User)
            messages.success(request, "Updated Successfully")
            # return redirect('account:list_user')
        if request.POST['password'] and request.POST['confirm_password']:
            if request.POST['password'] != request.POST['confirm_password']:
                messages.error(request, "Please Confirm Password")
                # Return With Error confirmation
            else:
                user.set_password(request.POST.get('password'))
                user.save()
                messages.success(request, "Password Updated")

    context = {'userform': userform}
    return render(request, "pages/edit_user.html", context)


@login_required
@custom_permission_required("auth.add_group")
def add_group(request):
    perm = Permission.objects.all()
    #    return HttpResponse(request.POST.getlist("permissions[]"))
    if request.method == 'POST':
        print(request)
        groupform = UserGroupForm(request.POST)
        if groupform.is_valid():
            groupform.save()
            group = Group.objects.get(name=groupform.cleaned_data.get("name"))
            print(group)
            group.permissions.set(request.POST.getlist("permissions[]"))
            logs('add', None, request, Group)
            messages.success(request, "group added Successfully")
            return redirect('account:list_group')
    else:
        groupform = UserGroupForm()
    context = {'groupform': groupform, 'perms': perm}
    return render(request, "pages/add_groups.html", context)


@login_required
@custom_permission_required("auth.add_permission")
def add_user_perm(request):
    perm = Permission.objects.all()
    users = User.objects.all()
    if request.method == 'POST':
        perms = request.POST.getlist("permissions[]")
        userid = request.POST.get("user")
        user = User.objects.get(id=userid)
        user.user_permissions.set(perms)
        logs('add', None, request, User)
        messages.success(request, "permission added Successfully")
        return redirect('account:list_user_perms')

    context = {'users': users, 'perms': perm}
    return render(request, "pages/add_user_perms.html", context)


@login_required
@custom_permission_required("auth.view_permission")
def list_user_perms(request):
    user = User.objects.all()
    context = {'users': user}
    return render(request, "pages/list_user_perms.html", context)


@login_required
@custom_permission_required("auth.change_permission")
def edit_user_perms(request, pk):
    perm = Permission.objects.all()
    user = User.objects.get(id=pk)
    user_perms = user.user_permissions.all().values_list('id', flat=True)
    if request.method == "POST":
        user.user_permissions.set(request.POST.getlist("permissions[]"))
        logs('edit', user_perms, request, User)
        messages.success(request, "Updated Successfully")
        return redirect('account:list_user_perms')
    context = {"perms": perm, "user_perms": user_perms, "user": user}
    return render(request, "pages/edit_user_perms.html", context)


@login_required
@custom_permission_required("auth.view_group")
def list_groups(request):
    group = Group.objects.all()
    context = {'groups': group}
    return render(request, "pages/list_group.html", context)


@login_required
@custom_permission_required("auth.change_group")
def edit_group(request, pk):
    perm = Permission.objects.all()
    group = Group.objects.get(id=pk)
    group_perms = group.permissions.all().values_list('id', flat=True)
    form = UserGroupForm(instance=group)
    if request.method == "POST":
        mform = UserGroupForm(request.POST, instance=group)
        if mform.is_valid():
            mform.save()
            group.permissions.set(request.POST.getlist("permissions[]"))
            logs('edit', group, request, Group)
            messages.success(request, "Updated Successfully")

            return redirect('account:list_group')

    context = {"form": form, "perms": perm, "group_perms": group_perms}
    return render(request, "pages/edit_group.html", context)


@login_required
@custom_permission_required("auth.delete_group")
def delete_group(request, pk):
    group = Group.objects.get(id=pk)
    group.delete()
    logs('delete', group, request, Group)
    return redirect(reverse('account:list_group'))


@login_required
def edit_profile(request, pk):
    profile = Profile.objects.get(user_id=pk)
    form = Profileform(instance=profile)
    if request.method == "POST":
        form = Profileform(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            logs('edit', profile, request, Profile)
            messages.success(request, "Updated Successfully")
        else:
            print(form.errors)
            messages.error(request, form.errors)
    context = {'form': form}
    return render(request, "pages/profile.html", context)


'''def update_avatar(request):
    data = {}
    if (request.is_ajax()):
        Profile.objects.filter(user=request.user).update(avatar=request.POST.get('avatar'))
        data['state'] = True
        data['msg'] = "Success Man"

        return JsonResponse(data)'''


@login_required
@custom_permission_required("auth.delete_user")
def delete_user(request, pk):
    user = User.objects.get(id=pk)
    user.delete()
    logs('delete', user, request, User)

    return redirect(reverse('account:list_user'))


# admin only
@login_required
@custom_permission_required("tasks.view_activitymodel")
def user_activity(request, name):
    activity = ActivityModel.objects.filter(made_by=name)
    paginator = Paginator(activity, 6)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'activities': page_obj}
    return render(request, "pages/user_activity.html", context)


'''@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        print("before")
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            print("*****************************************")
            return redirect('account:account_login')
        else:
            print(form.errors)
            print("dddddddddddddddddddddddddddddddd")

    else:
        form = PasswordChangeForm(request.user)

    context = {'form': form}
    return render(request, "account/password_change.html", context)

'''


def site_setting(request):
    setting = SiteSettings.objects.all()
    if request.method == "POST":
        for key in request.POST:
            if key == 'csrfmiddlewaretoken':
                pass
            else:
                setting = SiteSettings.objects.get(key=key)
                setting.value = request.POST.get(key)
                setting.save()

    context = {"settings": setting}
    return render(request, "pages/site_setting.html", context)


def file_upload(file):
    save_path = os.path.join(settings.MEDIA_ROOT, 'uploads', file)
    path = default_storage.save(save_path, file)
    return default_storage.path(path)


def system_logs(request):
    log = Log.objects.all()
    myfilter = LogFilter(request.GET, queryset=log)
    log = myfilter.qs
    paginator = Paginator(log, 6)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'logs': page_obj, 'myfilter': myfilter}
    return render(request, "pages/logs.html", context)


def system_log_details(request, pk):
    log = Log.objects.get(id=pk)
    context = {'log': log}
    return render(request, "pages/log_detail.html", context)


def logout_fun(request):
    logout(request)
    return redirect('account_login')
