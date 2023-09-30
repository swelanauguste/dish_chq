from django.urls import path
from django_filters.views import FilterView

from .views import (
    ChequeAddJournalUpdateView,
    ChequeCreateView,
    ChequeDeleteView,
    ChequeDetailView,
    ChequeListView,
    ChequeStatusChangeUpdateView,
    ChequeUpdateView,
    DashboardView,
    MinistryCreateView,
    MinistryDetailView,
    MinistryListView,
    MinistryUpdateView,
    OwnerCreateView,
    OwnerDetailView,
    OwnerListView,
    OwnerUpdateView,
    ReportView,
    ReturnedCreateView,
    ReturnedUpdateView,
    cheque_comment_create_view,
    export_to_csv,
)

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("cheques/", ChequeListView.as_view(), name="cheque-list"),
    path("cheque/create/", ChequeCreateView.as_view(), name="cheque-create"),
    path("cheque/update/<int:pk>/", ChequeUpdateView.as_view(), name="cheque-update"),
    path("cheque/detail/<int:pk>/", ChequeDetailView.as_view(), name="cheque-detail"),
    path("cheque/delete/<int:pk>/", ChequeDeleteView.as_view(), name="cheque-delete"),
    path(
        "cheque/journal/update/<int:pk>/",
        ChequeAddJournalUpdateView.as_view(),
        name="cheque-update-journal",
    ),
    path(
        "cheque/status/update/<int:pk>/",
        ChequeStatusChangeUpdateView.as_view(),
        name="cheque-update-status",
    ),
    path(
        "cheque/create/<int:pk>/",
        cheque_comment_create_view,
        name="cheque-create-comment",
    ),
    path("owners/", OwnerListView.as_view(), name="owner-list"),
    path("owner/create/", OwnerCreateView.as_view(), name="owner-create"),
    path("owner/detail/<int:pk>/", OwnerDetailView.as_view(), name="owner-detail"),
    path("owner/update/<int:pk>/", OwnerUpdateView.as_view(), name="owner-update"),
    path("ministries/", MinistryListView.as_view(), name="ministry-list"),
    path("ministry/create/", MinistryCreateView.as_view(), name="ministry-create"),
    path(
        "ministry/detail/<int:pk>/",
        MinistryDetailView.as_view(),
        name="ministry-detail",
    ),
    path(
        "ministry/update/<int:pk>/",
        MinistryUpdateView.as_view(),
        name="ministry-update",
    ),
    path("returned/create/", ReturnedCreateView.as_view(), name="returned-create"),
    path(
        "returned/update/<int:pk>/",
        ReturnedUpdateView.as_view(),
        name="returned-update",
    ),
    path("reports/", ReportView.as_view(), name="reports"),
    path("reports/export-to-csv", export_to_csv, name="export-to-csv"),
]
