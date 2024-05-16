from django.contrib import admin
from .models import Contact, Post
from import_export.admin import ImportExportModelAdmin # type: ignore


class ContactAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass


admin.site.register(Contact, ContactAdmin)
admin.site.register(Post)

# Register your models here.
