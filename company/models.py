import pytz
from django.db import models

from django.contrib.auth.models import User

from django.core.exceptions import ValidationError

# creating a validator function
# Create your models here.
from .validator import validate_phone


def file_upload(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'company_file/company {0}/{1}'.format(instance.company_name, filename)


class CompanyModel(models.Model):
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    company_name = models.CharField(max_length=50)
    industry = models.CharField(max_length=50, blank=True)
    company_owner = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=150, blank=True)
    street = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    mobile = models.CharField(max_length=20, validators=[validate_phone])
    office_phone = models.CharField(max_length=20, blank=True, null=True)
    fax = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=30)
    employees_numbers = models.IntegerField(blank=True, null=True)
    social_page = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.company_name)
