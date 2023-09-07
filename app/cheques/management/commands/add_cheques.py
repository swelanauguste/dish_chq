import csv
from datetime import datetime
from decimal import Decimal

from django.core.management.base import BaseCommand

from ...models import Cheque, Ministry, Owner, Returned


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with open(f"static/docs/ch3.csv", "r") as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                date_debited = datetime.strptime(row[0], "%m/%d/%y")
                owner = Owner.objects.get(name__icontains=row[1].replace("\n", "").lower())
                returned = Returned.objects.get(name__icontains=row[2].replace("\n", "").lower())
                chq_amount = Decimal(row[3].strip())
                cheque_date = datetime.strptime(row[5], "%Y-%m-%d")
                cheque_no = row[4].replace(" ", "").lower()
                ministry = Ministry.objects.get(name__icontains=row[8].replace("\n", "").strip().lower())
                receipt_no = row[7].replace(" ", "").lower().strip()

                Cheque.objects.get_or_create(
                    date_debited=date_debited,
                    owner=owner,
                    returned=returned,
                    chq_amount=chq_amount,
                    cheque_date=cheque_date,
                    cheque_no=cheque_no,
                    ministry=ministry,
                    receipt_no=receipt_no
                )
                self.stdout.write(self.style.SUCCESS(f"{cheque_no} added"))
