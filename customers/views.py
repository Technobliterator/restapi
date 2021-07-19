from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.core import serializers
from django.forms.models import model_to_dict
from .models import Customer
from .filters import CustomerFilter
from .forms import CustomerForm
from rest_framework.decorators import api_view
import json

@api_view()
def index(response):
    form = CustomerForm()
    customers = Customer.objects.all()
    total_customers = len(customers)
    return render(response, 'home.html', {'form': form, customers: 'customers', 'total_customers': total_customers})

@api_view(['GET', 'POST'])
def customers(response):
    status = 200
    if response.method == 'POST':
        post(response)
        status = 201

    data = Customer.objects.order_by('last_name')

    filter = CustomerFilter(response.GET, queryset=data)	
    filtered_data = serializers.serialize('python', filter.qs)
    processed_filtered_data = [c['fields'] for c in filtered_data]

    return HttpResponse(json.dumps(processed_filtered_data), content_type="application/json", status=status)

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