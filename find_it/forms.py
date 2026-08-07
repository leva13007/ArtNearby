from django import forms
from find_it.models import Product, Store
from find_it.mixins import UserIsOverMixin

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ["name", "description", "phone", "website"]

    def __init__(self, *args, **kwargs):
        super(StoreForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["store", "name", "category", "price", "fabricator", "description", "image"] 

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProductForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


class ProductFilterForm(forms.Form):
    CATEGORY_CHOICES = [
        ("fine_art", "Fine Art"), #Right what user see
        ("graphic_art", "Graphic Art"),
        ("papeterie", "Papeterie"),
        ("art_craft", "Art Craft")
    ]
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=False, label="Category") 

    def __init__(self, *args, **kwargs):
        super(ProductFilterForm, self).__init__(*args, **kwargs)
        self.fields["category"].widget.attrs.update({"class": "form-control"})