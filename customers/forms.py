from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    first_name = forms.CharField(max_length = 255)
    last_name = forms.CharField(max_length = 255)
    email = forms.EmailField()
    address = forms.CharField(max_length = 255)
    city = forms.CharField(max_length = 50)
    state = forms.CharField(max_length = 50)
    zip = forms.CharField(max_length = 5)
     
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'address', 'city', 'state', 'zip']