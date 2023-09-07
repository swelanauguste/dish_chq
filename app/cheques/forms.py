from django import forms

from .models import Cheque


class ChequeCreateForm(forms.ModelForm):
    class Meta:
        model = Cheque
        fields = "__all__"
        exclude = [
            "created_by",
            "updated_by",
            "is_deleted",
            "receipt_no",
            "journal",
            "cheque_status",
        ]
        widgets = {
            "date_debited": forms.TextInput(attrs={"type": "date"}),
            "cheque_date": forms.TextInput(attrs={"type": "date"}),
        }


class ChequeUpdateForm(forms.ModelForm):
    class Meta:
        model = Cheque
        fields = "__all__"
        exclude = ["created_by", "updated_by", "is_deleted"]
        widgets = {
            "date_debited": forms.TextInput(attrs={"type": "date"}),
            "cheque_date": forms.TextInput(attrs={"type": "date"}),
        }


class ChequeAddJournalUpdateViewForm(forms.ModelForm):
    class Meta:
        model = Cheque
        fields = ["journal"]


class ChequeStatusUpdateViewForm(forms.ModelForm):
    class Meta:
        model = Cheque
        fields = ["cheque_status"]
        widgets = {
            "cheque_date": forms.TextInput(attrs={"type": "date"}),
        }
