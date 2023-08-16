import random

from django.core.management.base import BaseCommand
from faker import Faker

from ...models import Cheque, Ministry, Owner, Returned


class Command(BaseCommand):
    help = "Add faker data to the database"

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, help="Number of fake cheque to create")

    def handle(self, *args, **options):
        count = options["count"]
        fake = Faker()
        cheques = []
        for _ in range(count):
            date_debited = fake.date_this_month()
            owner = Owner.objects.get(pk=random.randint(1, 80))
            returned = Returned.objects.get(pk=random.randint(1, 2))
            chq_amount = random.randint(10, 380000)
            cheque_date = fake.date_this_month()
            cheque_no = fake.random_number(digits=9)
            ministry = Ministry.objects.get(pk=random.randint(1, 3))
            receipt_no = fake.random_number(digits=7)
            cheque = Cheque(
                date_debited=date_debited,
                owner=owner,
                returned=returned,
                chq_amount=chq_amount,
                cheque_date=cheque_date,
                cheque_no=cheque_no,
                ministry=ministry,
                receipt_no=receipt_no,
            )
            cheques.append(cheque)
        Cheque.objects.bulk_create(cheques)
        self.stdout.write(self.style.SUCCESS("Data generated"))
