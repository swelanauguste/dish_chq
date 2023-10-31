from django.contrib import admin

from .models import (
    Cheque,
    ChequeComment,
    ChequeStatus,
    ChequeStatusUpdate,
    Fee,
    Ministry,
    Owner,
    Returned,
)

admin.site.register(Owner)
admin.site.register(Fee)
admin.site.register(Ministry)
admin.site.register(ChequeStatus)
admin.site.register(ChequeStatusUpdate)
admin.site.register(ChequeComment)


@admin.register(Returned)
class ReturnedAdmin(admin.ModelAdmin):
    list_display = ["name", "pk"]


@admin.register(Cheque)
class ChequeAdmin(admin.ModelAdmin):
    list_display = ["cheque_no", "get_cheque_status", "chq_amount", "created_at"]
    search_fields = ["cheque_no"]

    def get_cheque_status(self, obj):
        status = obj.get_cheque_status()
        return status.name if status else None

    get_cheque_status.short_description = "Cheque Status"
