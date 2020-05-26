from django.urls import path
from . import views

urlpatterns=[
    path('', views.home, name= 'home'),
    path('vendors/', views.vendors, name= 'vendors'),
    path('customerlogin/', views.customerLogin, name= 'customerlogin'),
    path('customersignup/', views.customerSignUp, name= 'customersignup'),
    path('customerlogin/', views.customerLogin, name= 'customerlogin'),
    path('createcustomer/', views.createCustomer, name= 'createcustomer'),
    path('customerprofile/', views.customerProfile, name= 'customerprofile'),
    path('updatecustomer/<int:id>/', views.updateCustomer, name= 'updatecustomer'),
    path('customermenu/', views.customerMenu, name= 'customermenu'),
    path('vendorsignup/', views.vendorSignup, name= 'vendorsignup'),
    path('vendorlogin/', views.vendorLogin, name= 'vendorlogin'),
    path('createvendor/', views.createVendor, name= 'createvendor'),
    path('vendorprofile/', views.vendorProfile, name= 'vendorprofile'),
    path('updatevendor/<int:id>/', views.updateVendor, name= 'updatevendor'),
    path('vendormenu/', views.vendorMenu, name= 'vendormenu'),
    path('addmenu/', views.addMenu, name= 'addmenu'),
    path('editvendormenu/<int:id>/', views.editVendormenu, name= 'editvendormenu'),
    path('orderlist/', views.orderplaced, name= 'orderplaced'),
    path('logout/', views.Logout, name= 'logout'),

]