from django.contrib import admin

from .models import Cheque, Ministry, Owner, Returned, ChequeStatus

admin.site.register(Owner)
# admin.site.register(Returned)
admin.site.register(Ministry)
admin.site.register(ChequeStatus)




@admin.register(Returned)
class ReturnedAdmin(admin.ModelAdmin):
    list_display = ["name", "pk"]

@admin.register(Cheque)
class ChequeAdmin(admin.ModelAdmin):
    list_display = ["cheque_no", "chq_amount", "cheque_status", 'created_at']
    list_editable = ["cheque_status"]
    search_fields = ["cheque_no"]

