from django.db import models
from User.models import User
# Create your models here.
#Item_product category subcategory 
# porduct_image stock discount
# discount_product review stock_product










class Discount(models.Model):
    Discount_id = models.AutoField(primary_key=True)
    Value = models.DecimalField(max_digits=2, decimal_places=2, blank=True, null=True)
    Start_date = models.DateField( blank=True, null=True)
    End_date = models.DateField( blank=True, null=True)
    def __str__(self):
        return f"Discount - {self.Value}%"


class Category(models.Model):
    Category_id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=20, unique=True, blank=True, null=True)
    describtion = models.TextField(blank=True, null=True)
    Image = models.ImageField(upload_to='category_images', blank=True, null=True)
    def __str__(self):
        return self.Name


class Subcategory(models.Model):
    Subcategory_id = models.AutoField(primary_key=True)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    Name = models.CharField(max_length=20, blank=True, null=True)
    describtion = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.Category.Name} - {self.Name}"


class Item_product(models.Model):
    Product_id = models.AutoField(primary_key=True)
    Product_name = models.CharField(max_length=20, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    describtion = models.TextField(blank=True, null=True)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    Subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.Product_name


class Product_image(models.Model):
    Product = models.ForeignKey(Item_product, on_delete=models.CASCADE, blank=True, null=True)
    Image = models.ImageField(upload_to='product_images', blank=True, null=True)
    def __str__(self):
        return f"Image for {self.Product.Product_name}"


class Stock(models.Model):
    Stock_id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=20, blank=True, null=True)
    Address = models.CharField(max_length=50, blank=True, null=True)
    def __str__(self):
        return self.Name




class Review(models.Model):
    Review_id = models.AutoField(primary_key=True)
    User = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    Product = models.ForeignKey(Item_product, on_delete=models.CASCADE, blank=True, null=True)
    describtion = models.TextField(blank=True, null=True)
    Rate = models.IntegerField( blank=True, null=True)
    Created_at = models.DateField( blank=True, null=True)
    def __str__(self):
        return f"Review by {self.User} for {self.Product.Product_name}"


class Discount_Product(models.Model):
    Discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
    Product = models.ForeignKey(Item_product, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.Discount} applied to {self.Product.Product_name}"


class Stock_Product(models.Model):
    Stock = models.ForeignKey(Stock, on_delete=models.CASCADE, blank=True, null=True)
    Product = models.ForeignKey(Item_product, on_delete=models.CASCADE, blank=True, null=True)
    #Available_quantity = models.IntegerField( blank=True, null=True)
    def __str__(self):
        return f"{self.Product.Product_name} in {self.Stock.Name}"


