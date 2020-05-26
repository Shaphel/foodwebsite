from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login,logout
from .forms import CustomerSignUpForm, CustomerForm, VendorSignUpForm, VendorForm, MenuForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Customer, User, Vendor, Menu

# Create your views here.

# General Views.................................#######
def home(request):
    return render(request, 'signup/home.html')

def vendors(request):
    v_object= Vendor.objects.all()
    query= request.GET.get('q')
    if query:
        v_object= Vendor.objects.filter(Q(business_name_icontains= query)).distinct()
        return render(request, 'signup/vendors.html', {'v_object': v_object})
    return render(request, 'signup/vendors.html', {'v_object': v_object})

def Logout(request):
    if request.user.is_vendor:
        logout(request)
        return redirect('vendorlogin')
    return redirect('customerlogin')



# Customer Views.........................................#####

def customerSignUp(request):
    form= CustomerSignUpForm(request.POST or None)
    if form.is_valid():
        user= form.save(commit= False)
        username= form.cleaned_data['username']
        password= form.cleaned_data['password']
        user.is_customer= True
        user.set_password(password)
        user.save()
        user= authenticate(username= username, password= password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('createcustomer')
    context= {'form': form}
    return render(request, 'signup/customersignup.html', context)

def customerLogin(request):
    if request.method == 'POST':
        username= request.POST['username']
        password= request.POST['password']
        user= authenticate(username= username, password= password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('customerprofile')
            else:
                return render(request, 'signup/login.html', {'error_message': 'Your account Is Inactive'})
        else:
            return render(request, 'signup/login.html', {'error_message': 'Login Invalid!'})
    return render(request, 'signup/login.html')


def customerProfile(request, pk= None):
    if pk:
        user= User.objects.get(pk=pk)
    else:
        user= request.user
    return render(request, 'signup/customerprofile.html', {'user': user})


@login_required(login_url='/customerlogin/')
def createCustomer(request):
    form= CustomerForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance= form.save(commit= False)
        instance.user= request.user
        instance.save()
        return redirect('customerprofile')
    context= {'form': form, 'title': 'Complete Your Profile'}
    return render(request, 'signup/customerprofile_form.html', context)



@login_required(login_url='/customerlogin/')
def updateCustomer(request, id):
    form= CustomerForm(request.POST or None, request.FILES or None, instance= request.user.customer)
    if form.is_valid():
        form.save()
        return redirect('customerprofile')
    context= {'form': form, 'title': 'Update Your Profile'}
    return render(request, 'signup/customerprofile_form.html', context)


@login_required(login_url='/vendorlogin/')
def customerMenu(request):
    #form= MenuForm()
    menus= Menu.objects.all()
    return render(request, 'signup/customermenu.html', {'menus': menus})



# vendor half.................................

def vendorSignup(request):
    form= VendorSignUpForm(request.POST or None)
    if form.is_valid():
        user= form.save(commit= False)
        username= form.cleaned_data['username']
        password= form.cleaned_data['password']
        user.is_vendor= True
        user.set_password(password)
        user.save()
        user= authenticate(username= username, password= password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('createvendor')
    context= {'form': form}
    return render(request, 'signup/vendorsignup.html', context)

# vendor login
def vendorLogin(request):
    if request.method == 'POST':
        username= request.POST['username']
        password= request.POST['password']
        user= authenticate(username= username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('vendorprofile')
            else:
                return render(request, 'signup/vendorlogin.html', {'error_message':'Inactive Account'})
        else:
            return render(request, 'signup/vendorlogin.html', {'error_message': 'Invalid Login'})
    return render(request, 'signup/vendorlogin.html')


#profile view
def vendorProfile(request, pk= None):
    if pk:
        user= User.objects.get(pk=pk)
    else:
        user= request.user
    return render(request, 'signup/vendorprofile.html', {'user': user})


# filling vendor details
@login_required(login_url='/vendorlogin/')
def createVendor(request):
    form= VendorForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance= form.save(commit= False)
        instance.user= request.user
        instance.save()
        return redirect('vendorprofile')
    context= {'form': form, 'title': 'Complete Your Profile'}
    return render(request, 'signup/vendorprofile_form.html', context)

# Update vendor details
@login_required(login_url='/vendorlogin/')
def updateVendor(request, id):
    form= VendorForm(request.POST or None, request.FILES or None, instance= request.user.vendor)
    if form.is_valid():
        form.save()
        return redirect('vendorprofile')
    context= {'form': form, 'title': 'Update Your Profile'}
    return render(request, 'signup/vendorprofile_form.html', context)


# vendor makes menu
@login_required(login_url='/vendorlogin/')
def vendorMenu(request):
    form= MenuForm()
    menus= Menu.objects.filter(vendorId= request.user.vendor).order_by('-id')
    return render(request, 'signup/menu.html', {'form': form, 'menus': menus})

@login_required(login_url='/vendorlogin/')
def addMenu(request):
    form= MenuForm()
    if request.method == 'POST':
        form= MenuForm(request.POST, request.FILES)
        if form.is_valid():
            menu= form.save(commit= False)
            menu.vendorId= request.user.vendor
            menu.save()
            return redirect('vendormenu')
    return render(request, 'signup/addmenu.html', {'form': form})


@login_required(login_url='/vendorlogin/')
def editVendormenu(request, id):
    form = MenuForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        menu= Menu.objects.get(id= id)
        form= MenuForm(request.POST, instance= menu)
        form.save()
        return redirect('vendormenu')
    else:
        menu= Menu.objects.get(id= id)
        form= MenuForm(instance= menu)
    context = {'form': form, 'title': 'Edit Menu'}
    return render(request, 'signup/editvendormenu.html', context)


def orderplaced(request):
    return render(request, 'signup/orderplaced.html', {})
