from django.db import models
from django.db.models import Sum

class Owner(models.Model):
    """
    Model for Owner
    """

    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class Returned(models.Model):
    """
    Model for Returned
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


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
        return self.name


class Cheque(models.Model):
    """
    Model for Cheque
    """

    CHEQUE_STATUS = (
        ("P", "Paid"),
        ("R", "Returned"),
    )
    date_debited = models.DateField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    returned = models.ForeignKey(Returned, on_delete=models.CASCADE)
    returned_other = models.CharField("other", max_length=255, blank=True)
    chq_amount = models.DecimalField(max_digits=10, decimal_places=2)
    cheque_date = models.DateField()
    cheque_no = models.CharField(max_length=255)
    cheque_status = models.CharField(max_length=1, choices=CHEQUE_STATUS, default=CHEQUE_STATUS[0][0], blank=True)
    ministry = models.ForeignKey(Ministry, on_delete=models.CASCADE)
    receipt_no = models.CharField(max_length=255)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('date_debited',)
        
    # get sum of objects chq_amount
    
        
    # def get_sum_of_all_cheques(self):
    #     return Cheque.objects.aggregate(total=Sum("chq_amount"))
    
    # total_of_all_cheques = Cheque.objects.aggregate(total=Sum("chq_amount"))

    def __str__(self):
        return f"{self.owner} - {self.chq_amount} - {self.cheque_status}"
