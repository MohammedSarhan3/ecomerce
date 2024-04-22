from django.shortcuts import render,redirect
from django.views import View
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Item_product, Product_image ,Category, Subcategory
from .forms import ProductForm, ProductImageForm
from django.views.generic import ListView, DetailView
from random import shuffle
from django.utils.text import slugify

class ProductListView(ListView):
    model = Item_product
    template_name = 'home.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        products = list(queryset)
        shuffle(products)  # Shuffle the list of products
        return products
    

class ProductDetailView(DetailView):
    model = Item_product
    template_name = 'product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.Product_name  # Add product name as title
        return context

from collections import defaultdict






class CategoryListView(ListView):
    model = Item_product
    template_name = 'category.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        queryset = super().get_queryset()

        category_products = queryset.filter(Category__Category_id=category_id)

        products_grouped = defaultdict(list)
        for product in category_products:
            subcategory_name = product.Subcategory.Name if product.Subcategory else 'No Subcategory'
            products_grouped[subcategory_name].append(product)

        return dict(products_grouped)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs['category_id']

        category_name = Category.objects.get(Category_id=category_id).Name
        context['category_name'] = category_name
        context['category_id'] = category_id

        # Get the subcategories related to the current category
        subcategories = Subcategory.objects.filter(Category__Category_id=category_id)
        context['subcategories'] = subcategories

        return context

def category_view(request):
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()

    context = {'categories': categories, 'subcategories': subcategories}
    return render(request, 'category_view.html', context)


class AddProductView(View):
    template_name = 'add_product.html'

    def get(self, request):
        form = ProductForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return redirect('add_product_images', product_id=product.pk)
        return render(request, self.template_name, {'form': form})
    



class AddProductImagesView(View):
    template_name = 'add_product_images.html'

    def get(self, request, product_id):
        product = Item_product.objects.get(pk=product_id)
        image_form = ProductImageForm()
        return render(request, self.template_name, {'product': product, 'image_form': image_form})

    def post(self, request, product_id):
        product = Item_product.objects.get(pk=product_id)
        image_form = ProductImageForm(request.POST, request.FILES)
        if image_form.is_valid():
            image = image_form.save(commit=False)
            image.Product = product
            image.save()
            return redirect('add_product')  # Redirect to the add_product_images view
        return render(request, self.template_name, {'product': product, 'image_form': image_form})




def selected_subcategories_view(request):
    # Select random subcategories
    selected_subcategories = Subcategory.objects.all().order_by('?')[:7]  # Change 5 to the number you want

    context = {'selected_subcategories': selected_subcategories}
    return render(request, 'selected_subcategories.html', context)


from django.shortcuts import render, get_object_or_404

def subcategory_products(request, subcategory_id):
    subcategory = get_object_or_404(Subcategory, pk=subcategory_id)
    products = Item_product.objects.filter(Subcategory=subcategory)
    
    context = {'subcategory': subcategory, 'products': products}
    return render(request, 'subcategory_products.html', context)