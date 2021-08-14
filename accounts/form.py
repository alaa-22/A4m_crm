from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User, Group

from .models import Profile


class UserCreateform(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'groups', 'is_active', 'first_name', 'last_name']

    '''def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(UserCreateform, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['password1'].required = False
        self.fields['password2'].required = False'''


class Userform(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email',  'groups', 'is_active', 'first_name', 'last_name','is_superuser']

    '''def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(Userform, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['password1'].required = False
        self.fields['password2'].required = False'''


class UserGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'


class Profileform(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']
