from django.contrib import admin
# Models
from . import models


admin.site.register(models.Order)
admin.site.register(models.Product)
admin.site.register(models.OrderDetail)
