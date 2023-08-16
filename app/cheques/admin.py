from django.contrib import admin

from .models import Cheque, Ministry, Owner, Returned

admin.site.register(Owner)
admin.site.register(Returned)
admin.site.register(Ministry)
admin.site.register(Cheque)
