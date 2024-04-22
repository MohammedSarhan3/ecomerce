# admin.py
from django.contrib import admin
from .models import Payment, CreditCard, wallet, Cash, Order, Cart, Cart_Product, Order_Product

@admin.register(Payment, CreditCard, wallet, Cash)
class PaymentAdmin(admin.ModelAdmin):
    pass

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('Order_id', 'User','Name', 'Payment', 'Shipping_cost', 'Adress', 'Status','Total_price')
    search_fields = ['Order_id', 'User__username']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('Cart_id', 'User', 'Total_price', 'Notes')
    search_fields = ['Cart_id', 'User__username']

@admin.register(Cart_Product)
class CartProductAdmin(admin.ModelAdmin):
    list_display = ('Cart', 'Product', 'Quantity')
    search_fields = ['Cart__Cart_id', 'Product__name']

@admin.register(Order_Product)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('Order', 'Product', 'Quantity')
    search_fields = ['Order__Order_id', 'Product__name']
