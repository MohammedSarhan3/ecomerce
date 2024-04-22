# forms.py
from django import forms
from .models import wallet
class CheckoutForm(forms.Form):
    PAYMENT_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('wallet', 'Wallet'),
        ('cash', 'Cash'),
    ]
    
    name = forms.CharField(label='Name', required=True)
    address = forms.CharField(label='Address', required=True)
    payment_method = forms.ChoiceField(label='Payment Method', choices=PAYMENT_CHOICES, widget=forms.RadioSelect)
    card_number = forms.CharField(label='Card Number', required=False)
    cvv = forms.CharField(label='CVV', required=False)
    card_password = forms.CharField(label='Card Password', required=False, widget=forms.PasswordInput)
    exp_date = forms.CharField(label='Expiration Date', required=False)
    phone_number = forms.CharField(label='Phone Number', required=False)
    wallet_password = forms.CharField(label='Wallet Password', required=False, widget=forms.PasswordInput)
    CARRIER_CHOICES = [
        ('vodafone', 'Vodafone'),
        ('orange', 'Orange'),
        ('etisalat', 'Etisalat'),
        ('we', 'We'),
        # Add more carriers as needed
    ]
    
    carrier = forms.ChoiceField(choices=CARRIER_CHOICES, label="شركة الاتصالات", required=False)  
    receive_date = forms.DateField(label='Receive Date', required=False, widget=forms.DateInput(attrs={'type': 'date'}))


