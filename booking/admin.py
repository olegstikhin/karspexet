from django.contrib import admin

# Register your models here.
from .models import Participant, DiscountCode

admin.site.register(Participant)
admin.site.register(DiscountCode)
