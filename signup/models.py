from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import  settings
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save
from decimal import Decimal

# Create your models here.
class User(AbstractUser):
    is_customer= models.BooleanField(default= False)
    is_vendor= models.BooleanField(default= False)


class Customer(models.Model):
    user= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    firstname= models.CharField(max_length= 20, blank= False)
    lastname= models.CharField(max_length= 20, blank= False)
    email= models.EmailField(blank= False)
    phoneNumber= PhoneNumberField(blank= False, unique= True)
    amountOutstanding= models.DecimalField(max_digits=65, decimal_places= 2, default= Decimal('0.00'))
    dateTimeCreated= models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.user.username

class Vendor(models.Model):
    user= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    business_name= models.CharField(max_length= 20, blank= False)
    email= models.EmailField(max_length= 100, blank= False)
    phoneNumber= PhoneNumberField(blank= False)
    dateTimeCreated= models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.user.business_name



class Menu(models.Model):
    foodname= models.CharField(max_length= 150)
    description= models.TextField(max_length= 200)
    price= models.DecimalField(max_digits= 65, decimal_places= 2)
    quantity= models.PositiveSmallIntegerField()
    MENU_STATUS= (('Available', 'AVAILABLE'), ('Sold Out', 'SOLD OUT'))
    status= models.CharField(max_length= 30, choices= MENU_STATUS, default= 'AVAILABLE')
    dateTimeCreated= models.DateTimeField(auto_now_add= True)
    vendorId= models.ForeignKey(Vendor, on_delete= models.CASCADE)
    CHOICES= (('YES', 'YES'), ('NO', 'NO'))
    isRecurring= models.CharField(max_length= 10, default= 'YES', choices= CHOICES)
    CHOICES2= (('Breakfast, Mon', 'B1'),('Breakfast, Mon-Tue', 'B2'), ('Breakfast, Mon-Wed', 'B3'),
               ('Breakfast, Mon-Thur', 'B4'), ('Breakfast, Mon-Fri', 'B5'),
               ('Lunch, Mon', 'L1'), ('Lunch, Mon-Tue', 'L2'), ('Lunch, Mon-Wed', 'L3'),
               ('Lunch, Mon-Thur', 'L4'), ('Lunch, Mon-Fri', 'L5'), ('ONCE', 'ONCE'))

    frequencyofRecurrence= models.CharField(max_length= 30, choices= CHOICES2)

    def __str__(self):
        return self.foodname+' - '+str(self.price)

class Order(models.Model):
    vendorId= models.ForeignKey(Vendor, on_delete= models.CASCADE)
    totalamount= models.DecimalField(max_digits= 64, decimal_places= 2, default= Decimal('0.00'))
    orderedby= models.ForeignKey(User, on_delete= models.CASCADE, default= 1)

    ORDER_STATE_WAITING = "Waiting"
    ORDER_STATE_PLACED = "Placed"
    ORDER_STATE_ACKNOWLEDGED = "Acknowledged"
    ORDER_STATE_COMPLETED = "Completed"
    ORDER_STATE_CANCELLED = "Cancelled"
    ORDER_STATE_DISPATCHED = "Dispatched"

    ORDER_STATE_CHOICES = (
        (ORDER_STATE_WAITING, ORDER_STATE_WAITING),
        (ORDER_STATE_PLACED, ORDER_STATE_PLACED),
        (ORDER_STATE_ACKNOWLEDGED, ORDER_STATE_ACKNOWLEDGED),
        (ORDER_STATE_COMPLETED, ORDER_STATE_COMPLETED),
        (ORDER_STATE_CANCELLED, ORDER_STATE_CANCELLED),
        (ORDER_STATE_DISPATCHED, ORDER_STATE_DISPATCHED)
    )
    status = models.CharField(max_length=50, choices=ORDER_STATE_CHOICES, default=ORDER_STATE_WAITING)

    def __str__(self):
        return str(self.id) + ' ' + self.status


class OrderItem(models.Model):
    item_id = models.ForeignKey(Menu, on_delete=models.CASCADE)
    ord_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)


