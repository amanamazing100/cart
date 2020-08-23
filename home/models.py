from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
	#return self.name
class Category(models.Model):
	name = models.CharField(max_length=50, null=True, blank=True)
	def __str__(self):
		return self.name
'''
class Seller(models.Model):
	name = models.CharField(max_length=50, null=True)
	def __str__(self):
		return self.name
'''

class Product(models.Model):
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
	#seller = models.ForeignKey(Seller, null=True, on_delete=models.SET_NULL, blank=True)
	name = models.CharField(max_length=50)
	price = models.FloatField(null=True)
	image = models.ImageField(null=True, blank=True)
	
	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse("addcart", kwargs={"id": self.id})
	def get_ab_url(self):
		return reverse("removecart", kwargs={"id": self.id})

class Order(models.Model):
	CHOICES = (
		('D', 'DELIEVERED'),
		('P', 'PENDING')
		)
	customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
	status = models.CharField(null=True, blank=True, max_length=100, choices=CHOICES)
	date = models.DateField(auto_now_add=True)
	transid = models.IntegerField(null=True)
	def __str__(self):
		return str(self.id)

	@property
	def no_of_items(self):
		no_of_item = self.orderitem_set.all()
		total = sum([item.quantity for item in no_of_item])
		return total


	@property
	def total_of_items(self):
		no_of_item = self.orderitem_set.all()
		total = sum([item.sub_total for item in no_of_item])
		return total


class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	
	@property
	def sub_total(self):
		return self.quantity * self.product.price
	


class ShippingAddress(models.Model):
	customer = models.ForeignKey(User, on_delete=models.CASCADE)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
	address = models.CharField(max_length=250)

	def __str__(self):
		return self.address