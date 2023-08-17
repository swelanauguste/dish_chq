from django import forms

from .models import Cheque, Owner

class ChequeForm(forms.ModelForm):
    class Meta:
        model = Cheque
        fields = "__all__"
        exclude = ["created_at", "updated_at"]
        widgets = {
            "date_debited": forms.TextInput(attrs={"type": "date"}),
            "cheque_date": forms.TextInput(attrs={"type": "date"}),
        }
