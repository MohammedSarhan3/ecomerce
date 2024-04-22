from django import forms
from .models import User ,Customer,Admin,User_Phone_Num
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username')

class CustomerRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.CharField(max_length=50)



    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email','password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['first_name'] + self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class AdminRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    task = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'password1', 'password2', 'task')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['first_name'] + self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = [ 'Task']

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']  # You can customize this list based on your requirements

class CustomerEditForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['country', 'state', 'city', 'street', 'postal_code']


class PhoneForm(forms.Form):
    phone_number = forms.CharField(max_length=15)

class UserPhoneNumForm(forms.ModelForm):
    class Meta:
        model = User_Phone_Num
        fields = ['Phone_num']