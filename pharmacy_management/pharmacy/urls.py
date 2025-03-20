from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('medicine_list/', views.medicine_list, name='medicine_list'),
    path('medicine_detail/<int:pk>/', views.medicine_detail, name='medicine_detail'),
    path('billing/', views.billing, name='billing'),
    path('bills/', views.bill_detail, name='bill_detail'),
    path('bill/<int:pk>/', views.bill_detail_view, name='bill_detail_view'),
]
