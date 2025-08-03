from django import forms
from secondapp.models import add_product

class add_product_form(forms.ModelForm):
    class Meta:
        model = add_product
        # fields = "__all__"
        fields = ["product_name", "product_price", "sale_price", "product_desc", "product_image", "details", "category"]
        
class JazzCashForm(forms.Form):
    amount = forms.DecimalField(label="Amount", max_digits=10, decimal_places=2)
    # Add other fields as needed