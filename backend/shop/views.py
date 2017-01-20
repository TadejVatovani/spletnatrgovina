from django.http import *
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions import *
from django.core.urlresolvers import reverse

import sys

from .forms import *
from .models import *



app_name = 'shop'
def home(request):
	"""
	Returns the newest item added to database and the top 3 current promotions by start date

	Keyword arguments:
	request -- the django requst object
	"""
	promotion_list = Promotion.objects.order_by('-start')[:3]
	new_item = Product.objects.all()[len(Product.objects.all())-1]
	product_list = []
	for promotion in list(promotion_list):
		product_list.append(Product.objects.get(pk=promotion.id_Product.id))
	context = {'products': product_list,'newitem': new_item,'promotions': promotion_list} 
	return render(request, 'shop/Home.html', context)

def shop(request):
	"""
	Returns all the products in the database	

	Keyword arguments:
	request -- the django requst object
	"""
	product_list = Product.objects.order_by('-price')
	context = {'products': product_list}
	return render(request, 'shop/Shop.html',context)

def shopcategory(request, category):
	"""
	Returns all the products from the requested category	

	Keyword arguments:
	request -- the django requst object, category -- the requested category
	"""
	product_list = Product.objects.raw('SELECT * FROM shop_product WHERE category = %s', [category])	
	context = {'products': product_list}
	return render(request, 'shop/Shop.html',context)


def addtocart(request):
	"""
	Adds the ordered product to the cookie data

	Keyword arguments:
	request -- the django requst object
	"""
	if request.POST:
		if 'orders' in request.session:
			orders = request.session['orders']
			if not(str(request.POST['product']) in orders):
				orders[request.POST['product']]=1
			request.session['orders'] = orders;
		else:
			orders={request.POST['product']:1}
			request.session['orders'] = orders
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def deletefromcart(request,id):
	"""
	Removes the product from the cookie data	

	Keyword arguments:
	request -- the django requst object, id -- the id of the product to delete
	"""
	if 'orders' in request.session:
		del request.session['orders'][id]; 
		request.session.modified = True
		return HttpResponseRedirect(reverse('cart'))
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#
def register(request):
	"""
	Adds the register information to the database

	Keyword arguments:
	request -- the django requst object
	"""
	if request.POST:
		form = RegisterForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			firstname = form.cleaned_data['name']
			lastname = form.cleaned_data['lastname']
			address = form.cleaned_data['address']
			phone = form.cleaned_data['phone']
			password = form.cleaned_data['password']
			confirm = form.cleaned_data['confirm']
			zipcode = form.cleaned_data['zipcode']
			if password == confirm:	
				if not(User.objects.filter(username=email).exists()):
					user = User.objects.create(username=email)
					user.set_password(password)
					user.save()
					user = authenticate(username=email, password=password)
					login(request, user)
					customer = Customer(name=firstname, lastname=lastname, email=email, phone = phone)
					customer.save()
					address = Address(id_Customer=customer, postal=zipcode, address=address)
					address.save()
					return HttpResponseRedirect(reverse('home'))
			else:
				return HttpResponseRedirect(request.META.get('HTTP_REFERER'))		
	return render(request, 'shop/Register.html')


#Logins the user	
def loginuser(request):
	if request.POST:
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['email']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return HttpResponseRedirect(reverse('home'))
	return render(request, 'shop/Login.html')

#Logouts the user
def logoutuser(request):
	logout(request)
	request.session.flush()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#Renders the contact html	
def contact(request):
	return render(request, 'shop/Contact.html')

#Renders the about html	
def about(request):
	return render(request, 'shop/About.html')


def cart(request):
	"""
	Gets the data from the cookie and displays the products

	Keyword arguments:
	request -- the django requst object
	"""
	product_list = []
	if 'orders' in request.session:
		for id in request.session['orders']:
			product_list.append(Product.objects.get(pk=id))
	context = {'products': product_list}
	return render(request, 'shop/Cart.html',context)

def search(request):
	"""
	Searches the database based on the input and returns the found products

	Keyword arguments:
	request -- the django requst object
	"""
	if request.POST:
		product_list = Product.objects.raw("SELECT * FROM shop_product WHERE name LIKE %s OR category LIKE %s", ['%'+request.POST['search']+'%' ,'%'+request.POST['search']+'%' ])	
		context = {'products': product_list}
		return render(request, 'shop/Shop.html',context)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def checkorder(request):
	"""
	Shows the selected products and calculates the total cost when including the promotions on the products

	Keyword arguments:
	request -- the django requst object
	"""
	if request.POST:
		if 'orders' in request.session:
			quantity = request.session['orders']
			for id in quantity:
				quantity[id]=int(request.POST[id])
			request.session['orders']=quantity
			product_list = []
			total=0
			for id in request.session['orders'].keys():
				p=Product.objects.get(pk=int(id))
				product_list.append(p)
				promotion = Promotion.objects.all().filter(id_Product=p)
				if promotion:
					total+=int(quantity[id])*p.price*(100-promotion[0].discount)/100
				else:
					total+=int(quantity[id])*p.price
			if request.user.is_authenticated():
				c=Customer.objects.all().filter(email=request.user.username)[0]
				address=Address.objects.all().filter(id_Customer=c)[0]
				context = {'products': product_list,'quantity': quantity,'total':total,'address':address,'customer':c}
				return render(request, 'shop/Order.html',context)
			context = {'products': product_list,'quantity': quantity,'total':total}
			return render(request, 'shop/Order.html',context)			
	return HttpResponseRedirect(reverse('cart'))

def finishorder(request):
	"""
	If the user is logged in, uses his data, otherwise it registers the costumer from the input. After saving the consumer data, saves the order to the database

	Keyword arguments:
	request -- the django requst object
	"""
	if request.POST:
		if 'orders' in request.session:
			if request.user.is_authenticated():
				customer=Customer.objects.all().filter(email=request.user.username)[0]
			else:
				form = CustomerForm(request.POST)
				if form.is_valid():
					email = form.cleaned_data['email']
					firstname = form.cleaned_data['name']
					lastname = form.cleaned_data['lastname']
					address = form.cleaned_data['address']
					phone = form.cleaned_data['phone']
					zipcode = form.cleaned_data['zipcode']
					customer = Customer(name=firstname, lastname=lastname, email=email, phone = phone)
					customer.save()
					address = Address(id_Customer=customer, postal=zipcode, address=address)
					address.save()
			quantity = request.session['orders']
			product_list = []
			total=0				
			for id in request.session['orders'].keys():
				p=Product.objects.get(pk=int(id))
				product_list.append(p)
				promotion = Promotion.objects.all().filter(id_Product=p)
				if promotion:
					total+=int(quantity[id])*p.price*(100-promotion[0].discount)/100
				else:
					total+=int(quantity[id])*p.price
			receipt=Receipt(id_Customer=customer,paid=False,total=total)
			receipt.save()
			for product in product_list:
				q=int(quantity[str(product.id)])
				order=Order(id_Product=product,id_Receipt=receipt,quantity=q)
				order.save()
			request.session.flush()
		
	return HttpResponseRedirect(reverse('cart'))