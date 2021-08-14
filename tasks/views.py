import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import TaskModel, SendEmailModel, WhatsappModel, MeetingModel, CallModel, ActivityModel, NoteModel
from .form import Taskform, Emailform, Callform, Whatsappform, Meetingform, Noteform
from company.models import CompanyModel
from contact.models import ContactModel
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.conf import settings
from .filters import WhatsappFilter, TaskFilter, MailFilter, Activity_ReportFilter
from crm.decor import custom_permission_required
from crm.functions import logs


# Create your views here.
@login_required
@custom_permission_required('tasks.view_taskmodel')
def tasks_list(request):
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    tasks = TaskModel.objects.filter(Assign_to=request.user, date__range=(today_min, today_max))
    if request.user.groups.filter(name="admins").exists():
        tasks = TaskModel.objects.all()
    myfilter = TaskFilter(request.GET, queryset=tasks)
    tasks = myfilter.qs
    paginator = Paginator(tasks, 10)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'tasks': page_obj, "myfilter": myfilter}
    return render(request, "pages/list/tasklist.html", context)


@login_required
@custom_permission_required('tasks.change_taskmodel')
def view_task(request, pk):
    task = TaskModel.objects.get(id=pk)
    form = Taskform(instance=task)
    if request.method == "POST":
        TaskModel.objects.filter(pk=pk).update(statue=request.POST.get('statue'))
        return redirect('tasks:Task list')
    context = {"taskform": form}
    return render(request, "pages/edit_task.html", context)


# allowed admins
@login_required
@custom_permission_required('tasks.add_taskmodel')
def add_task(request):
    company = CompanyModel.objects.all()
    if request.method == 'POST':
        task = Taskform(request.POST)
        if task.is_valid():
            t = task.save(commit=False)
            t.made_by = request.user
            t.statue = 'pending'
            t.save()
            logs('add', None, request, TaskModel)
            messages.success(request, "task added Successfully")
            return redirect('tasks:Task list')
        else:
            print(task.errors)
            messages.error(request, "error")
    else:
        task = Taskform()
    context = {'taskform': task}
    return render(request, "pages/add/add_task.html", context)


@login_required
@custom_permission_required('tasks.delete_taskmodel')
def delete_task(request, pk):
    task = TaskModel.objects.get(id=pk)
    task.delete()
    logs('delete', task, request, TaskModel)
    return redirect(reverse('tasks:Task list'))


@login_required
def add_reminder(request):
    if request.method == 'POST':
        task = Taskform(request.POST)
        if task.is_valid():
            t = task.save(commit=False)
            t.made_by = request.user
            t.task_type = 'Reminder'
            t.save()
            logs('add', None, request, TaskModel)
            messages.success(request, "reminder added successfully")
            return redirect('tasks:Task list')
        else:
            print(task.errors)
            messages.error(request, "error")
    else:
        task = Taskform()
    context = {'taskform': task}
    return render(request, "pages/add/add_reminder.html", context)


@login_required
@custom_permission_required('tasks.add_sendemailmodel')
def sendmail(request):
    if request.method == 'POST':
        email = Emailform(request.POST, request.FILES)
        if email.is_valid():
            emails = email.save(commit=False)
            emails.made_by = request.user
            emails.email = emails.contact_person.email
            subject = email.cleaned_data['subject']
            message = email.cleaned_data['message']
            from_email = settings.EMAIL_HOST_USER
            email1 = emails.email
            send_mail(subject, message, from_email, [email1], fail_silently=False, )
            emails.save()
            logs('add', None, request, SendEmailModel)
            company = None
            if emails.contact_person.type == 'contact':
                company = CompanyModel.objects.get(company_name=emails.contact_person.company.company_name)

            ActivityModel.objects.create(made_by=request.user, type="Email",
                                         contact_person=emails.contact_person,
                                         details=message,
                                         company=company
                                         )
            messages.success(request, "mail sent successfully")
            return redirect("tasks:mail_list")
        else:
            print(email.errors)
    else:
        email = Emailform()
    context = {'eform': email}
    return render(request, "pages/sendmail.html", context)


@login_required
@custom_permission_required('tasks.view_sendemailmodel')
def mail_list(request):
    mail = SendEmailModel.objects.filter(made_by=request.user)
    if request.user.groups.filter(name="admins").exists():
        mail = SendEmailModel.objects.all()

    myfilter = MailFilter(request.GET, queryset=mail)
    mail = myfilter.qs

    paginator = Paginator(mail, 10)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'mails': page_obj, "myfilter": myfilter}
    return render(request, "pages/list/mail_list.html", context)


@login_required
@custom_permission_required('tasks.view_sendemailmodel')
def view_mail(request, pk):
    mail = SendEmailModel.objects.get(id=pk)
    form = Emailform(instance=mail)
    context = {'eform': form}
    return render(request, "pages/view_mail.html", context)


@login_required
@custom_permission_required('tasks.add_whatsappmodel')
def send_whatsapp(request):
    if request.method == 'POST':
        whats = Whatsappform(request.POST, request.FILES)
        if whats.is_valid():
            m = whats.save(commit=False)
            m.made_by = request.user
            m.phone = m.contact_person.mobile
            print(m.phone)
            phone = m.phone
            message = whats.cleaned_data['message']
            print(phone)
            whatsappdata(phone, message)
            m.save()
            logs('add', None, request, WhatsappModel)
            company = CompanyModel.objects.get(company_name=m.contact_person.company.company_name)

            ActivityModel.objects.create(made_by=request.user, type="Email",
                                         contact_person=m.contact_person,
                                         details=message,
                                         company=company
                                         )
        else:
            print(whats.errors)
    else:
        whats = Whatsappform(request.POST, request.FILES)
    context = {'wform': whats}
    return render(request, "pages/send_whats.html", context)


def whatsappdata(phone, message):
    import time
    import webbrowser
    import pyautogui
    phone = phone
    mes = message
    print(phone)
    webbrowser.open(f"https://web.whatsapp.com/send?phone={phone}&text={mes}&app_absent=0")
    time.sleep(9)  # wait for whatsapp web
    pyautogui.click()  # move your mouse to textbox before
    pyautogui.press("enter")
    return redirect("tasks:whats_list")


@login_required
@custom_permission_required('tasks.view_whatsappmodel')
def whats_list(request):
    whats = WhatsappModel.objects.filter(made_by=request.user)
    if request.user.groups.filter(name="admins").exists():
        whats = WhatsappModel.objects.all()
    myfilter = WhatsappFilter(request.GET, queryset=whats)
    whats = myfilter.qs

    paginator = Paginator(whats, 10)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'whats': page_obj, 'myfilter': myfilter}
    return render(request, "pages/list/whatsapp_list.html", context)


@login_required
@custom_permission_required('tasks.add_meetingmodel')
def add_meeting(request):
    if request.method == 'POST':
        meeting = Meetingform(request.POST)
        if meeting.is_valid():
            t = meeting.save(commit=False)
            t.made_by = request.user
            t.date = datetime.date.today()
            t.save()
            logs('add', None, request, MeetingModel)
            company = None
            if t.contact_person.type == 'contact':
                company = CompanyModel.objects.get(company_name=t.contact_person.company.company_name)

            ActivityModel.objects.create(made_by=request.user, type="Meeting",
                                         contact_person=t.contact_person,
                                         details=t.details,
                                         company=company
                                         )
            messages.success(request, "meeting info added successfully")

            return redirect('tasks:list_meeting')
        else:
            print(meeting.errors)
            messages.error(request, "error")
    else:
        meeting = Meetingform()
    context = {'form': meeting}
    return render(request, "pages/add/add_meeting.html", context)


@login_required
@custom_permission_required('tasks.view_meetingmodel')
def list_meeting(request):
    meeting = MeetingModel.objects.filter(made_by=request.user)
    if request.user.groups.filter(name="admins").exists():
        meeting = MeetingModel.objects.all()
    myfilter = MailFilter(request.GET, queryset=meeting)
    meeting = myfilter.qs
    paginator = Paginator(meeting, 10)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'meeting': page_obj, "myfilter": myfilter}
    return render(request, "pages/list/meeting_list.html", context)


@login_required
@custom_permission_required('tasks.view_meetingmodel')
def view_meeting(request, pk):
    meeting = MeetingModel.objects.get(id=pk)
    form = Meetingform(instance=meeting)
    context = {'mform': form}
    return render(request, "pages/view_meeting.html", context)


@login_required
@custom_permission_required('tasks.add_callmodel')
def add_call(request):
    if request.method == 'POST':
        call = Callform(request.POST)
        if call.is_valid():
            t = call.save(commit=False)
            t.date = datetime.date.today()
            t.made_by = request.user
            t.save()
            logs('add', None, request, CallModel)
            company = None
            if t.contact_person.type == 'contact':
                company = CompanyModel.objects.get(company_name=t.contact_person.company.company_name)
            ActivityModel.objects.create(made_by=request.user, type="Call",
                                         contact_person=t.contact_person,
                                         details=t.details,
                                         company=company
                                         )
            messages.success(request, "call info added successfully")

            return redirect('tasks:list_call')
        else:
            print(call.errors)
            messages.error(request, "error")
    else:
        call = Callform()
    context = {'form': call}
    return render(request, "pages/add/add_call.html", context)


@login_required
@custom_permission_required('tasks.view_callmodel')
def list_call(request):
    call = CallModel.objects.filter(made_by=request.user)
    if request.user.groups.filter(name="admins").exists():
        call = CallModel.objects.all()
    myfilter = MailFilter(request.GET, queryset=call)
    call = myfilter.qs
    paginator = Paginator(call, 10)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'call': page_obj, "myfilter": myfilter}
    return render(request, "pages/list/call_list.html", context)


@login_required
@custom_permission_required('tasks.view_callmodel')
def view_call(request, pk):
    call = CallModel.objects.get(id=pk)
    form = Callform(instance=call)
    contact = ContactModel.objects.get(id=call.contact_person_id)
    company = contact.company
    context = {'form': form, 'company': company}
    return render(request, "pages/view_call.html", context)


@login_required
@custom_permission_required('tasks.add_notemodel')
def add_note(request):
    if request.method == 'POST':
        note = Noteform(request.POST)
        if note.is_valid():
            t = note.save(commit=False)
            t.date = datetime.date.today()
            t.made_by = request.user
            t.save()
            print(t.contact_person.company)
            logs('add', None, request, NoteModel)
            company = CompanyModel.objects.get(company_name=t.contact_person.company.company_name)
            ActivityModel.objects.create(made_by=request.user, type="Note",
                                         contact_person=t.contact_person,
                                         details=t.note,
                                         company=company
                                         )
            return redirect('tasks:list_call')
        else:
            print(note.errors)
    else:
        note = Noteform()
    context = {'form': note}
    return render(request, "pages/add/add_note.html", context)


def list_activity1(request):
    activity = ActivityModel.objects.all()
    myfilter = Activity_ReportFilter(request.GET, queryset=activity)
    activity = myfilter.qs
    context = {'activities': activity, "myfilter": myfilter}
    return render(request, "pages/activtiy_list.html",context)


@login_required
def calender(request):
    tasks = TaskModel.objects.filter(Assign_to=request.user, )
    if request.user.groups.filter(name="admins").exists():
        tasks = TaskModel.objects.all()
    context = {'tasks': tasks}
    return render(request, "pages/calendar.html", context)
