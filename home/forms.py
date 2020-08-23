from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *
class CreateNewUser(UserCreationForm):
	class Meta:
		model = User
		fields = [
		'username', 'email', 'password1', 'password2'
		]

'''
class CreateNewSeller(UserCreationForm):
	class Meta:
		model = Seller
		fields = [
		'name', 'password1', 'password2'
		]

class CreateNewProduct(UserCreationForm):
	class Meta:
		model = Product
		fields = [
		'category', 'name', 'price', 'image', 'seller'
		]

'''