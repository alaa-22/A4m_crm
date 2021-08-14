from django import forms
from .models import ContactModel, LeadsModel, Product


class Contactform(forms.ModelForm):
    class Meta:
        model = ContactModel
        fields = '__all__'


class Leadform(forms.ModelForm):
    class Meta:
        model = LeadsModel
        fields = '__all__'


class Productform(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
