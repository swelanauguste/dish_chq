from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q, Sum
from django.shortcuts import redirect, render
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import ChequeForm
from .models import Cheque, Owner
from django.http import HttpResponseRedirect



class OwnerCreateView(CreateView):
    model = Owner
    fields = "__all__"


class OwnerUpdateView(UpdateView):
    model = Owner
    fields = "__all__"


class OwnerDetailView(DetailView):
    model = Owner

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_cheques = Cheque.objects.filter(owner=self.get_object().pk)
        paid_cheques = Cheque.objects.filter(
            cheque_status="P", owner=self.get_object().pk
        )
        total_amount = sum(cheque.chq_amount for cheque in all_cheques)
        paid_cheque_total_amount = sum(cheque.chq_amount for cheque in paid_cheques)
        context["total_amount"] = total_amount
        context["paid_cheque_total_amount"] = paid_cheque_total_amount
        context["all_cheques"] = all_cheques
        return context


class OwnerListView(ListView):
    model = Owner

    def get_queryset(self):
        query = self.request.GET.get("owners")
        if query:
            return Owner.objects.filter(
                Q(owner__name__icontains=query)
                | Q(name__icontains=query)
                | Q(email__icontains=query)
                | Q(phone__icontains=query)
                | Q(address__icontains=query)
                | Q(address1__icontains=query)
            ).distinct()
        else:
            return Owner.objects.all()


class ChequeCreateView(SuccessMessageMixin, CreateView):
    model = Cheque
    form_class = ChequeForm
    success_url = "/"
    success_message = "%(cheque_no)s added"


class ChequeDeleteView(DeleteView):
    model = Cheque
    success_url = "/cheques/"


class ChequeDetailView(DetailView):
    model = Cheque


class ChequeUpdateView(UpdateView):
    model = Cheque
    fields = "__all__"


class ChequeListView(ListView):
    model = Cheque

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
                | Q(chq_amount__icontains=query)
            ).distinct()
        else:
            return Cheque.objects.all()


def cheque_paid_status(request, pk):
    cheque = Cheque.objects.get(pk=pk)
    cheque.cheque_status = "P"
    cheque.save()
    messages.success(request, f"Cheque number {cheque.cheque_no} was updated.") 
    return redirect("cheque-list")


def cheque_returned_status(request, pk):
    cheque = Cheque.objects.get(pk=pk)
    cheque.cheque_status = "R"
    cheque.save()
    messages.success(request, f"Cheque number {cheque.cheque_no} was updated.") 
    return redirect("cheque-list")

