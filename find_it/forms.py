from django import forms
from find_it.models import Product

class TaskFilterForm(forms.Form):
    CATEGORY_CHOICES = [
        ("fine_art", "Fine Art"), #Right what user see
        ("graphic_art", "Graphic Art"),
        ("papeterie", "Papeterie"),
        ("art_craft", "Art Craft")
    ]
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=False, label="Category") 

    def __init__(self, *args, **kwargs):
        super(TaskFilterForm, self).__init__(*args, **kwargs)
        self.fields["category"].widget.attrs.update({"class": "form-control"})