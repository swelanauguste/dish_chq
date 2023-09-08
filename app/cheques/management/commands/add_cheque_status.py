from django.core.management.base import BaseCommand

from ...models import ChequeStatus


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with open(f"static/docs/cheque_status_list.txt") as file:
            for row in file:
                name = row.replace("\n", "").strip().lower()
                ChequeStatus.objects.get_or_create(
                    name=name,
                )
                self.stdout.write(self.style.SUCCESS(f"{name} added"))