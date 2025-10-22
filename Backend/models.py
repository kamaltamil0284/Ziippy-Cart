from django.db import models
from django.utils import timezone
import os
from django.contrib.auth.models import User


def getfilename(request,filename):
    # use timezone-aware timestamp and avoid characters invalid on Windows filenames
    now = timezone.now().strftime("%Y%m%d%H%M%S")
    new_filename = "%s%s" % (now, filename)
    return os.path.join('uploads/',new_filename)

class Category(models.Model):
    name = models.CharField(max_length=150,null=False,blank=False)
    image = models.ImageField(upload_to=getfilename,null=True,blank=True)
    description = models.TextField(max_length=400,null=True,blank=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Products(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    product_name = models.CharField(max_length=150,null=False,blank=False)
    seller =  models.CharField(max_length=100,null=False,blank=False)
    product_image = models.ImageField(upload_to=getfilename,null=True,blank=True)
    quantity = models.IntegerField(null=False,blank=False)
    description = models.TextField(max_length=500,null=True,blank=True)
    original_price = models.FloatField(null=False,blank=False)
    selling_price = models.FloatField(null=False,blank=False)
    status = models.BooleanField(default=False)
    trending = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.product_name

class Favourite(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.product_name

class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, null=False, blank=False)
    mobile = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return self.user.username
