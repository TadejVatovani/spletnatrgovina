from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from .models import Customer

class LoginForm(forms.Form):
	email = forms.EmailField(label=_('email'), max_length=20)
	password = forms.CharField(label=_('password'), max_length=100, widget=forms.PasswordInput)

  
class RegisterForm(forms.Form):
	email = forms.EmailField(label=_('email'), max_length=20)
	password = forms.CharField(label=_('password'), max_length=100, widget=forms.PasswordInput)
	confirm = forms.CharField(label=_('password'), max_length=100, widget=forms.PasswordInput)
	name = forms.CharField(label=_('name'), max_length=20)
	lastname = forms.CharField(label=_('lastname'), max_length=20)
	address = forms.CharField(label=_('address'), max_length=50)
	phone = forms.CharField(label=_('phone'), validators=[RegexValidator(regex='^\d{9}$', message='A phone number is 9 digits', code='nomatch')], max_length=9)
	zipcode = forms.CharField(validators=[RegexValidator(regex='^\d{4}$', message='Not a postal code', code='nomatch')],max_length=4)
	
class CustomerForm(forms.Form):
	email = forms.EmailField(label=_('email'), max_length=20)
	name = forms.CharField(label=_('name'), max_length=20)
	lastname = forms.CharField(label=_('lastname'), max_length=20)
	address = forms.CharField(label=_('address'), max_length=50)
	phone = forms.CharField(label=_('phone'), validators=[RegexValidator(regex='^\d{9}$', message='A phone number is 9 digits', code='nomatch')], max_length=9)
	zipcode = forms.CharField(label=_('zipcode'), validators=[RegexValidator(regex='^\d{4}$', message='Not a postal code', code='nomatch')],max_length=4)