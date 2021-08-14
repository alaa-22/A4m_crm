import datetime
from os.path import join

import pytz
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from .models import *
from .form import *
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .filters import CompanyFilter
from contact.models import ContactModel, LeadsModel
from tasks.models import ActivityModel
from tasks.filters import ActivityFilter
from crm.decor import custom_permission_required
from django.contrib.auth.models import User
from crm.functions import logs
from tasks.models import TaskModel

from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import Q


# Create your views here.

def dashboard(request):
    user = User.objects.all().count()
    company_count = CompanyModel.objects.all().count()
    contact = ContactModel.objects.all().count()
    lead = LeadsModel.objects.all().count()
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    tasks = TaskModel.objects.exclude(task_type='Reminder').filter(Assign_to=request.user,
                                                                   date__range=(today_min, today_max))
    if request.user.groups.filter(name="admins").exists() or request.user.is_superuser:
        tasks = TaskModel.objects.exclude(task_type='Reminder').filter(date__range=(today_min, today_max))
    paginator = Paginator(tasks, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # paginator for reminders
    reminders = TaskModel.objects.filter(made_by=request.user, task_type="Reminder", date__range=(today_min, today_max))

    paginator1 = Paginator(reminders, 5)
    page_number1 = request.GET.get('page')
    page_obj1 = paginator1.get_page(page_number1)
    arr = {}
    array = {}
    for i in range(1, 13):
        i = "{:02d}".format(i)
        conp = CompanyModel.objects.filter(created_at__year=timezone.now().year, created_at__month=i).count()

        cont = ContactModel.objects.filter(created_at__year=timezone.now().year, created_at__month=i).count()
        array[i] = cont
        arr[i] = conp
    print(lead)
    context = {
        "users": user,
        "company_count": company_count,
        "contact": contact,
        "lead": lead,
        "tasks": page_obj,
        "reminders": page_obj1,
        "arr": arr,
        "array": array,
    }
    return render(request, "pages/dashboard1.html", context)


@login_required
@custom_permission_required('company.view_companymodel')
def company_list(request):
    company = CompanyModel.objects.all()
    myfilter = CompanyFilter(request.GET, queryset=company)
    company = myfilter.qs
    paginator = Paginator(company, 10)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {"company": page_obj, "myfilter": myfilter}
    return render(request, "pages/company_list.html", context)


def fetch_resources(uri, rel):
    path = join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ""))
    return path


@login_required
def company_profile(request, pk):
    company = CompanyModel.objects.get(id=pk)
    contact = ContactModel.objects.filter(company=company)
    activtiy = ActivityModel.objects.filter(company=company)
    myfilter = ActivityFilter(request.GET, queryset=activtiy)
    activtiy = myfilter.qs
    context = {"company": company, "contacts": contact, "activities": activtiy, "myfilter": myfilter}
    return render(request, "pages/company_profile.html", context)


@login_required
@custom_permission_required('company.add_companymodel')
def add_company(request):
    if request.method == 'POST':
        company = Companyform(request.POST, request.FILES)
        if company.is_valid():
            mform = company.save(commit=False)
            mform.added_by = request.user
            mform.save()
            logs('add', None, request, CompanyModel)
            messages.success(request, "company added Successfully")

            return redirect('company:company_home')
        else:
            print(company.errors)
            messages.error(request, "error")

    else:
        company = Companyform()
    context = {'form': company}
    return render(request, "pages/add_company.html", context)


@login_required
@custom_permission_required('company.change_companymodel')
def edit_company(request, pk):
    company = CompanyModel.objects.get(id=pk)
    form = Companyform(instance=company)
    if request.method == "POST":
        mform = Companyform(request.POST, instance=company)
        if mform.is_valid():
            mform.save()
            logs('edit', company, request, CompanyModel)
            messages.success(request, "company updated Successfully")

            return redirect('company:company_home')
        else:
            print(form.errors)
            messages.error(request, "error")
    context = {"form": form}
    return render(request, "pages/edit_company.html", context)


@login_required
@custom_permission_required('company.delete_companymodel')
def delete_company(request, pk):
    company = CompanyModel.objects.get(id=pk)
    company.delete()
    logs('delete', company, request, CompanyModel)
    return redirect(reverse('company:company_home'))


def company_report(request):
    company = CompanyModel.objects.all()
    myfilter = CompanyFilter(request.GET, queryset=company)
    company = myfilter.qs
    context = {"company": company, "myfilter": myfilter}
    return render(request, "pages/company_report.html", context)


"""def render_pdf_view(request):
    template_path = 'pages/company_list.html'
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
        html.encode("UTF-8"), dest=response, encoding='UTF-8')
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
"""
