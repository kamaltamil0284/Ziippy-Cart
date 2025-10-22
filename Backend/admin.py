from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Products)
admin.site.register(Cart)
admin.site.register(Favourite)
admin.site.register(UserDetails)