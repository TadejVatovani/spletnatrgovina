from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Consumer

class LoginForm(forms.Form):
  email = forms.EmailField(label=_('email'), max_length=100)
  password = forms.CharField(label=_('password'), max_length=100, widget=forms.PasswordInput)
