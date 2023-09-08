import csv

from django.core.management.base import BaseCommand

from ...models import Ministry


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with open(f"static/docs/chq_22_clean_8.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)
            for i, row in enumerate(reader):
                name = row[9].replace("\n", "").lower()
                Ministry.objects.get_or_create(
                    name=name,
                )
                self.stdout.write(self.style.SUCCESS(f"{name} added"))
