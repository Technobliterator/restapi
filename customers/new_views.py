from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.core import serializers
from django.forms.models import fields_for_model, model_to_dict
from .models import Customer
from .filters import CustomerFilter
from .forms import CustomerForm
from rest_framework.views import APIView
import json

class CustomerView(APIView):
    model = Customer
    objects = model.objects.order_by('last_name')
    form_class = CustomerForm
    filter_class = CustomerFilter

    def get(self, request):
        status = 200
        if request.method == 'POST':
            self.post(request)
            status = 201

        data = Customer.objects.order_by('last_name')

        filter = self.filter_class(request.GET, queryset=data)	
        filtered_data = serializers.serialize('python', filter.qs)
        processed_filtered_data = [c['fields'] for c in filtered_data]

        return HttpResponse(json.dumps(processed_filtered_data), content_type="application/json", status=status)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        else:
            return Http404("Form is invalid; please try again")

    def delete(response, id):
        customer = verify_customer(id)
        customer.delete()
        return redirect('customers')

    def verify_customer(id):
        try:
            customer = self.objects.get(pk=id)
            return customer
            #processed_data = {'Full name': customer.get_full_name()}
        except Customer.DoesNotExist:
            raise Http404("Customer does not exist")

    def get_customer(response, id):
        customer = verify_customer(id)
        processed_data = model_to_dict(customer)
        return JsonResponse(processed_data)