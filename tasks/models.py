from django.db import models

from contact.models import ContactModel
from company.models import CompanyModel
from django.contrib.auth.models import User
from contact.models import Product
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class TaskModel(models.Model):
    choices = [
        ("Call", "Call"),
        ("Email", "Email"),
        ("Whatsapp message", "Whatsapp message"),
        ("Meet", "Meet"),
        ("Reminder", "Reminder"),
    ]
    choice = [
        ("pending", "pending"),
        ("done", "done"),
    ]
    task_name = models.CharField(max_length=50, blank=True, null=True)
    Assign_to = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    contact_person = models.ForeignKey(ContactModel, blank=True, null=True, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True, null=True)
    task_type = models.CharField(choices=choices, max_length=52, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    created_at = models.TimeField(auto_now=True)
    statue = models.CharField(choices=choice, max_length=100, blank=True, null=True)
    made_by = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.task_name)


class SendEmailModel(models.Model):
    contact_person = models.ForeignKey(ContactModel, on_delete=models.CASCADE)
    email = models.EmailField()
    subject = models.CharField(max_length=50, blank=True, null=True)
    about_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    message = models.TextField(max_length=500, )
    made_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(blank=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.subject)


class WhatsappModel(models.Model):
    contact_person = models.ForeignKey(ContactModel, blank=True, null=True, on_delete=models.CASCADE)
    phone = models.CharField(max_length=100, )
    message = models.TextField(max_length=500)
    about_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    made_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.phone)


class MeetingModel(models.Model):
    contact_person = models.ForeignKey(ContactModel, blank=True, null=True, on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True)
    subject = models.CharField(max_length=100)
    about_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    details = models.TextField(max_length=500, )
    made_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.subject)


class CallModel(models.Model):
    contact_person = models.ForeignKey(ContactModel, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True, null=True)
    about_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    details = models.TextField(max_length=500, )
    made_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.contact_person)


class NoteModel(models.Model):
    made_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    contact_person = models.ForeignKey(ContactModel, blank=True, null=True, on_delete=models.CASCADE)
    note = models.TextField(max_length=500, )
    create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)


class ActivityModel(models.Model):
    choices = [
        ("Call", "Call"),
        ("Email", "Email"),
        ("Whatsapp message", "Whatsapp message"),
        ("Meeting", "Meeting"),
        ("Note", "Note"),
    ]
    type = models.CharField(choices=choices, max_length=52, blank=True, null=True)
    made_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyModel, blank=True, null=True, on_delete=models.CASCADE)
    contact_person = models.ForeignKey(ContactModel, blank=True, null=True, on_delete=models.CASCADE)
    details = models.TextField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.CASCADE)
