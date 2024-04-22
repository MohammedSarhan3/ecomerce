from django.shortcuts import get_object_or_404, render, redirect
from .models import Cart, Cart_Product, Item_product
from django.contrib import messages
from django.http import JsonResponse
from decimal import Decimal






def add_to_cart(request, product_id):
    try:
        product = get_object_or_404(Item_product, pk=product_id)
        user = request.user if request.user.is_authenticated else None

        # Get or create the user's cart
        cart, created = Cart.objects.get_or_create(User=user)

        # Get the quantity from the form submission
        quantity = int(request.POST.get('cart_quantity', 1))

        # Check if the product is already in the cart
        cart_product, cart_product_created = Cart_Product.objects.get_or_create(
            Cart=cart,
            Product=product,
            defaults={'Quantity': quantity}
        )

        if not cart_product_created:
            # If the product is already in the cart, update the quantity
            cart_product.Quantity += quantity
            cart_product.save()
        else:
            # Save the cart after creating the new cart_product
            cart.save()

        success_message = f"تم إضافة المنتج إلى عربة التسوق"

        # Return a JSON response with the success message
        return JsonResponse({'message': success_message})

    except Exception as e:
        print(f"Error: {e}")
        # Add more details or log the error as needed
        return JsonResponse({'error': 'Internal Server Error'}, status=500)
 

def cart_detail(request):
    user = request.user if request.user.is_authenticated else None
    cart = Cart.objects.filter(User=user).first()

    if cart:
        cart_products = Cart_Product.objects.filter(Cart=cart)

        # Calculate total price and quantity for each cart product
        total_price = 0
        total_quantity = 0

        for cart_product in cart_products:
            cart_product.total_price = cart_product.Product.price * cart_product.Quantity
            total_price += cart_product.total_price
            total_quantity += cart_product.Quantity

        # Update the cart's total price and quantity
        cart.Total_price = total_price
        cart.Total_quantity = total_quantity
        cart.save()

        # Count of items in the cart
        cart_items_count = cart_products.count()
    else:
        cart_products = []
        cart_items_count = 0

    context = {'cart': cart, 'cart_products': cart_products, 'cart_items_count': cart_items_count}
    return render(request, 'cart_detail.html', context)



def remove_from_cart(request, cart_product_id):
    cart_product = get_object_or_404(Cart_Product, pk=cart_product_id)

    # Delete the Cart_Product instance
    cart_product.delete()

    # Optionally, add a success message
    # messages.success(request, "Product removed from your cart.")

    return redirect('cart_detail')


# views.py
from django.shortcuts import render, redirect
from .forms import CheckoutForm
from .models import Cart, Order, Order_Product, Payment, CreditCard, wallet, Cash
from django.contrib import messages
# views.py
from django.shortcuts import render, redirect
from .forms import CheckoutForm
from .models import Cart, Order, Order_Product, Payment, CreditCard, wallet, Cash
from django.contrib import messages
from django.contrib.auth.decorators import login_required




@login_required
def checkout_view(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You need to log in to proceed with the checkout.')
        return redirect('login')

    user_cart = Cart.objects.filter(User=request.user).first()

    if not user_cart or user_cart.cart_product_set.count() == 0:
        messages.error(request, '')
        return redirect('cart_detail')

    cart_products = user_cart.cart_product_set.all()
    new_order = None

    # Calculate total price for all cart products
    total_cart_price = sum(cart_product.Quantity * cart_product.Product.price for cart_product in cart_products) + 20
    for cart_product in cart_products:
        cart_product.total_price = cart_product.Product.price * cart_product.Quantity

    if request.method == 'POST':
        form = CheckoutForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            payment_method = form.cleaned_data['payment_method']

            new_order = Order.objects.create(User=request.user, Status='جاري الشحن', Name=name, Adress=address)
            new_order.save()

            

            payment = Payment.objects.create()
            new_order.Payment = payment

            if payment_method == 'credit_card':
                card_number = form.cleaned_data['card_number']
                cvv = form.cleaned_data['cvv']
                card_password = form.cleaned_data['card_password']
                exp_date = form.cleaned_data['exp_date']

                CreditCard.objects.create(Payment=payment, Card_Number=card_number, CVV=cvv, Card_password=card_password, Exp_Date=exp_date)

            elif payment_method == 'wallet':
                phone_number = form.cleaned_data['phone_number']
                wallet_password = form.cleaned_data['wallet_password']
                carrier = form.cleaned_data['carrier']

                wallet.objects.create(Payment=payment, Phone_number=phone_number, password=wallet_password, carrier=carrier)

            elif payment_method == 'cash':
                receive_date = form.cleaned_data['receive_date']
                Cash.objects.create(Payment=payment, Recieve_date=receive_date)
            
            user_cart_total_price = Decimal(str(user_cart.Total_price))
            shipping_cost = Decimal(str(new_order.Shipping_cost))

            new_order.Total_price = user_cart_total_price + shipping_cost
            new_order.save()

            user_cart.cart_product_set.all().delete()

            messages.success(request, 'Your order has been placed successfully! Thank you for shopping with us.')

            return redirect('order_list')

    else:
        form = CheckoutForm()

    return render(request, 'checkout.html', {'form': form, 'cart_products': cart_products, 'total_cart_price': total_cart_price})


from django.shortcuts import render
from .models import Order


from django.contrib.auth.decorators import login_required

@login_required
def order_list(request):
    # Get the specific order

    # Get a list of orders for the current user
    all_orders = Order.objects.filter(User=request.user)


    return render(request, 'order.html', { 'all_orders': all_orders})

def delete_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.delete()
    # Optionally, add a success message
    # messages.success(request, "Order deleted successfully.")
    return redirect('order_list')  # Redirect to the order list page
