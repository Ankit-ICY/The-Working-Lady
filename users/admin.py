from django.contrib import admin
from .models import Contact, Post, Blog
from import_export.admin import ImportExportModelAdmin # type: ignore


class ContactAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass


admin.site.register(Contact, ContactAdmin)
admin.site.register(Post)
admin.site.register(Blog)


# Register your models here.
