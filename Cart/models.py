from django.db import models
from product.models import Item_product
# Create your models here.
#payment  credit_card wallet  order
# cash cart cart_product order_product 
from User.models import User
class Payment(models.Model):
    Payment_id = models.AutoField(primary_key=True)

    def __str__(self):
        payment_type = get_payment_type(self)
        return f"{payment_type} - {self.Payment_id}"

def get_payment_type(payment_instance):
    if hasattr(payment_instance, 'creditcard') and payment_instance.creditcard is not None:
        return 'Credit Card'
    elif hasattr(payment_instance, 'wallet') and payment_instance.wallet is not None:
        return 'Wallet'
    elif hasattr(payment_instance, 'cash') and payment_instance.cash is not None:
        return 'Cash'
    else:
        return 'Unknown'
from django.core.exceptions import ValidationError
from datetime import datetime

def validate_mm_yy_date_format(value):
    try:
        # Parse the input string to create a datetime.date object
        datetime.strptime(value, '%m/%y').date()
    except ValueError:
        raise ValidationError("Invalid date format. Use 'MM/YY'.")


class CreditCard(models.Model):
    name=models.CharField(max_length=16, blank=True, null=True,default="CreditCard")
    Payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    Card_Number = models.CharField(max_length=16, blank=True, null=True)
    CVV = models.CharField(max_length=4, blank=True, null=True)
    Card_password = models.CharField(max_length=20, blank=True, null=True)
    Exp_Date = models.CharField(max_length=5, blank=True, null=True, validators=[validate_mm_yy_date_format])
    def __str__(self):
        return f"CreditCard {self.id}"

CARRIER_CHOICES = [
        ('vodafone', 'Vodafone'),
        ('orange', 'Orange'),
        ('etisalat', 'Etisalat'),
        ('we', 'We'),
        # Add more carriers as needed
    ]
class wallet(models.Model):
    name=models.CharField(max_length=16, blank=True, null=True,default="wallet")

    Payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    Phone_number = models.CharField(max_length=15, blank=True, null=True)
    password = models.CharField(max_length=20, blank=True, null=True)
  

    carrier = models.CharField(max_length=10, choices=CARRIER_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"Wallet {self.id}"


class Cash(models.Model):
    name=models.CharField(max_length=16, blank=True, null=True,default="Cash")
    Payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    Recieve_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Cash {self.id}"


class Order(models.Model):
    Order_id = models.AutoField(primary_key=True)
    User = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    Payment = models.ForeignKey(Payment, on_delete=models.CASCADE, blank=True, null=True)
    Shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=20.0)
    Adress = models.CharField(max_length=50, blank=True, null=True)
    Name = models.CharField(max_length=50, blank=True, null=True)
    Status = models.CharField(max_length=20, blank=True, null=True)
    Total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"Order {self.Order_id}"


class Cart(models.Model):
    Cart_id = models.AutoField(primary_key=True)
    User = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    Total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    Notes = models.TextField(blank=True, null=True)
   

    def __str__(self):
        return f"Cart {self.Cart_id}"


class Cart_Product(models.Model):
    Cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True)
    Product = models.ForeignKey(Item_product, on_delete=models.CASCADE, blank=True, null=True)
    Quantity = models.IntegerField(default=1)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Fetch the related Cart instance
        cart = Cart.objects.get(pk=self.Cart.pk)

        # Update the Cart's total price
        cart.Total_price += self.Product.price * self.Quantity
        cart.save()

    def __str__(self):
        return f"Cart_Product {self.id}"


class Order_Product(models.Model):
    Order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    Product = models.ForeignKey(Item_product, on_delete=models.CASCADE, blank=True, null=True)
    Quantity = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"Order_Product {self.id}"
