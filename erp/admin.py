from django.contrib import admin
from .models import *

admin.site.register(Product)
admin.site.register(Bill)
admin.site.register(SaleItem)
admin.site.register(Production)
admin.site.register(RawMaterial)