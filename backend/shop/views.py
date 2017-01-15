from django.http import *
from django.shortcuts import get_object_or_404, render
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions import *
import sys
from django.core.urlresolvers import reverse


def home(request):
	promotion_list = Promotion.objects.order_by('-start')[:3]
	new_item = Product.objects.all()[len(Product.objects.all())-1]
	product_list = []
	for promotion in list(promotion_list):
		product_list.append(Product.objects.get(pk=promotion.id_Product.id))
	context = {'products': product_list,'newitem': new_item,'promotions': promotion_list} 
	return render(request, 'shop/Home.html', context)
	
def shop(request):
	product_list = Product.objects.order_by('-price')
	context = {'products': product_list}
	return render(request, 'shop/Shop.html',context)
	
def shopcategory(request, category):
	product_list = Product.objects.raw('SELECT * FROM shop_product WHERE category = %s', [category])	
	context = {'products': product_list}
	return render(request, 'shop/Shop.html',context)

def addtocart(request):
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
	if 'orders' in request.session:
		del request.session['orders'][id]; 
		request.session.modified = True
		return HttpResponseRedirect(reverse('cart'))
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	
def register(request):
	if request.POST:
		email = request.POST['email']
		firstname = request.POST['name']
		lastname = request.POST['lastname']
		address = request.POST['address']
		phone = request.POST['phone']
		password = request.POST['password']
		confirm = request.POST['confirm']
		zipcode = request.POST['zipcode']
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


	
def loginuser(request):
	if request.POST:
		username = request.POST['email']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse('home'))
	return render(request, 'shop/Login.html')

def logoutuser(request):
	logout(request)
	request.session.flush()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	
def contact(request):
	return render(request, 'shop/Contact.html')
	
def about(request):
	return render(request, 'shop/About.html')
	
def cart(request):
	product_list = []
	if 'orders' in request.session:
		for id in request.session['orders']:
			product_list.append(Product.objects.get(pk=id))
	context = {'products': product_list}
	return render(request, 'shop/Cart.html',context)

def search(request):
	if request.POST:
		product_list = Product.objects.raw("SELECT * FROM shop_product WHERE name LIKE %s OR category LIKE %s", ['%'+request.POST['search']+'%' ,'%'+request.POST['search']+'%' ])	
		context = {'products': product_list}
		return render(request, 'shop/Shop.html',context)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	
def checkorder(request):
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
	if request.POST:
		if 'orders' in request.session:
			if request.user.is_authenticated():
				customer=Customer.objects.all().filter(email=request.user.username)[0]
			else:
				email = request.POST['email']
				firstname = request.POST['name']
				lastname = request.POST['lastname']
				address = request.POST['address']
				phone = request.POST['phone']
				zipcode = request.POST['zipcode']
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