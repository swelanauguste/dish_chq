from django.db.models import Q, Sum
from django.shortcuts import render
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.shortcuts import redirect
from .models import Cheque


class ChequeListView(ListView):
    model = Cheque

    # total_of_all_cheques = Cheque.objects.aggregate(total=Sum("chq_amount"))
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_cheques = Cheque.objects.all()
        paid_cheques = Cheque.objects.filter(cheque_status="P")
        total_amount = sum(cheque.chq_amount for cheque in all_cheques)
        paid_cheque_total_amount = sum(cheque.chq_amount for cheque in paid_cheques)
        context["total_amount"] = total_amount
        context["paid_cheque_total_amount"] = paid_cheque_total_amount
        return context

    def get_queryset(self):
        query = self.request.GET.get("cheques")
        if query:
            return Cheque.objects.filter(
                Q(owner__name__icontains=query)
                | Q(returned__name__icontains=query)
                | Q(cheque_no__icontains=query)
                | Q(ministry__name__icontains=query)
                | Q(receipt_no__icontains=query)
                | Q(receipt_no__icontains=query)
            ).distinct()
        else:
            return Cheque.objects.all()


def cheque_paid_status(request, pk):
    cheque = Cheque.objects.get(pk=pk)
    cheque.cheque_status = "P"
    cheque.save()
    return redirect("cheque-list")


def cheque_returned_status(request, pk):
    cheque = Cheque.objects.get(pk=pk)
    cheque.cheque_status = "R"
    cheque.save()
    return redirect("cheque-list")
