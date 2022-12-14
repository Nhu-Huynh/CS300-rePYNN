from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['dish']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'paid', 'created']
    list_filter = ['paid', 'created']
    inlines = [OrderItemInline]
