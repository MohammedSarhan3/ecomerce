# forms.py
from django import forms
from .models import Item_product, Product_image

class ProductForm(forms.ModelForm):
    class Meta:
        model = Item_product
        fields = ['Product_name', 'price', 'describtion', 'Category', 'Subcategory']
        widgets = {
            'describtion': forms.Textarea(attrs={'cols': 40, 'rows': 5}),
        }


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = Product_image
        fields = ['Image']
        widgets = {
            'Image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }