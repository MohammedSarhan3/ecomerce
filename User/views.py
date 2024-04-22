from django.shortcuts import render, redirect
from .forms import LoginForm, CustomerRegistrationForm,AdminRegistrationForm,CustomUserChangeForm, CustomerEditForm,AdminProfileForm,UserPhoneNumForm
from django.contrib.auth.decorators import login_required
from .models import Customer,Admin,User_Phone_Num
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django import forms
from django.views.generic import UpdateView




class LoginView(AuthLoginView):
    form_class = LoginForm
    template_name = 'login.html'


def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print("User created:", user)

            # Create Customer instance after user has been registered
            customer = Customer.objects.create(User=user)
            print("Customer created:", customer)

            return redirect('login')  # Redirect to the login page

        else:
            print("Form errors:", form.errors)
    else:
        form = CustomerRegistrationForm()

    return render(request, 'registration.html', {'form': form})

def register_admin(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Additional logic specific to admin registration
            admin = Admin.objects.create(User=user, Task=form.cleaned_data['task'])
            return redirect('profile')  # Replace 'home' with the desired URL after successful registration
    else:
        form = AdminRegistrationForm()
    return render(request, 'admin_registration.html', {'form': form})


class CombinedUpdateForm(forms.ModelForm):
    phone_numbers = forms.CharField(required=False)
    

    class Meta:
        model = Customer
        fields = ['country', 'state', 'city', 'street', 'postal_code']



class CombinedUpdateView(UpdateView):
    model = Customer
    template_name = 'profile.html'
    form_class = CombinedUpdateForm

    def get_object(self, queryset=None):
        return self.request.user.customer

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        initial.update({
            'country': user.customer.country,
            'state': user.customer.state,
            'city': user.customer.city,
            'street': user.customer.street,
            'postal_code': user.customer.postal_code,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'profile_picture': user.Image if user.Image else None,
        })
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        form.fields['first_name'] = forms.CharField(initial=user.first_name)
        form.fields['last_name'] = forms.CharField(initial=user.last_name)
        form.fields['email'] = forms.EmailField(initial=user.email)
        form.fields['profile_picture'] = forms.ImageField(initial=user.Image if user.Image else None, required=False)
        return form
    
    def form_valid(self, form):
        # Handle updating Customer model
        customer = form.instance
        customer.country = form.cleaned_data['country']
        customer.state = form.cleaned_data['state']
        customer.city = form.cleaned_data['city']
        customer.street = form.cleaned_data['street']
        customer.postal_code = form.cleaned_data['postal_code']
        customer.save()

        # Handle updating User model
        user = customer.User
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email']

        # Set username as the concatenation of first_name and last_name
        user.username = f"{form.cleaned_data['first_name']}_{form.cleaned_data['last_name']}"

        # Update profile picture
        profile_picture = form.cleaned_data['profile_picture']
        if profile_picture:
            # If a new image is provided, delete the old one
            
            
            # Save the new image
            user.Image = profile_picture

        user.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve the user's phone numbers
        user_phone_numbers = User_Phone_Num.objects.filter(User=self.request.user)
        context['user_phone_numbers'] = user_phone_numbers
        return context



def manage_phone_numbers(request):
    user = request.user

    # Retrieve existing phone numbers for the user
    user_phone_numbers = User_Phone_Num.objects.filter(User=user)

    if request.method == 'POST':
        form = UserPhoneNumForm(request.POST)
        if form.is_valid():
            # Check if the phone number already exists for the user
            phone_number = form.cleaned_data['Phone_num']
            existing_phone_number = User_Phone_Num.objects.filter(User=user, Phone_num=phone_number).first()

            if existing_phone_number:
                # Update existing phone number
                existing_phone_number.Phone_num = phone_number
                existing_phone_number.save()
            else:
                # Save the new phone number
                user_phone = User_Phone_Num.objects.create(User=user, Phone_num=phone_number)

            # Redirect or add additional logic as needed
            return redirect('profile')
    else:
        form = UserPhoneNumForm()

    return render(request, 'phone_number_form.html', {'form': form, 'user_phone_numbers': user_phone_numbers})


def delete_phone_number(request, pk):
    phone_number = get_object_or_404(User_Phone_Num, pk=pk)

    # Check if the user making the request is the owner of the phone number
    if phone_number.User == request.user:
        phone_number.delete()

    # Redirect to the manage_phone_numbers page or another appropriate page
    return redirect('manage_phone_numbers')




