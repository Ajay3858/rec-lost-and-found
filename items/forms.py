from django import forms
from .models import Item

class ItemForm(forms.ModelForm):

    class Meta:

        model = Item

        exclude = ["user", "status", "created_at"]

        widgets = {

            "item_name": forms.TextInput(attrs={
                "class":"form-control",
                "placeholder":"Enter item name"
            }),

            "category": forms.Select(attrs={
                "class":"form-select"
            }),

            "location": forms.TextInput(attrs={
                "class":"form-control",
                "placeholder":"Where did you lose it?"
            }),

            "date": forms.DateInput(attrs={
                "class":"form-control",
                "type":"date"
            }),

            "description": forms.Textarea(attrs={
                "class":"form-control",
                "rows":4
            }),

            "contact": forms.TextInput(attrs={
                "class":"form-control",
                "placeholder":"Phone Number"
            }),

            "image": forms.ClearableFileInput(attrs={
                "class":"form-control"
            })

        }