from django.core.validators import RegexValidator
from django.db import models
from company.models import CompanyModel
from django.contrib.auth.models import User
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from company.validator import validate_phone


class LeadsModel(models.Model):
    choices = [
        ("lead", "lead"),
        ("contact", "contact"),
    ]
    name = models.CharField(max_length=50, )
    mobile = models.CharField(max_length=20,  validators=[validate_phone])
    office_phone = models.CharField(max_length=20, blank=True, validators=[validate_phone])
    fax = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=50)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    social_account = models.CharField(max_length=50, blank=True)
    type = models.CharField(choices=choices, max_length=52, default='lead')
    notes = models.TextField(max_length=5000)
    created_at = models.DateField(auto_now=True)


class ContactModel(models.Model):
    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=50, )
    job_title = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=150, blank=True)
    street = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    mobile = models.CharField(max_length=20, validators=[validate_phone])
    office_phone = models.CharField(max_length=20, blank=True, validators=[validate_phone])
    fax = models.CharField(max_length=20, blank=True, validators=[validate_phone])
    email = models.CharField(max_length=50)
    created_at = models.DateField(auto_now=True)
    notes = models.TextField(max_length=5000)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


def image_upload(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'product/{0}/{1}'.format(instance.name, filename)


class Product(models.Model):
    name = models.CharField(max_length=50, )
    description = models.TextField(max_length=500, )
    img = models.ImageField(upload_to=image_upload, blank=True, null=True)

    def __str__(self):
        return self.name
