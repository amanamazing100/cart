from django.shortcuts import render, redirect
from .models import *
from .forms import CreateNewUser
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

login_required(login_url='login')
def home(request, *args, **kwargs):
	products = Product.objects.all()
	if request.user.is_authenticated:
		order, created = Order.objects.get_or_create(customer=request.user)
		productsordered = order.orderitem_set.all()
		recc = Product.objects.none()
		categoryintrested = []
		for prod in productsordered:
			categoryintrested.append(prod.product.category)
		#print(categoryintrested)
		for category in categoryintrested:
			temp = Product.objects.filter(category=category)
			recc = recc.union(temp)
		productbought = Product.objects.none()
		for prod in productsordered:
			temp = Product.objects.filter(name=prod.product.name)
			productbought = productbought.union(temp)
		recc = recc.difference(productbought)
		print(recc)
		context = {'products': products,
		'recc': recc}
	else:
		return redirect('login')
	return render(request, 'home.html', context)



login_required(login_url='login')
def cart(request, *args, **kwargs):
	if request.user.is_authenticated:
		order, created = Order.objects.get_or_create(customer=request.user)
		items = order.orderitem_set.all()
	else:
		items = []
	context = {'items': items,
		'order': order}
	return render(request, 'cart.html', context)

'''
login_required(login_url='login')
def recommend(request):
	order, created = Order.objects.get_or_create(customer=request.user)
	recc = Product.objects.none()

	products = Product.objects.all()
	categoryintrested = []
	for prod in productsordered:
		categoryintrested.append(prod.product.category)
	#print(categoryintrested)
	for category in categoryintrested:
		temp = Product.objects.filter(category=category)
		
		recc = recc.union(temp)
		#print(recc)
	#print(recc)
	productbought = Product.objects.none()
	for prod in productsordered:
		temp = Product.objects.filter(name=prod.product.name)
		productbought = productbought.union(temp)
	recc = recc.difference(productbought)
	print(recc)
	context = {
	'products': products
	}
	return render(request, 'home.html', context)
'''
	



login_required(login_url='login')
def checkout(request, *args, **kwargs):
	if request.user.is_authenticated:
		customer = request.user
		order, created = Order.objects.get_or_create(customer=customer)
		items = order.orderitem_set.all()
	else:
		items = []
	context = {'items': items,
	'order': order,
	'customer': customer}
	return render(request, 'checkout.html', context)

def addcart(request, id):
	#customer = request.user.customer
	objectadd = Product.objects.get(id=id)
	order, created = Order.objects.get_or_create(customer=request.user)
	print(created)
	if OrderItem.objects.filter(order=order, product = objectadd).exists():
		orderitem = OrderItem.objects.get(order=order, product = objectadd)
		print(orderitem.quantity)
		orderitem.quantity += 1
		orderitem.save()
		items = order.orderitem_set.all()
		context = {'items': items,
		'order': order}
		return redirect('cart')
	else:
		OrderItem.objects.create(order=order, product = objectadd, quantity=1)
	items = order.orderitem_set.all()
	context = {'items': items,
		'order': order}
	return render(request, 'cart.html', context)


def removecart(request, id):
	objectrem = Product.objects.get(id=id)
	order = Order.objects.get(customer=request.user)
	if OrderItem.objects.filter(order=order, product = objectrem).exists():
		orderitem = OrderItem.objects.get(order=order, product = objectrem)
		print(orderitem.quantity)
		orderitem.quantity -= 1
		orderitem.save()
		if orderitem.quantity == 0:
			orderitem.delete()
			return redirect('cart')
		items = order.orderitem_set.all()
		context = {'items': items,
		'order': order}
		return redirect('cart')
	else:
		return redirect('cart')
	return render(request, 'cart.html', context)
'''
def registerSeller(request):
	form = CreateNewSeller()
	if request.method == 'POST':
		form = CreateNewSeller(request.POST)
		if form.is_valid():
			form.save()
			return redirect('sell')
	context = {'form': form}
	return render(request, 'register.html', context)

def createProduct(request):
	form = CreateNewProduct()
	if request.method == 'POST':
		form = CreateNewProduct(request.POST)
		if form.is_valid():
			form.save()
			return redirect('home')
	context = {'form': form}
	return render(request, 'newproduct.html', context)
'''

def registerUser(request):
	form = CreateNewUser()
	if request.method == 'POST':
		form = CreateNewUser(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login')
	context = {'form': form}
	return render(request, 'register.html', context)

def loginUser(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		email = request.POST.get('email')
		user = authenticate(username=username, password=password)
		if user is not None:
			#customer = User.objects.create(username=username)
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username or password incorrect')
			return render(request, 'login.html', {})

	return render(request, 'login.html', {})


login_required(login_url='login')
def logoutUser(request):
	logout(request)
	return redirect('login')

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

def sendMail(request):
	if request.user.is_authenticated:
		order, created = Order.objects.get_or_create(customer=request.user)
		items = order.orderitem_set.all()
		template = render_to_string('email_template.html', {'name': request.user, 'items': items})
		email = EmailMessage(
			'Thanks for purchasing!',
			template,
			settings.EMAIL_HOST_USER,
			[request.user.email],
			)
		email.fail_silently = False
		email.send()
	return redirect('home')