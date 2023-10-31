import calendar
import csv
from datetime import date, datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q, Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from .filters import ChequeFilter
from .forms import (ChequeAddJournalUpdateViewForm, ChequeCommentCreateForm,
                    ChequeCreateForm, ChequeStatusUpdateForm,
                    ChequeStatusUpdateViewForm, ChequeUpdateForm)
from .models import Cheque, ChequeStatusUpdate, Ministry, Owner, Returned


def get_quarter_start_end_dates(year, quarter):
    quarter_starts = [(1, 1), (4, 1), (7, 1), (10, 1)]
    quarter_ends = [(3, 31), (6, 30), (9, 30), (12, 31)]
    return date(year, *quarter_starts[quarter - 1]), date(
        year, *quarter_ends[quarter - 1]
    )


class ExportMinistryCSVView(View):
    def get(self, request):
        # Retrieve data based on your filters (quarters, bi-annual, ministry, etc.)
        # For example, if you want to filter by ministry:
        ministry_id = request.GET.get("ministry_id")
        quarter = request.GET.get("quarter")
        cheques = Cheque.objects.filter(ministry__id=ministry_id)

        if year and quarter:
            year = int(year)
            quarter = int(quarter)

            start_date, end_date = get_quarter_start_end_dates(year, quarter)

            # Filter Cheques based on date_debited falling within the selected quarter
            cheques = Cheque.objects.filter(date_debited__range=(start_date, end_date))
        else:
            # If year and/or quarter is not provided, return all Cheques
            cheques = Cheque.objects.all()

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="cheques.csv"'

        writer = csv.writer(response)
        writer.writerow(
            [
                "cheque",
                "date_debited",
                "owner",
                "returned",
                "journal",
                "cheque_date",
                "cheque_no",
                "get_cheque_status",
                "receipt_no",
                "created_at",
                "created_by",
                "days_outstanding",
            ]
        )

        for cheque in cheques:
            writer.writerow(
                [
                    cheque.cheque_scan,
                    cheque.date_debited,
                    cheque.owner.name,
                    cheque.returned.name,
                    cheque.journal,
                    cheque.cheque_date,
                    cheque.cheque_no,
                    cheque.get_cheque_status,
                    cheque.receipt_no,
                    cheque.created_at,
                    cheque.created_by,
                    cheque.get_days_outstanding(),
                ]
            )

        return response


class DashboardView(LoginRequiredMixin, TemplateView):
    # Initialize lists to store data for each quarter
    extra_context = {}
    cheques_by_quarter = []
    total_amount_by_quarter = []
    paid_cheque_total_amount_by_quarter = []
    quarters = [
        (datetime(2022, 1, 1), datetime(2022, 3, 31)),
        (datetime(2022, 4, 1), datetime(2022, 6, 30)),
        (datetime(2022, 7, 1), datetime(2022, 9, 30)),
        (datetime(2022, 10, 1), datetime(2022, 12, 31)),
    ]
    for start_date, end_date in quarters:
        cheques = Cheque.objects.filter(date_debited__range=(start_date, end_date))
        paid_cheques = Cheque.objects.filter(
            cheques_statuses__cheque_status__name__iexact="paid",
            date_debited__year=2022,
        )

        total_amount = sum(cheque.chq_amount for cheque in cheques)
        paid_cheque_total_amount = sum(cheque.chq_amount for cheque in paid_cheques)

        unpaid_cheque_total_amount = total_amount - paid_cheque_total_amount

        cheques_by_quarter.append(cheques)
        total_amount_by_quarter.append(total_amount)
        paid_cheque_total_amount_by_quarter.append(paid_cheque_total_amount)

    current_year = datetime.now().year - 1
    all_paid_cheques = Cheque.objects.filter(
        cheques_statuses__cheque_status__name__iexact="paid", date_debited__year=2022
    )
    extra_context["current_year"] = current_year
    extra_context["month_choices"] = [
        (i, datetime(2000, i, 1).strftime("%B")) for i in range(1, 13)
    ]
    extra_context["year_choices"] = range(current_year - 1, current_year + 2)
    for i, quarter in enumerate(["Q1", "Q2", "Q3", "Q4"]):
        extra_context[f"cheques_q{i + 1}"] = cheques_by_quarter[i]
        extra_context[f"total_amount_q{i + 1}"] = total_amount_by_quarter[i]
        extra_context[
            f"paid_cheque_total_amount_q{i + 1}"
        ] = paid_cheque_total_amount_by_quarter[i]
        extra_context[f"unpaid_cheque_total_amount_q{i + 1}"] = (
            total_amount_by_quarter[i] - paid_cheque_total_amount_by_quarter[i]
        )

    template_name = "cheques/dashboard.html"


@login_required
def export_to_csv(request):
    month = request.GET.get("month")
    abbreviated_month_name = calendar.month_abbr[int(month)]
    year = request.GET.get("year")
    response = HttpResponse(content_type="text/csv")
    response[
        "Content-Disposition"
    ] = f'attachment; filename="{abbreviated_month_name}_{year}_cheques.csv"'

    writer = csv.writer(response)
    writer.writerow(
        [
            "cheque",
            "date_debited",
            "owner",
            "returned",
            "journal",
            "cheque_date",
            "cheque_no",
            "get_cheque_status",
            "ministry",
            "receipt_no",
            "created_at",
            "created_by",
            "get_days_outstanding",
        ]
    )  # Write header row
    cheques = Cheque.objects.filter(cheque_date__month=month, cheque_date__year=year)
    for cheque in cheques:
        writer.writerow(
            [
                cheque.cheque_scan,
                cheque.date_debited,
                cheque.owner.name,
                cheque.returned.name,
                cheque.journal,
                cheque.cheque_date,
                cheque.cheque_no,
                cheque.get_cheque_status,
                cheque.ministry.name,
                cheque.receipt_no,
                cheque.created_at,
                cheque.created_by,
                cheque.get_days_outstanding(),
            ]
        )

    return response


class ReportView(LoginRequiredMixin, TemplateView):
    template_name = "cheques/reports.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_year = datetime.now().year
        month_choices = [(i, datetime(2000, i, 1).strftime("%B")) for i in range(1, 13)]
        # year_choices = range(current_year - 3, current_year + 1)  # Adjust as needed
        year_choices = range(current_year - 1, current_year + 1)  # Adjust as needed
        # # start_date = datetime(datetime.today().year, 1, 1)
        # # end_date = datetime(datetime.today().year, 3, 31)

        # Initialize lists to store data for each quarter
        cheques_by_quarter = []
        total_amount_by_quarter = []
        paid_cheque_total_amount_by_quarter = []

        # Define quarters
        quarters = [
            (datetime(2022, 1, 1), datetime(2022, 3, 31)),
            (datetime(2022, 4, 1), datetime(2022, 6, 30)),
            (datetime(2022, 7, 1), datetime(2022, 9, 30)),
            (datetime(2022, 10, 1), datetime(2022, 12, 31)),
        ]

        for start_date, end_date in quarters:
            cheques = Cheque.objects.filter(date_debited__range=(start_date, end_date))
            paid_cheques = cheques.filter(cheque_status__name__iexact="paid")

            total_amount = sum(cheque.chq_amount for cheque in cheques)
            paid_cheque_total_amount = sum(cheque.chq_amount for cheque in paid_cheques)

            unpaid_cheque_total_amount = total_amount - paid_cheque_total_amount

            cheques_by_quarter.append(cheques)
            total_amount_by_quarter.append(total_amount)
            paid_cheque_total_amount_by_quarter.append(paid_cheque_total_amount)

        # Populate context dictionary
        context = {}
        context["month_choices"] = month_choices
        context["year_choices"] = year_choices
        context["filter"] = ChequeFilter(
            self.request.GET, queryset=Cheque.objects.all()
        )
        if not context["filter"].qs.exists():
            context["no_results"] = True

        for i, quarter in enumerate(["Q1", "Q2", "Q3", "Q4"]):
            context[f"cheques_q{i + 1}"] = cheques_by_quarter[i]
            context[f"total_amount_q{i + 1}"] = total_amount_by_quarter[i]
            context[
                f"paid_cheque_total_amount_q{i + 1}"
            ] = paid_cheque_total_amount_by_quarter[i]
            context[f"unpaid_cheque_total_amount_q{i + 1}"] = (
                total_amount_by_quarter[i] - paid_cheque_total_amount_by_quarter[i]
            )
        return context


@login_required
def cheque_comment_create_view(request, pk):
    cheque = get_object_or_404(Cheque, pk=pk)
    if request.method == "POST":
        add_comment_form = ChequeCommentCreateForm(request.POST)
        if add_comment_form.is_valid():
            comment = add_comment_form.save(commit=False)
            comment.cheque = cheque
            comment.created_by = request.user
            comment.upated_by = request.user
            comment.save()
            messages.success(
                request,
                f"Your comment was added.",
            )
            return redirect("cheque-detail", pk=pk)
    else:
        add_comment_form = LetterCreateForm()
    return render(
        request,
        "cheque/cheque_list.html",
        {"add_comment_form": add_comment_form, "cheque": cheque},
    )


class ReturnedCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Returned
    fields = "__all__"
    success_url = reverse_lazy("cheque-list")
    success_message = "%(name)s was created"


class ReturnedUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Returned
    fields = "__all__"
    success_url = reverse_lazy("cheque-list")
    success_message = "%(name)s was updated"
    template_name_suffix = "_update_form"


class MinistryCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Ministry
    fields = "__all__"
    success_url = reverse_lazy("cheque-list")
    success_message = "%(name)s was created"


class MinistryDetailView(LoginRequiredMixin, DetailView):
    model = Ministry

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_cheques = Cheque.objects.filter(ministry=self.get_object().pk)
        paid_cheques = Cheque.objects.filter(
            cheques_statuses__cheque_status__name__iexact="paid",
            ministry=self.get_object().pk,
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
    success_url = reverse_lazy("cheque-list")
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
    success_url = reverse_lazy("cheque-list")
    success_message = "%(name)s was created"


class OwnerUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Owner
    fields = "__all__"
    success_url = reverse_lazy("cheque-list")
    success_message = "%(name)s was updated"
    template_name_suffix = "_update_form"


class OwnerDetailView(LoginRequiredMixin, DetailView):
    model = Owner

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_cheques = Cheque.objects.filter(owner=self.get_object().pk)
        paid_cheques = Cheque.objects.filter(
            cheques_statuses__cheque_status__name__iexact="paid",
            owner=self.get_object().pk,
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
    success_url = reverse_lazy("cheque-list")
    success_message = "%(cheque_no)s was added"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ChequeDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView
):
    model = Cheque
    success_url = reverse_lazy("cheque-list")
    success_message = "This cheque was deleted."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ChequeDeleteView, self).delete(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.is_supervisor


class ChequeDetailView(LoginRequiredMixin, DetailView):
    model = Cheque

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ChequeCommentCreateForm()
        cheque = Cheque.objects.get(pk=self.kwargs["pk"])
        context["cheque"] = cheque
        return context


class ChequeUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Cheque
    form_class = ChequeUpdateForm
    template_name_suffix = "_update_form"

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ChequeStatusUpdateView(UpdateView):
    model = Cheque
    form_class = ChequeStatusUpdateForm
    # template_name = "update_cheque_status.html"
    pk_url_kwarg = (
        "cheque_id"  # Specify the name of the URL parameter for the primary key
    )
    
    def get_object(self, queryset=None):
        return get_object_or_404(ChequeStatusUpdate, cheque_id=self.kwargs['cheque_id'])

    def get_success_url(self):
        return reverse("cheque-detail", kwargs={"pk": self.object.cheque_id})


class ChequeAddJournalUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Cheque
    fields = ["journal"]
    success_message = "Journal was updated"
    success_url = reverse_lazy("cheque-list")

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ChequeStatusChangeUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Cheque
    form_class = ChequeStatusUpdateViewForm
    success_message = "Status was updated"
    success_url = reverse_lazy("cheque-list")

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ChequeListView(LoginRequiredMixin, ListView):
    model = Cheque
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_cheques = Cheque.objects.filter(date_debited__year=2022)
        paid_cheques = Cheque.objects.filter(
            cheques_statuses__cheque_status__name__iexact="paid",
            date_debited__year=2022,
        )
        total_amount = sum(cheque.chq_amount for cheque in all_cheques)
        paid_cheque_total_amount = sum(cheque.chq_amount for cheque in paid_cheques)
        context["total_amount"] = total_amount
        context["paid_cheque_total_amount"] = paid_cheque_total_amount
        context["form"] = ChequeAddJournalUpdateViewForm(initial={})
        context["cheque_status_form"] = ChequeStatusUpdateForm()
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
