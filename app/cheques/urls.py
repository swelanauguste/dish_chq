from django.urls import path

from .views import ChequeListView, cheque_paid_status, cheque_returned_status

urlpatterns = [
    path("", ChequeListView.as_view(), name="cheque-list"),
    path("returned/<int:pk>/", cheque_returned_status, name="cheque-returned"),
    path("paid/<int:pk>/", cheque_paid_status, name="cheque-paid"),
]
