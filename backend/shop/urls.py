from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
	url(r'^logoutuser', views.logoutuser, name='logoutuser'),
	url(r'Shop/addtocart', views.addtocart, name='addtocart'),
	url(r'Shop/search', views.search, name='search'),
	url(r'Shop/(?P<category>\w+)/$', views.shopcategory, name='shopcategory'),
	url(r'Shop', views.shop, name='shop'),
	url(r'Home', views.home, name='home'),
	url(r'Cart/checkorder', views.checkorder, name='checkorder'),
	url(r'Order/finishorder', views.finishorder, name='finishorder'),
	url(r'Cart/deletefromcart/(?P<id>\d+)/$', views.deletefromcart, name='deletefromcart'),
	url(r'Cart', views.cart, name='cart'),
	url(r'Register', views.register, name='register'),
	url(r'Login', views.loginuser, name='loginuser'),
	url(r'Contact', views.contact, name='contact'),
	url(r'About', views.about, name='about'),
	url(r'Order', views.checkorder, name='checkorder')
	
]