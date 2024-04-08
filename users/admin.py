from django.contrib import admin
from .models import Contact
from import_export.admin import ImportExportModelAdmin # type: ignore


class ContactAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass


admin.site.register(Contact, ContactAdmin)
# Register your models here.
