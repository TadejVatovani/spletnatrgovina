from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Product(models.Model):
	name = models.CharField(max_length=40)
	description = models.CharField(max_length=200)
	size = models.CharField(max_length=40)
	category = models.CharField(max_length=20)
	supply = models.IntegerField(default=0)
	price = models.FloatField(default=0)
	def __str__(self):
		return self.name

class Customer(models.Model):
	name = models.CharField(max_length=20)
	lastname = models.CharField(max_length=20)
	email = models.CharField(max_length=20)
	phone = models.CharField(validators=[RegexValidator(regex='^\d{9}$', message='A phone number is 9 digits', code='nomatch')],max_length=9)
	def __str__(self):
		return self.email
	
class Address(models.Model):
	id_Customer= models.ForeignKey(Customer, on_delete=models.CASCADE)
	postal= models.CharField(validators=[RegexValidator(regex='^\d{4}$', message='Not a postal code', code='nomatch')],max_length=4)
	address = models.CharField(max_length=50)
	def __str__(self):
		return self.address

class Receipt(models.Model):
	id_Customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	paid = models.BooleanField(default=False)
	total = models.FloatField(default=0)

class Order(models.Model):
	id_Product = models.ForeignKey(Product, on_delete=models.CASCADE)
	id_Receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=0)
	
class Promotion(models.Model):
	id_Product = models.ForeignKey(Product, on_delete=models.CASCADE)
	discount = models.FloatField(default=0)
	start = models.DateTimeField('date of the start of the promotion', default=timezone.now )
	end = models.DateTimeField('date of the end of the promotion', default=timezone.now )
	def __str__(self):
		return self.id_Product.name
