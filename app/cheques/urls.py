from django.urls import path

from .views import (
    ChequeCreateView,
    ChequeDetailView,
    ChequeListView,
    ChequeUpdateView,
    OwnerCreateView,
    OwnerDetailView,
    OwnerListView,
    OwnerUpdateView,
    cheque_paid_status,
    cheque_returned_status,
)

urlpatterns = [
    path("", ChequeListView.as_view(), name="cheque-list"),
    path("cheque/create/", ChequeCreateView.as_view(), name="cheque-create"),
    path("cheque/update/<int:pk>/", ChequeUpdateView.as_view(), name="cheque-update"),
    path("owners/", OwnerListView.as_view(), name="owner-list"),
    path("owner/create/", OwnerCreateView.as_view(), name="owner-create"),
    path("owner/detail/<int:pk>/", OwnerDetailView.as_view(), name="owner-detail"),
    path("cheque/detail/<int:pk>/", ChequeDetailView.as_view(), name="cheque-detail"),
    path("owner/update/<int:pk>/", OwnerUpdateView.as_view(), name="cheque-update"),
    path("returned/<int:pk>/", cheque_returned_status, name="cheque-returned"),
    path("paid/<int:pk>/", cheque_paid_status, name="cheque-paid"),
]
