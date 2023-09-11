from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django.utils.text import slugify
from users.models import User


class Owner(models.Model):
    """
    Model for Owner
    """

    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    address1 = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("owner-detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name.title()


class Returned(models.Model):
    """
    Model for Returned
    """

    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "returns"
        ordering = ("name",)

    def __str__(self):
        return f"{self.name.upper()}"


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
        ordering = ["name"]
        verbose_name_plural = "Ministries"

    def get_absolute_url(self):
        return reverse("ministry-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name


class ChequeStatus(models.Model):
    """
    Model for Cheque Status
    """

    name = models.CharField(max_length=255)
    desc = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse("cheque-status-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name.upper()


class Cheque(models.Model):
    """
    Model for Cheque
    """

    # CHEQUE_STATUS = (
    #     ("P", "Paid"),
    #     ("U", "Unpaid"),
    #     ("R", "Returned"),
    # )
    is_deleted = models.BooleanField(default=False)
    date_debited = models.DateField()
    owner = models.ForeignKey(
        Owner,
        on_delete=models.CASCADE,
        related_name="cheques",
    )
    returned = models.ForeignKey(Returned, on_delete=models.CASCADE, default=1)
    chq_amount = models.DecimalField("cheque amount", max_digits=10, decimal_places=2)
    journal = models.CharField(max_length=255, blank=True)
    cheque_date = models.DateField()
    cheque_no = models.CharField("cheque number", max_length=255)
    # cheque_status = models.CharField(
    #     max_length=1, choices=CHEQUE_STATUS, default=CHEQUE_STATUS[1][0], blank=True
    # )
    cheque_status = models.ForeignKey(
        ChequeStatus,
        on_delete=models.PROTECT,
        related_name="cheque_statuses",
        null=True,
        blank=True,
        default=1,
    )
    ministry = models.ForeignKey(
        Ministry,
        on_delete=models.CASCADE,
    )
    receipt_no = models.CharField("receipt number", max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="cheques_created",
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="cheques_updated",
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ("date_debited",)

    def get_absolute_url(self):
        return reverse("cheque-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.cheque_no.upper()
