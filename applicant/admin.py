from django.contrib import admin
from import_export.admin import ImportExportModelAdmin # type: ignore
from .models import Applicants, Work, Work_Category

# Register your models here.


class ApplicantsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass



admin.site.register(Applicants, ApplicantsAdmin)
admin.site.register(Work)
admin.site.register(Work_Category)
