from django.contrib import admin
from .models import ContactModel,LeadsModel

# Register your models here.
admin.site.register(ContactModel)
admin.site.register(LeadsModel)