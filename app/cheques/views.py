from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q, Sum
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import (
    ChequeAddJournalUpdateViewForm,
    ChequeCreateForm,
    ChequeStatusUpdateViewForm,
    ChequeUpdateForm,
)
from .models import Cheque, Ministry, Owner, Returned


class ReturnedCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Returned
    fields = "__all__"
    success_url = "/"
    success_message = "%(name)s was created"


class ReturnedUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Returned
    fields = "__all__"
    success_url = "/"
    success_message = "%(name)s was updated"
    template_name_suffix = "_update_form"


class MinistryCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Ministry
    fields = "__all__"
    success_url = "/"
    success_message = "%(name)s was created"


class MinistryDetailView(LoginRequiredMixin, DetailView):
    model = Ministry

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_cheques = Cheque.objects.filter(ministry=self.get_object().pk)
        paid_cheques = Cheque.objects.filter(
            cheque_status__name__icontains='paid', ministry=self.get_object().pk
        )
        total_amount = sum(cheque.chq_amount for cheque in all_cheques)
        paid_cheque_total_amount = sum(cheque.chq_amount for cheque in paid_cheques)
        context["total_amount"] = total_amount
        context["paid_cheque_total_amount"] = paid_cheque_total_amount
        context["all_cheques"] = all_cheques
        return context


class MinistryUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Ministry
    fields = "__all__"
    success_url = "/"
    success_message = "%(name)s was updated"
    template_name_suffix = "_update_form"


class MinistryListView(LoginRequiredMixin, ListView):
    model = Ministry

    def get_queryset(self):
        query = self.request.GET.get("ministries")
        if query:
            return Ministry.objects.filter(
                Q(name__icontains=query)
                | Q(email__icontains=query)
                | Q(phone__icontains=query)
            ).distinct()
        else:
            return Ministry.objects.all()


class OwnerCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Owner
    fields = "__all__"
    success_url = "/"
    success_message = "%(name)s was created"


class OwnerUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Owner
    fields = "__all__"
    success_url = "/"
    success_message = "%(name)s was updated"
    template_name_suffix = "_update_form"


class OwnerDetailView(LoginRequiredMixin, DetailView):
    model = Owner

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_cheques = Cheque.objects.filter(owner=self.get_object().pk)
        paid_cheques = Cheque.objects.filter(
            cheque_status__name__icontains='paid', owner=self.get_object().pk
        )
        total_amount = sum(cheque.chq_amount for cheque in all_cheques)
        paid_cheque_total_amount = sum(cheque.chq_amount for cheque in paid_cheques)
        context["total_amount"] = total_amount
        context["paid_cheque_total_amount"] = paid_cheque_total_amount
        context["all_cheques"] = all_cheques
        return context


class OwnerListView(LoginRequiredMixin, ListView):
    model = Owner

    def get_queryset(self):
        query = self.request.GET.get("owners")
        if query:
            return Owner.objects.filter(
                Q(name__icontains=query)
                | Q(email__icontains=query)
                | Q(phone__icontains=query)
                | Q(address__icontains=query)
                | Q(address1__icontains=query)
            ).distinct()
        else:
            return Owner.objects.all()


class ChequeCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Cheque
    form_class = ChequeCreateForm
    success_url = "/"
    success_message = "%(cheque_no)s was added"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ChequeDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView
):
    model = Cheque
    success_url = "/"
    success_message = "This cheque was deleted."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ChequeDeleteView, self).delete(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.is_supervisor


class ChequeDetailView(LoginRequiredMixin, DetailView):
    model = Cheque


class ChequeUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Cheque
    form_class = ChequeUpdateForm
    template_name_suffix = "_update_form"

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ChequeAddJournalUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Cheque
    fields = ["journal"]
    success_message = "Journal was updated"
    success_url = "/"

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ChequeStatusChangeUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Cheque
    form_class = ChequeStatusUpdateViewForm
    success_message = "Status was updated"
    success_url = "/"

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ChequeListView(LoginRequiredMixin, ListView):
    model = Cheque

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_cheques = Cheque.objects.all()
        paid_cheques = Cheque.objects.filter(cheque_status__name__icontains='paid')
        total_amount = sum(cheque.chq_amount for cheque in all_cheques)
        paid_cheque_total_amount = sum(cheque.chq_amount for cheque in paid_cheques)
        context["total_amount"] = total_amount
        context["paid_cheque_total_amount"] = paid_cheque_total_amount
        context["form"] = ChequeAddJournalUpdateViewForm(initial={})
        context["cheque_status_form"] = ChequeStatusUpdateViewForm(initial={})
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


# @login_required
# def cheque_paid_status(request, pk):
#     cheque = Cheque.objects.get(pk=pk)
#     cheque.cheque_status = "P"
#     cheque.save()
#     cheque_status_display = cheque.get_cheque_status_display()
#     messages.success(
#         request, f"Cheque number {cheque.cheque_no} was {cheque_status_display}."
#     )
#     return redirect("cheque-list")


# @login_required
# def cheque_returned_status(request, pk):
#     cheque = Cheque.objects.get(pk=pk)
#     cheque.cheque_status = "R"
#     cheque.save()
#     cheque_status_display = cheque.get_cheque_status_display()
#     messages.success(
#         request, f"Cheque number {cheque.cheque_no} was {cheque_status_display}."
#     )
#     return redirect("cheque-list")
