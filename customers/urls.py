from django.urls import path
from . import views

urlpatterns = [path('', views.index, name='index'),
    path('customers/', views.customers, name='customers'),
    path('customers/<int:id>', views.get_customer, name='get_customer'),
    path('customers/<int:id>/delete', views.delete_customer, name='delete_customer'),
]