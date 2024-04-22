# admin.py
from django.contrib import admin
from .models import Discount, Category, Subcategory, Item_product, Product_image, Stock, Review, Discount_Product, Stock_Product

# Register your models here
admin.site.register(Discount)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Item_product)
admin.site.register(Product_image)
admin.site.register(Stock)
admin.site.register(Review)
admin.site.register(Discount_Product)
admin.site.register(Stock_Product)
