from django import forms
from .models import ListNew


class ListForm(forms.ModelForm):
    class Meta:
        model = ListNew
        fields = ["item", "completed", "owner"]
