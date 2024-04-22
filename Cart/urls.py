from django.urls import path
from .views import add_to_cart, cart_detail,remove_from_cart,checkout_view,order_list,delete_order
urlpatterns = [
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart_detail/', cart_detail, name='cart_detail'),
        path('remove_from_cart/<int:cart_product_id>/', remove_from_cart, name='remove_from_cart'),
            path('checkout/', checkout_view, name='checkout'),
                path('order', order_list, name='order_list'),
        path('delete_order/<int:order_id>/', delete_order, name='delete_order'),




]






