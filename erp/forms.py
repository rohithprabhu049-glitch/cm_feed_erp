from django import forms
from .models import *


class SaleForm(forms.ModelForm):

    class Meta:
        model = Sale

        fields = '__all__'


class ProductionForm(forms.ModelForm):

    class Meta:
        model = Production

        fields = '__all__'

