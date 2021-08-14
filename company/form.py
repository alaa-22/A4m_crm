from django import forms
from django.core.exceptions import ValidationError

from .models import CompanyModel


class Companyform(forms.ModelForm):
    '''def __init__(self, *args, **kwargs):
            super(Companyform, self).__init__(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'
    '''
    class Meta:
        model = CompanyModel
        fields = '__all__'


    """def clean_mobile(self):
        phone = self.cleaned_data['mobile']
        if not phone.isdigit():
            raise forms.ValidationError('Phone number can only contains digits')
        return phone
        
        
        
        
                    
"""
