from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.core import serializers
from django.forms.models import model_to_dict
from .models import Customer
from .filters import CustomerFilter
from .forms import CustomerForm
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
import json

@api_view()
def index(response):
    form = CustomerForm()
    customers = Customer.objects.all()
    total_customers = len(customers)
    return render(response, 'home.html', {'form': form, customers: 'customers', 'total_customers': total_customers})

@swagger_auto_schema(method='get',
    manual_parameters=[
        openapi.Parameter( 'city', in_=openapi.IN_QUERY, description='Customers by city', type=openapi.TYPE_STRING, ),
        openapi.Parameter( 'state', in_=openapi.IN_QUERY, description='Customers by state', type=openapi.TYPE_STRING, ),
        openapi.Parameter( 'zip', in_=openapi.IN_QUERY, description='Customers by zip code', type=openapi.TYPE_STRING, ),
    ])
@swagger_auto_schema(methods=['post'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['version'],
        properties={
            'first_name': openapi.Schema(type=openapi.TYPE_STRING, description="Customer's first name"),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING, description="Customer's last name"),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description="Customer's email address"),
            'address': openapi.Schema(type=openapi.TYPE_STRING, description="Customer's physical address"),
            'city': openapi.Schema(type=openapi.TYPE_STRING, description="Customer's city"),
            'state': openapi.Schema(type=openapi.TYPE_STRING, description="Customer's state"),
            'zip': openapi.Schema(type=openapi.TYPE_STRING, description="Customer's zip code"),
        },
    ),
    operation_description='Post new customer')
@api_view(['GET', 'POST'])
def customers(response):
    if response.method == 'POST':
        post(response)

    data = Customer.objects.order_by('last_name')

    filter = CustomerFilter(response.GET, queryset=data)	
    filtered_data = serializers.serialize('python', filter.qs)
    processed_filtered_data = [c['fields'] for c in filtered_data]

    return HttpResponse(json.dumps(processed_filtered_data), content_type="application/json")

@api_view()
def post(response):
    form = CustomerForm(response.POST)
    if form.is_valid():
        form.save()
    else:
        return Http404("Form is invalid; please try again")

@api_view()
def get_customer(response, id):
    customer = verify_customer(id)
    processed_data = model_to_dict(customer)
    return JsonResponse(processed_data)

@api_view()
def delete_customer(response, id):
    customer = verify_customer(id)
    customer.delete()
    return redirect('customers')

def verify_customer(id):
    try:
        customer = Customer.objects.get(pk=id)
        return customer
        #processed_data = {'Full name': customer.get_full_name()}
    except Customer.DoesNotExist:
        raise Http404("Customer does not exist")

'''
first_name -- The customer's first name
last_name -- The customer's last name
email -- The customer's email address
address -- The customer's physical address
city -- The customer's city in their address
state -- The customer's state in their address
zip -- The customer's zip code'''

'''
Documentation
---
parameters:
    - name: first_name
        description: First name of customer
        type: string
    - name: last_name
        description: Last name of customer
        type: string
    - name: email
        description: Email address of customer
        type: string
    - name: address
        description: Physical address of customer
        type: string
    - name: city
        description: City of customer
        type: string
    - name: state
        description: State of customer
        type: string
    - name: zip
        description: Zip code of customer
        type: string
'''