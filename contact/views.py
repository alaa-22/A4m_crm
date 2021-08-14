from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse

from .form import Contactform, Leadform, Productform
from .models import ContactModel, LeadsModel, Product
from .filters import ContactFilter, LeadFilter
from company.models import CompanyModel
from tasks.models import ActivityModel
from tasks.filters import ActivityFilter
from crm.decor import custom_permission_required
from crm.functions import logs


# Create your views here.


@login_required
@custom_permission_required('contact.view_contactmodel')
def contact_list(request):
    contact = ContactModel.objects.all()

    myfilter = ContactFilter(request.GET, queryset=contact)
    contact = myfilter.qs
    paginator = Paginator(contact, 6)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {"contacts": page_obj, "myfilter": myfilter}
    return render(request, "pages/contact_list.html", context)


@login_required
@custom_permission_required('contact.add_contactmodel')
def add_contact(request):
    if request.method == 'POST':
        contact = Contactform(request.POST)
        if contact.is_valid():
            mform = contact.save(commit=False)
            mform.added_by = request.user
            mform.save()
            logs('add', None, request, ContactModel)
            messages.success(request, "contact added Successfully")
            return redirect('contact:contact_home')
        else:
            print(contact.errors)
            messages.error(request, "error")
    else:
        contact = Contactform()
    context = {'form': contact}
    return render(request, "pages/add_contact.html", context)


@login_required
@custom_permission_required('contact.change_contactmodel')
def edit_contact(request, pk):
    contact = ContactModel.objects.get(id=pk)
    form = Contactform(instance=contact)
    if request.method == "POST":
        mform = Contactform(request.POST, instance=contact)
        if mform.is_valid():
            mform.save()
            logs('edit', contact, request, ContactModel)
            messages.success(request, "contact updated Successfully")
            return redirect('contact:contact_home')
        else:
            print(form.errors)
            messages.error(request, "error")
    context = {"form": form}
    return render(request, "pages/edit_contact.html", context)


@login_required
def contact_profile(request, pk):
    contact = ContactModel.objects.get(id=pk)
    comp = contact.company
    company = CompanyModel.objects.get(company_name=comp)
    activtiy = ActivityModel.objects.filter(contact_person=contact)
    myfilter = ActivityFilter(request.GET, queryset=activtiy)
    activtiy = myfilter.qs
    context = {"contact": contact, "company": company, "activities": activtiy, "myfilter": myfilter}
    return render(request, "pages/contact_profile.html", context)


@login_required
@custom_permission_required('contact.delete_contactmodel')
def delete_contact(request, pk):
    contact = ContactModel.objects.get(id=pk)
    contact.delete()
    logs('delete', contact, request, ContactModel)

    return redirect(reverse('contact:contact_home'))


@login_required
@custom_permission_required('contact.add_leadsmodel')
def add_lead(request):
    if request.method == 'POST':
        lead = Leadform(request.POST)
        if lead.is_valid():
            mform = lead.save(commit=False)
            mform.added_by = request.user
            mform.type = 'lead'
            mform.save()
            logs('add', None, request, LeadsModel)
            messages.success(request, "leads added Successfully")
            return redirect('contact:list_lead')
        else:
            print(lead.errors)
            messages.error(request, "error")
    else:
        lead = Leadform()
    context = {'form': lead}
    return render(request, "pages/add_lead.html", context)


@login_required
@custom_permission_required('contact.change_contactmodel')
def edit_lead(request, pk):
    lead = LeadsModel.objects.get(id=pk)
    form = Leadform(instance=lead)
    if request.method == "POST":
        mform = Leadform(request.POST, instance=lead)
        if mform.is_valid():
            mform.save()
            logs('edit', lead, request, LeadsModel)
            messages.success(request, "lead updated Successfully")
            return redirect('contact:list_lead')
        else:
            print(form.errors)
            messages.error(request, "error")
    context = {"form": form, "lead": lead}
    return render(request, "pages/edit_lead.html", context)


@login_required
@custom_permission_required('contact.change_leadsmodel')
def lead_list(request):
    lead = LeadsModel.objects.all()

    myfilter = LeadFilter(request.GET, queryset=lead)
    lead = myfilter.qs
    paginator = Paginator(lead, 10)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {"leads": page_obj, "myfilter": myfilter}
    return render(request, "pages/lead_list.html", context)


@login_required
@custom_permission_required('contact.delete_leadsmodel')
def delete_lead(request, pk):
    lead = LeadsModel.objects.get(id=pk)
    lead.delete()
    logs('delete', lead, request, LeadsModel)

    return redirect(reverse('contact:list_lead'))


@login_required
@custom_permission_required('')
def convert_lead(request, pk):
    lead = LeadsModel.objects.get(id=pk)
    LeadsModel.objects.filter(id=pk).update(type='contact')
    t = ContactModel.objects.create(name=lead.name, mobile=lead.mobile, office_phone=lead.office_phone
                                    , fax=lead.fax, email=lead.email, notes=lead.notes, added_by=request.user)
    # logs('add', None, t, ContactModel)
    return redirect(reverse('contact:list_lead'))


# Products
def add_product(request):
    if request.method == 'POST':
        form = Productform(request.POST, request.FILES)
        if form.is_valid():
            print(form)
            form.save()
            print(form)
            logs('add', None, request, Product)
            messages.success(request, "product added Successfully")
        else:
            messages.error(request, "error")

    form = Productform()
    context = {'form': form}
    return render(request, "pages/add_product.html", context)


def list_product(request):
    product = Product.objects.all()
    paginator = Paginator(product, 6)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {"products": page_obj}
    return render(request, "pages/product_list.html", context)


def contact_report(request):
    contact = ContactModel.objects.all()
    myfilter = ContactFilter(request.GET, queryset=contact)
    contact = myfilter.qs
    context = {"contacts": contact, "myfilter": myfilter}
    return render(request, "pages/contact_report.html", context)


def lead_report(request):
    lead = LeadsModel.objects.all()
    myfilter = ContactFilter(request.GET, queryset=lead)
    lead = myfilter.qs
    context = {"leads": lead, "myfilter": myfilter}
    return render(request, "pages/lead_report.html", context)
