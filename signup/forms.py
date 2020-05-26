from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, Customer, Vendor, Menu

class CustomerSignUpForm(forms.ModelForm):
    password= forms.CharField(widget= forms.PasswordInput)
    class Meta:
        model= User
        fields= ['username', 'email', 'password']
        def save(self, commit= True):
            user= super().save(commit= False)
            user.is_customer= True
            if commit:
                user.save()
            return user


class CustomerForm(forms.ModelForm):
    class Meta:
        model= Customer
        fields= ['firstname', 'lastname', 'email', 'phoneNumber']


class VendorSignUpForm(forms.ModelForm):
    password= forms.CharField(widget= forms.PasswordInput)

    class Meta:
        model= User
        fields= ['username', 'password']
        def save(self, commit= True):
            user= super().save(commit= False)
            user.is_vendor= True
            if commit:
                user.save()
            return user


class VendorForm(forms.ModelForm):
    class Meta:
        model= Vendor
        fields= ['business_name', 'email', 'phoneNumber']


class MenuForm(forms.ModelForm):
    class Meta:
        model= Menu
        fields= ['foodname', 'description', 'price', 'quantity', 'status', 'isRecurring', 'frequencyofRecurrence']
