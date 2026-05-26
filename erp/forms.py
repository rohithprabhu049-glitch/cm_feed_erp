from django import forms
from .models import Bill, SaleItem


class BillForm(forms.ModelForm):

    class Meta:

        model = Bill

        fields = '__all__'


class SaleItemForm(forms.ModelForm):

    class Meta:

        model = SaleItem

        fields = '__all__'