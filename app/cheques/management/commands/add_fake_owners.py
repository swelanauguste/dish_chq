import random

from django.core.management.base import BaseCommand
from faker import Faker

from ...models import Cheque, Owner


class Command(BaseCommand):
    help = "Add faker data to the database"

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, help="Number of fake owners to create")

    def handle(self, *args, **options):
        count = options["count"]
        fake = Faker()
        owners = []
        for _ in range(count):
            name = fake.company()
            owner = Owner(
                name=name,
            )
            owners.append(owner)
        Owner.objects.bulk_create(owners)
        self.stdout.write(self.style.SUCCESS("Data generated"))
