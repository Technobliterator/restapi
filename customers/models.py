from django.db import models

# Create your models here.
class Customer(models.Model):
    first_name = models.TextField(max_length = 255)
    last_name = models.TextField(max_length = 255)
    email = models.EmailField(max_length = 255)
    address = models.TextField(max_length = 255)
    city = models.TextField(max_length = 50)
    state = models.TextField(max_length = 50)
    zip = models.TextField(max_length = 5)

    def __str__(self):
        return self.first_name
    
    def get_full_name(self):
        return self.first_name + ' ' + self.last_name