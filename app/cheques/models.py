from django.db import models
from django.db.models import Sum


class Owner(models.Model):
    """
    Model for Owner
    """

    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    address1 = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name.title()


class Returned(models.Model):
    """
    Model for Returned
    """

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name.title()


class Ministry(models.Model):
    """
    Model for Ministrty
    """

    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name.title()


class Cheque(models.Model):
    """
    Model for Cheque
    """

    CHEQUE_STATUS = (
        ("P", "Paid"),
        ("U", "Unpaid"),
        ("R", "Returned"),
    )
    date_debited = models.DateField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name="cheques")
    returned = models.ForeignKey(Returned, on_delete=models.CASCADE)
    returned_other = models.CharField("other", max_length=255, blank=True)
    chq_amount = models.DecimalField("cheque amount", max_digits=10, decimal_places=2)
    journal = models.CharField(max_length=255, blank=True)
    cheque_date = models.DateField()
    cheque_no = models.CharField("cheque number", max_length=255)
    cheque_status = models.CharField(
        max_length=1, choices=CHEQUE_STATUS, default=CHEQUE_STATUS[1][0], blank=True
    )
    ministry = models.ForeignKey(Ministry, on_delete=models.CASCADE)
    receipt_no = models.CharField("receipt number", max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("date_debited",)

    def __str__(self):
        return f"{self.owner} - ${self.chq_amount} - {self.cheque_status}"
