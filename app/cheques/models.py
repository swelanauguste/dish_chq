# from datetime import date, datetime, timedelta
import datetime

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
        return self.name.title()


class Fee(models.Model):
    name = models.CharField(max_length=50, unique=True)
    price = models.PositiveIntegerField(default=0)
    desc = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - ${self.price}"


class Cheque(models.Model):
    """
    Model for Cheque
    """

    cheque_scan = models.FileField(upload_to="cheques", null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    date_debited = models.DateField()
    owner = models.ForeignKey(
        Owner,
        on_delete=models.CASCADE,
        related_name="cheques",
    )
    returned = models.ForeignKey(Returned, on_delete=models.CASCADE, default=1)
    fee = models.ForeignKey(
        Fee, on_delete=models.PROTECT, related_name="fees", blank=True, null=True
    )
    chq_amount = models.DecimalField("cheque amount", max_digits=10, decimal_places=2)
    journal = models.CharField(max_length=255, blank=True)
    cheque_date = models.DateField()
    cheque_no = models.CharField("cheque number", max_length=255)
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

    def get_days_outstanding(self):
        if self.get_cheque_status and self.get_cheque_status == "paid":
            return (self.cheque_status.updated_at.date() - self.date_debited).days
        return (datetime.date.today() - self.date_debited).days

    def get_cheque_status_colour(self):
        status = self.get_cheque_status()
        if status and status.name == "paid":
            return "success"
        return "warning"

    def get_cheque_status(self):
        try:
            latest_status_update = self.cheques_statuses.latest("updated_at")
            return latest_status_update.cheque_status
        except ChequeStatusUpdate.DoesNotExist:
            return None

    def __str__(self):
        return self.cheque_no.upper()


class ChequeStatus(models.Model):
    """
    Model for Cheque Status
    """

    name = models.CharField(max_length=255)
    desc = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    # def get_absolute_url(self):
    #     return reverse("cheque-status-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name.upper()


class ChequeStatusUpdate(models.Model):
    """
    Model for Cheque Status
    """

    cheque = models.ForeignKey(
        Cheque, on_delete=models.PROTECT, related_name="cheques_statuses"
    )
    cheque_status = models.ForeignKey(
        ChequeStatus, on_delete=models.PROTECT, related_name="statuses"
    )
    details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def get_absolute_url(self):
    #     return reverse("cheque-status-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.cheque_status.name.upper()


class ChequeComment(models.Model):
    """
    Cheque comment model
    """

    cheque = models.ForeignKey(
        Cheque, on_delete=models.PROTECT, related_name="comments"
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="comment_created",
    )
    upated_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="comment_updated",
    )

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.cheque.cheque_no} - {self.comment}"
