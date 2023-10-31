import datetime

from django.db.models import Sum

from ..models import Cheque


def sum_of_all_cheques(request):
    current_year = datetime.datetime.now().year - 1
    total_sum = (
        Cheque.objects.filter(date_debited__year=(current_year)).aggregate(
            total_sum=Sum("chq_amount")
        )["total_sum"]
        or 0
    )
    return {"total_sum_of_cheques": f"{total_sum:.2f}"}


def sum_of_all_paid_cheques(request):
    current_year = datetime.datetime.now().year - 1
    total_sum = (
        Cheque.objects.filter(
            date_debited__year=current_year,
            cheques_statuses__cheque_status__name__iexact="paid",
        ).aggregate(total_sum=Sum("chq_amount"))["total_sum"]
        or 0
    )
    return {"total_sum_of_paid_cheques": f"{total_sum:.2f}"}


def sum_of_all_unpaid_cheques(request):
    current_year = datetime.datetime.now().year - 1
    sum_of_all_cheques = (
        Cheque.objects.filter(date_debited__year=current_year).aggregate(
            total_sum=Sum("chq_amount")
        )["total_sum"]
        or 0
    )

    sum_of_all_paid_cheques = (
        Cheque.objects.filter(
            date_debited__year=current_year,
            cheques_statuses__cheque_status__name__iexact="paid",
        ).aggregate(total_sum=Sum("chq_amount"))["total_sum"]
        or 0
    )

    total_sum = sum_of_all_cheques - sum_of_all_paid_cheques
    return {"total_sum_of_unpaid_cheques": f"{total_sum:.2f}"}


# extra_context["all_paid_cheques"] = sum(
#         cheque.chq_amount
#         for cheque in Cheque.objects.filter(date_debited__year=(current_year))
#     )
#     extra_context["all_paid_cheques_total"] = (
#         sum(cheque.chq_amount for cheque in all_paid_cheques)
