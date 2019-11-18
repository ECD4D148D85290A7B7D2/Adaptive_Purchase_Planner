from django.contrib import admin
from .models import Purchases
# Register your models here.

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'item', 'price', 'store', 'purchase_date']
    search_fields = ['item']
    list_filter = ['purchase_date', 'item']

admin.site.register(Purchases, PurchaseAdmin)
