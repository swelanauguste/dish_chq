import csv
from datetime import datetime
from decimal import Decimal

from django.core.management.base import BaseCommand

from ...models import Cheque, ChequeStatus, Ministry, Owner, Returned


class Command(BaseCommand):
    Cheque.objects.all().delete()
    def handle(self, *args, **kwargs):
        with open(f"static/docs/chq_22_clean_8.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)
            for i, row in enumerate(reader):
                date_debited = datetime.strptime(row[1], "%d-%b-%y")
                owner = Owner.objects.get(
                    name__iexact=row[2].replace("\n", "").lower()
                )
                returned = Returned.objects.get(
                    name__icontains=row[3].replace("\n", "").lower().strip()
                )
                chq_amount = Decimal(row[4].strip())
                cheque_date = datetime.strptime(row[6], "%d/%m/%Y")
                cheque_no = row[5].replace(" ", "").lower()
                cheque_status = ChequeStatus.objects.get(
                    name__iexact=row[7].replace("\n", "").lower().strip()
                )
                ministry = Ministry.objects.get(
                    name__icontains=row[9].replace("\n", "").strip().lower()
                )
                receipt_no = row[8].replace(" ", "").lower().strip()
                Cheque.objects.get_or_create(
                    date_debited=date_debited,
                    owner=owner,
                    returned=returned,
                    chq_amount=chq_amount,
                    cheque_date=cheque_date,
                    cheque_no=cheque_no,
                    cheque_status=cheque_status,
                    ministry=ministry,
                    receipt_no=receipt_no,
                )
                self.stdout.write(self.style.SUCCESS(f"{cheque_no.upper()} added"))
