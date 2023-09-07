from django.urls import path

from .views import (
    ChequeAddJournalUpdateView,
    ChequeCreateView,
    ChequeDeleteView,
    ChequeDetailView,
    ChequeListView,
    ChequeUpdateView,
    MinistryCreateView,
    MinistryUpdateView,
    OwnerCreateView,
    OwnerDetailView,
    OwnerListView,
    OwnerUpdateView,
    ReturnedCreateView,
    ReturnedUpdateView,
    cheque_paid_status,
    cheque_returned_status,
)

urlpatterns = [
    path("", ChequeListView.as_view(), name="cheque-list"),
    path("cheque/create/", ChequeCreateView.as_view(), name="cheque-create"),
    path("cheque/update/<int:pk>/", ChequeUpdateView.as_view(), name="cheque-update"),
    path("cheque/detail/<int:pk>/", ChequeDetailView.as_view(), name="cheque-detail"),
    path("cheque/delete/<int:pk>/", ChequeDeleteView.as_view(), name="cheque-delete"),
    path(
        "cheque/update-journal/<int:pk>/",
        ChequeAddJournalUpdateView.as_view(),
        name="cheque-update-journal",
    ),
    path("returned/<int:pk>/", cheque_returned_status, name="cheque-returned"),
    path("paid/<int:pk>/", cheque_paid_status, name="cheque-paid"),
    path("owners/", OwnerListView.as_view(), name="owner-list"),
    path("owner/create/", OwnerCreateView.as_view(), name="owner-create"),
    path("owner/detail/<int:pk>/", OwnerDetailView.as_view(), name="owner-detail"),
    path("owner/update/<int:pk>/", OwnerUpdateView.as_view(), name="owner-update"),
    path("ministry/create/", MinistryCreateView.as_view(), name="ministry-create"),
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
]
