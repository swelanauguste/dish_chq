import csv

from django.core.management.base import BaseCommand

from ...models import Returned

Returned.objects.all().delete()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with open(f"static/docs/chq_22_clean_8.csv") as file:
            reader = csv.reader(file)
            next(reader)
            for i, row in enumerate(reader):
                name = row[3].replace("\n", "").lower().strip()
                Returned.objects.get_or_create(
                    name=name,
                )
                self.stdout.write(self.style.SUCCESS(f"{name} added"))
